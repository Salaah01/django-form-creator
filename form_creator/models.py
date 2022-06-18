import typing as _t
import sys
from django.db import models
from django.db.models import Q, QuerySet
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from .question_form_fields import FieldTypeChoices, is_choice_field
from .managers import FormManager

User = get_user_model()

# When running test suite, it moans about the url app name not existing in the
# namespace. This fixes it, but it's a bit of a hack.
TESTING = "test" in sys.argv[0]
url_prefix = "form_creator:"


class Form(models.Model):
    """The configuration for a form."""

    class StatusChoices(models.TextChoices):
        """The status of a form."""

        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    editors = models.ManyToManyField(User, related_name="editors", blank=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    start_dt = models.DateTimeField(
        default=timezone.now,
        verbose_name="Start on",
    )
    end_dt = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Leave blank for no end date.",
        verbose_name="End on",
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )

    objects = FormManager()

    class Meta:
        db_table = "fc_form"
        ordering = ["status", "-created_dt"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save method to set the slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def can_edit(self, user: User) -> bool:
        """Check if the user can edit the form."""
        if not user or not user.is_authenticated:
            return False
        return any(
            [
                user.is_staff,
                user.username == self.owner.username,
                user in self.editors.all(),
            ]
        )

    def can_delete(self, user: User) -> bool:
        """Check if the user can delete the form."""
        if not user or not user.is_authenticated:
            return False
        return any([user.is_staff, user.username == self.owner.username])

    def completed_by(self, user: User) -> _t.Optional["FormResponder"]:
        """Get the form responder for the user."""
        if not user or not user.is_authenticated:
            return None
        return self.responders.filter(user=user).first()

    def can_complete_form(self, user: User) -> bool:
        """Check if the user can complete the form."""
        if not user or not user.is_authenticated:
            return False

        if not self.is_live():
            return False

        if self.can_edit(user):
            return False

        return not bool(self.completed_by(user))

    def get_absolute_url(self) -> str:
        """Get the absolute URL for the form."""
        return reverse(f"{url_prefix}form_detail", args=[self.id, self.slug])

    def get_edit_url(self) -> str:
        """Get the URL for the form's edit view."""
        return reverse(f"{url_prefix}form_edit", args=[self.id, self.slug])

    def get_delete_url(self) -> str:
        """Get the URL for the form's delete view."""
        return reverse(f"{url_prefix}form_delete", args=[self.id, self.slug])

    def get_edit_questions_url(self) -> str:
        """Get the URL for the form's questions edit view."""
        return reverse(
            f"{url_prefix}form_questions_edit",
            args=[self.id, self.slug],
        )

    def get_respond_url(self) -> str:
        """Get the URL to start filling out the form."""
        return reverse(f"{url_prefix}form_response", args=[self.id, self.slug])

    @classmethod
    def get_editable_forms(cls, user: _t.Optional[User]) -> QuerySet["Form"]:
        """Get the forms that the user can edit."""
        if not user or not user.is_authenticated:
            return cls.objects.none()
        return cls.objects.filter(Q(owner=user) | Q(editors=user))

    def is_live(self) -> bool:
        """Indicate if the form is live."""
        if not self.status == self.StatusChoices.ACTIVE:
            return False

        if self.end_dt and self.end_dt < timezone.now():
            return False

        if self.start_dt > timezone.now():
            return False

        return True

    @property
    def num_responses(self) -> int:
        """Get the number of responses for the form."""
        return self.responders.count()


class FormQuestion(models.Model):
    """A collection of questions for a form."""

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    field_type = models.CharField(
        max_length=32,
        choices=FieldTypeChoices.choices,
        default=FieldTypeChoices.TEXT,
    )
    question = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    required = models.BooleanField(default=False)
    seq_no = models.IntegerField(
        default=0,
        verbose_name="Order No.",
        help_text="Order of the questions.",
    )
    choices = models.TextField(
        blank=True,
        null=True,
        help_text="Separate choices with a pipe (|).",
    )
    related_question = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The question to use for the related question.",
    )

    class Meta:
        db_table = "fc_form_question"
        ordering = ["form", "seq_no"]
        unique_together = ["form", "question"]

    def __str__(self):
        return f"{self.form.title} - {self.question}"

    @property
    def choice_list(self) -> _t.List[str]:
        """Get the list of choices for the question."""
        return (self.choices or "").split("|")

    def clean(self, *args, **kwargs) -> None:
        """Ensure that fields that require choices are not blank and
        vice-versa.
        """
        super().clean(*args, **kwargs)
        _is_choice_field = is_choice_field(self.field_type)
        choices = (self.choices or "").strip()
        if _is_choice_field and not choices:
            raise ValidationError("This question field type requires choices.")
        if not _is_choice_field and choices:
            raise ValidationError(
                "This question field type does not support choices."
            )


class FormResponder(models.Model):
    """Represents a person responding to a form."""

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="responders",
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "fc_form_responder"
        ordering = ["-created_dt"]
        unique_together = ["form", "user"]

    def __str__(self):
        return f"{self.form.title} - {self.created_dt}"


class FormResponse(models.Model):
    """A response to a form."""

    form_responder = models.ForeignKey(
        FormResponder,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    question = models.ForeignKey(
        FormQuestion,
        on_delete=models.CASCADE,
    )
    answer = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "fc_form_response"
        ordering = ["form_responder", "question"]

    def __str__(self):
        return f"{self.form_responder.form.title} - {self.question.question}"
