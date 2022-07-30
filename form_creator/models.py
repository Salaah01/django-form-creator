import typing as _t
from functools import lru_cache
from django import dispatch
from django.apps import apps
from django.db import models, transaction
from django.db.models import Q, QuerySet
from django.db.models.base import ModelBase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .third_party.ckeditor.fields import RichTextField
from . import checks
from .question_form_fields import FieldTypeChoices, is_choice_field
from .managers import FormManager, FormElementOrderManager

User = get_user_model()
URL_PREFIX = "form_creator:"


SEQ_NO_INSTANCE_SAVED = dispatch.Signal()
SEQ_NO_INSTANCE_DELETED = dispatch.Signal()


# Note: The following manager is defined here and not the managers.py file as
# it depends on the models defined here. This is a workaround to avoid circular
# imports.


class SeqNoManager(models.Manager):
    """Manager for that attaches the `seq_no` property to the model."""

    @staticmethod
    def _ready_check() -> bool:
        """Returns True of the custom manager is ready to be used."""
        return checks.is_content_types_loaded()

    def get_queryset(self):
        if not self._ready_check():
            return super().get_queryset()

        qs = super().get_queryset()
        object_type = ContentType.objects.get_for_model(qs.model)
        return qs.annotate(
            seq_no=models.Subquery(
                FormElementOrder.objects.filter(
                    element_type=object_type,
                    element_id=models.OuterRef("id"),
                )
                .values_list("seq_no", flat=True)
                .order_by("seq_no"),
                output_field=models.IntegerField(),
            )
        )


class SeqNoBaseModel(models.Model):
    """Base model for models that have a `seq_no` field."""

    objects = SeqNoManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        seq_no = kwargs.pop("seq_no", None)
        super().__init__(*args, **kwargs)
        self.seq_no = seq_no

    def __lt__(self, other: models.Model):
        return self.seq_no < other.seq_no

    def clean(self):
        """The `seq_no` needs to be populated in the `FormElementOrder` model.
        Therefore, run its validation here.
        """
        super().clean()

        # If the seq_no is not provided, then it will be automatically
        # generated and thus we don't need to validate it.
        if self.seq_no is None:
            return

        content_type = ContentType.objects.get_for_model(self)

        # If this record already exists and the seq_no is the same, then
        # pass the validation.
        if (
            self.pk
            and FormElementOrder.objects.filter(
                form_id=self.form_id,
                element_type=content_type,
                element_id=self.id,
                seq_no=self.seq_no,
            ).exists()
        ):
            return

        # We can now validate the seq_no as by reaching this point, the user
        # is either changing the seq_no or creating a new record.
        FormElementOrder(
            form_id=self.form_id,
            element_type=ContentType.objects.get_for_model(self),
            element_id=1,  # Dummy value (actual value doesn't exist yet).
            seq_no=self.seq_no,
        ).full_clean()

    def save(self, seq_no: _t.Optional[int] = None, *args, **kwargs):
        """Saves the model and raises an signal to update the seq_no."""
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.seq_no = (
                self.seq_no
                or seq_no
                or FormElementOrder.form_next_seq_no(self.form_id)
            )
            SEQ_NO_INSTANCE_SAVED.send(sender=self.__class__, instance=self)

    def delete(self, *args, **kwargs):
        """Deletes the model and raises an signal to update the seq_no."""
        SEQ_NO_INSTANCE_DELETED.send(sender=self.__class__, instance=self)
        return super().delete(*args, **kwargs)

    @classmethod
    @lru_cache(maxsize=1)
    def inherited_models(cls) -> _t.List[ModelBase]:
        """Get the inherited models of the current model."""
        return set(
            model for model in apps.get_models() if issubclass(model, cls)
        )


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
        help_text="This form will be available to users only when status is "
        "active and the current date is between the start and end dates.",
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

    def can_edit(self, user: User, staff_can_edit: bool = True) -> bool:
        """Check if the user can edit the form.
        :param user: The user to check.
        :param staff_can_edit: Whether staff can edit the form.
        :return: True if the user can edit the form.
        """
        if not user or not user.is_authenticated:
            return False
        return any(
            [
                staff_can_edit and user.is_staff,
                user.username == self.owner.username,
                user in self.editors.all(),
            ]
        )

    def can_delete(self, user: User) -> bool:
        """Check if the user can delete the form.
        :param user: The user to check.
        :return: True if the user can delete the form.
        """
        if not user or not user.is_authenticated:
            return False
        return any([user.is_staff, user.username == self.owner.username])

    def completed_by(self, user: User) -> _t.Optional["FormResponder"]:
        """Get the form responder for the user.
        :param user: The user to check.
        :return: The form responder for the user.
        """
        if not user or not user.is_authenticated:
            return None
        return self.responders.filter(user=user).first()

    def can_complete_form(self, user: User) -> bool:
        """Check if the user can complete the form.
        :param user: The user to check.
        :return: True if the user can complete the form.
        """
        if not user or not user.is_authenticated:
            return False

        if not self.is_live():
            return False

        # We set the `staff_can_edit` to false as we want staff to be able to
        # complete the forms.
        if self.can_edit(user, False):
            return False

        return not bool(self.completed_by(user))

    def get_absolute_url(self) -> str:
        """Get the absolute URL for the form."""
        return reverse(f"{URL_PREFIX}form_detail", args=[self.id, self.slug])

    def get_edit_url(self) -> str:
        """Get the URL for the form's edit view."""
        return reverse(f"{URL_PREFIX}form_edit", args=[self.id, self.slug])

    def get_delete_url(self) -> str:
        """Get the URL for the form's delete view."""
        return reverse(f"{URL_PREFIX}form_delete", args=[self.id, self.slug])

    def get_edit_questions_url(self) -> str:
        """Get the URL for the form's questions edit view."""
        return reverse(
            f"{URL_PREFIX}form_questions_edit",
            args=[self.id, self.slug],
        )

    def get_respond_url(self) -> str:
        """Get the URL to start filling out the form."""
        return reverse(f"{URL_PREFIX}form_response", args=[self.id, self.slug])

    @classmethod
    def get_editable_forms(cls, user: _t.Optional[User]) -> QuerySet["Form"]:
        """Get the forms that the user can edit.
        :param user: The user to check.
        :return: The forms that the user can edit.
        """
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


