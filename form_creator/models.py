from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from .question_form_fields import FieldTypeChoices


User = get_user_model()


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

    class Meta:
        db_table = "fc_form"
        ordering = ["-created_dt"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save method to set the slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def can_edit(self, user: User) -> bool:
        """Check if the user can edit the form."""
        return user == self.owner or user in self.editors.all()

    def get_absolute_url(self):
        """Get the absolute URL for the form."""
        return reverse("form_creator:form_detail", args=[self.id, self.slug])


class FormQuestion(models.Model):
    """A collection of questions for a form."""

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    field_type = models.CharField(
        max_length=32,
        choices=FieldTypeChoices.choices,
        default=FieldTypeChoices.TEXT,
    )
    question = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    required = models.BooleanField(default=False)
    seq_no = models.IntegerField(default=0)
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

    def __str__(self):
        return f"{self.form.title} - {self.question}"


class FormResponder(models.Model):
    """Represents a person responding to a form."""

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=150)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "fc_form_responder"
        ordering = ["-created_dt"]

    def __str__(self):
        return f"{self.form.title} - {self.created_dt}"


class FormResponse(models.Model):
    """A response to a form."""

    form_responder = models.ForeignKey(
        FormResponder,
        on_delete=models.CASCADE,
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
