"""Overrides default form fields."""

from django import forms


class DateField(forms.DateField):
    """A date field."""

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.DateInput(attrs={"type": "date"})
        super().__init__(*args, **kwargs)


class DateTimeField(forms.DateTimeField):
    """A datetime field."""

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
        super().__init__(*args, **kwargs)


class TimeField(forms.TimeField):
    """A time field."""

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.TimeInput(attrs={"type": "time"})
        super().__init__(*args, **kwargs)
