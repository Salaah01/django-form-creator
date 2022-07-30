from rest_framework import serializers
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from .. import models as fc_models


class NestedElementSerializer(serializers.ModelSerializer):
    """Serializer for the content type model. The entire serializer is
    read-only.
    """

    class Meta:
        model = ContentType
        fields = "__all__"
        read_only_fields = [
            f.attname
            for f in ContentType._meta.get_fields()
            if not f.is_relation
        ]


class HTMLComponentSerializer(serializers.ModelSerializer):
    """Serializer for the `HTMLComponent` model."""

    seq_no = serializers.IntegerField()

    class Meta:
        model = fc_models.HTMLComponent
        fields = "__all__"


class FormQuestionSerializer(serializers.ModelSerializer):
    """Serializer for the `FormQuestion` model."""

    seq_no = serializers.IntegerField()

    class Meta:
        model = fc_models.FormQuestion
        fields = "__all__"


class FormElementOrderSerializer(serializers.ModelSerializer):
    """Serializer for the `FormElementOrder` model."""

    element = serializers.SerializerMethodField()
    element_type = NestedElementSerializer()

    class Meta:
        model = fc_models.FormElementOrder
        fields = "__all__"
        verbose_name = "Form Element Order"

    def get_element(self, obj):
        """Return the serialized element."""
        serializer = get_seq_no_model_serializer(obj.element.__class__)
        return serializer(obj.element).data

    def get_element_type_name(self, obj):
        """`element_type` is the content type ID, so we need to get the
        name.
        """

    @classmethod
    def for_form(cls, form_id: int) -> "FormElementOrderSerializer":
        form_element_orders = fc_models.FormElementOrder.objects.filter(
            form_id=form_id
        )
        return cls(form_element_orders, many=True)


class FormSerializer(serializers.ModelSerializer):
    """Serializer for the `Form` model."""

    form_elements = FormElementOrderSerializer(
        many=True,
        source="formelementorder_set",
    )
    url = serializers.URLField(source="get_absolute_url")

    class Meta:
        model = fc_models.Form
        fields = (
            "id",
            "slug",
            "url",
            "title",
            "description",
            "created_dt",
            "start_dt",
            "end_dt",
            "status",
            "form_elements",
        )


def get_seq_no_model_serializer(
    model_class: ModelBase,
) -> serializers.ModelSerializer:
    """Factory function to retrieve the serializer for a model class where
    the model class is a subclass of `SeqNoBaseModel`.

    :param model_class: The model class to retrieve the serializer for.
    :return: The serializer for the model instance.
    """
    if not issubclass(model_class, fc_models.SeqNoBaseModel):
        raise ValueError("`model_class` must be a subclass of SeqNoBaseModel")

    serializers = {
        fc_models.HTMLComponent: HTMLComponentSerializer,
        fc_models.FormQuestion: FormQuestionSerializer,
    }

    if model_class not in serializers:
        raise NotImplementedError("No serializer for `model_class`")

    return serializers[model_class]
