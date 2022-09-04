from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet
from .. import models as fc_models
from . import serializers as fc_serializers


class FormViewSet(ModelViewSet):
    """Viewset for a `fc_models.Form` and its subsequent form elements."""

    serializer_class = fc_serializers.FormSerializer

    def get_queryset(self) -> QuerySet[fc_models.Form]:
        """Return a queryset of forms that the current user is able to edit."""
        return fc_models.Form.get_editable_forms(self.request.user)


class FormElementViewSet(ModelViewSet):
    """Viewset for adding a form element to a form."""

    serializer_class = fc_serializers.FormElementOrderSerializer

    def get_queryset(self) -> QuerySet[fc_models.FormElementOrder]:
        """Return a queryset of form elements that the current user is able to
        edit.
        """
        return fc_models.FormElementOrder.objects.filter(
            form_id__in=fc_models.Form.get_editable_forms(
                self.request.user
            ).values_list("id", flat=True)
        )


class HTMLComponentViewSet(ModelViewSet):
    """Viewset for `HTMLComponent`."""

    serializer_class = fc_serializers.HTMLComponentSerializer

    def get_queryset(self) -> QuerySet[fc_models.HTMLComponent]:
        """Return a queryset of HTML component elements that the current user
        is able to edit.
        """
        return fc_models.HTMLComponent.objects.filter(
            form_id__in=fc_models.Form.get_editable_forms(
                self.request.user
            ).values_list("id", flat=True)
        )


class FormQuestionViewSet(ModelViewSet):
    """Viewset for `FormQuestion`."""

    serializer_class = fc_serializers.FormQuestionSerializer

    def get_queryset(self) -> QuerySet[fc_models.FormQuestion]:
        """Return a queryset of form question elements that the current user is
        able to edit.
        """
        return fc_models.FormQuestion.objects.filter(
            form_id__in=fc_models.Form.get_editable_forms(
                self.request.user
            ).values_list("id", flat=True)
        )
