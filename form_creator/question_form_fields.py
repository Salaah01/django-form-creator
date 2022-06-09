from django import forms
from django.db import models


class FieldTypeChoices(models.TextChoices):
    """The type of field."""

    TEXT = "text", "Text"
    TEXTAREA = "textarea", "Textarea"
    EMAIL = "email", "Email"
    INTEGER = "integer", "Integer"
    DECIMAL = "decimal", "Decimal"
    FLOAT = "float", "Float"
    BOOLEAN = "boolean", "Boolean"
    DATE = "date", "Date"
    DATETIME = "datetime", "DateTime"
    TIME = "time", "Time"
    URL = "url", "URL"
    CHOICE = "choice", "Choice"
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"


field_type_map = {
    FieldTypeChoices.TEXT: forms.CharField,
    FieldTypeChoices.TEXTAREA: forms.CharField,
    FieldTypeChoices.EMAIL: forms.EmailField,
    FieldTypeChoices.INTEGER: forms.IntegerField,
    FieldTypeChoices.DECIMAL: forms.DecimalField,
    FieldTypeChoices.FLOAT: forms.FloatField,
    FieldTypeChoices.BOOLEAN: forms.BooleanField,
    FieldTypeChoices.DATE: forms.DateField,
    FieldTypeChoices.DATETIME: forms.DateTimeField,
    FieldTypeChoices.TIME: forms.TimeField,
    FieldTypeChoices.URL: forms.URLField,
    FieldTypeChoices.CHOICE: forms.ChoiceField,
    FieldTypeChoices.MULTIPLE_CHOICE: forms.MultipleChoiceField,
}