class FormElementOrder(models.Model):
    """The ordering of form elements."""

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
    )
    element_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    element_id = models.PositiveIntegerField()
    seq_no = models.PositiveIntegerField(
        verbose_name="Sequence number",
        help_text="The order in which the element is displayed (ordered "
        "in ascending order)",
    )

    objects = FormElementOrderManager()

    class Meta:
        db_table = "fc_form_element_order"
        ordering = ("-form_id", "seq_no")
        unique_together = (
            "form",
            "seq_no",
        )

    def __str__(self):
        return f"{self.form} - {self.element_type} - {self.element_id}"

    def __lt__(self, other: models.Model):
        return self.seq_no < other.seq_no

    @classmethod
    def form_max_seq_no(cls, form_id: int) -> int:
        """Get the maximum sequence number for the form.
        :param form_id: The ID of the form.
        """
        latest_inst = (
            cls.objects.filter(form_id=form_id).order_by("-seq_no").first()
        )
        return latest_inst and latest_inst.seq_no or 0

    @classmethod
    def form_next_seq_no(cls, form_id: int) -> int:
        """Get the next sequence number for the form.
        :param form_id: The ID of the form.
        """
        return cls.form_max_seq_no(form_id) + 10

    @property
    def element(self) -> _t.Union[models.Model]:
        """Get the element if"""
        return (
            self.element_type.model_class()
            .objects.filter(id=self.element_id)
            .first()
        )


class HTMLComponent(SeqNoBaseModel):
    """Represents additional HTML components that can be added to form page."""

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    html = RichTextField(verbose_name="HTML")

    class Meta:
        db_table = "fc_html_component"
        verbose_name = "HTML Component"
        verbose_name_plural = "HTML Components"

    def __str__(self):
        return self.html


class FormQuestion(SeqNoBaseModel):
    """A collection form questions for a form."""

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
        ordering = ["form"]
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
