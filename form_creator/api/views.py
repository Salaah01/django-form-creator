from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request
from rest_framework.response import Response
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

   
