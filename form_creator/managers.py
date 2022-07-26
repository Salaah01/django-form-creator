from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


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


class FormElementOrderManager(models.Manager):
    """Manager for the "FormElementOrder" model."""

    def create_or_update_from_element(
        self,
        element: models.Model,
    ) -> models.Model:
        """Create or update a FormElementOrder from an element."""
        return self.get_or_create(
            form=element.form,
            element_type=ContentType.objects.get_for_model(element),
            element_id=element.id,
            defaults={"seq_no": element.seq_no},
        )[0]

    def delete_element(self, element: models.Model) -> tuple:
        """Delete a FormElementOrder from an element."""
        return self.filter(
            form=element.form,
            element_type=ContentType.objects.get_for_model(element),
            element_id=element.id,
        ).delete()
