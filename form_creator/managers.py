from django.db import models
from django.utils import timezone


class FormsQueryset(models.QuerySet):
    """QuerySet for the Form model."""

    def live(self):
        """Return only live forms."""
        now = timezone.now()
        # Ideally we would import the active status, but that would cause a
        # circular import.
        return (
            self.filter(status="active")
            .exclude(start_dt__gt=now)
            .exclude(end_dt__lt=now)
        )


class FormManager(models.Manager):
    """Manager for the Form model."""

    def live(self):
        """Return only live forms."""
        return self.get_queryset().live()

    def get_queryset(self):
        """Return a queryset for the Form model."""
        return FormsQueryset(self.model, using=self._db)
