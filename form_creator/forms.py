from django import forms
from django.utils import timezone
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from . import models as fc_models


User = get_user_model()


class NewForm(forms.ModelForm):
    """Form for creating a new form."""

    class Meta:
        model = fc_models.Form
        fields = [
            "title",
            "description",
            "start_dt",
            "end_dt",
            "owner",
            "editors",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        editor_choices = kwargs.pop("editor_choices", None)
        super().__init__(*args, **kwargs)

        self._setup_datetime_fields()
        self._set_owner_field(user)
        self._set_editors_field(editor_choices)

    def _setup_datetime_fields(self) -> None:
        """Set the `start_dt` and `end_dt` to datetime fields and set the
        `start_dt` to the current time.
        """
        start_dt = self.fields["start_dt"]
        end_dt = self.fields["end_dt"]
        start_dt.initial = timezone.now()
        start_dt.widget = forms.DateTimeInput(attrs={"type": "datetime-local"})
        end_dt.widget = forms.DateTimeInput(attrs={"type": "datetime-local"})

    def _set_owner_field(self, user: User) -> None:
        """Set the owner of the form."""
        self.fields["owner"].initial = user

    def _set_editors_field(self, editor_choices: QuerySet[User]) -> None:
        """Set the editor choices for the form if provided, otherwise hide the
        field.
        """
        editors_field = self.fields["editors"]
        editors_field.required = False
        if editor_choices:
            editors_field.queryset = editor_choices
        else:
            editors_field.queryset = User.objects.none()
            editors_field.widget = forms.HiddenInput()


class DeleteForm(forms.ModelForm):
    """Form for deleting a form."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        model = fc_models.Form
        fields = ["id"]

    def clean(self) -> None:
        """Check if the user can delete the form."""
        if not self.instance.can_delete(self.user):
            raise forms.ValidationError("You cannot delete this form.")


class FormQuestionForm(forms.ModelForm):
    """Form for creating a new form question."""

    choices = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1}),
        required=False,
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    class Meta:
        model = fc_models.FormQuestion
        exclude = ["form"]

    def __init__(self, form_id: int, *args, **kwargs):
        self.form_id = form_id
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs) -> fc_models.FormQuestion:
        """Save the form question and set the form id."""
        self.instance.form_id = self.form_id
        return super().save(*args, **kwargs)
