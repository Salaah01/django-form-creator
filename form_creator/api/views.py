from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .. import models as fc_models
from . import serializers as fc_serializers


class FormViewSet(ModelViewSet):
    """Viewset for a `fc_models.Form` and its subsequent form elements."""

    serializer_class = fc_serializers.FormSerializer

    def get_queryset(self) -> QuerySet[fc_models.Form]:
        """Return a queryset of forms that the current user is able to edit."""
        return fc_models.Form.get_editable_forms(self.request.user)
