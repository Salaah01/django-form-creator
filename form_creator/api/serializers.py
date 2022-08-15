import typing as _t
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers
from .. import models as fc_models
from ..utils import get_content_type_from_dict


class OptionalFieldsMixin:
    """A mixin to support the setting of optional fields in a serializer."""

    def __init__(self, *args, **kwargs) -> None:
        self._set_not_required_fields()
        super().__init__(*args, **kwargs)

    def _set_not_required_fields(self) -> None:
        for opt_field in self.Meta.optional_fields:
            field = self.fields[opt_field]
            field.required = False
            field.allow_null = True
            field.allow_blank = True


class NestedElementSerializer(serializers.Serializer, OptionalFieldsMixin):
    """Serializer for the content type model. The entire serializer is
    read-only.
    """

    id = serializers.IntegerField(required=False)
    app_label = serializers.CharField()
    model = serializers.CharField()

    class Meta:
        model = ContentType
        fields = "__all__"
        optional_fields = ("id", "app_label", "model")

    def validate(self, attrs):
        try:
            get_content_type_from_dict(attrs)
            return super().validate(attrs)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(
                f"The content type does not exist. (You provided: {attrs})"
            )
        except KeyError:
            raise serializers.ValidationError(
                "You must provide either a content type id or an app_label"
                "and model."
            )


class HTMLComponentSerializer(
    OptionalFieldsMixin,
    serializers.ModelSerializer,
):
    """Serializer for the `HTMLComponent` model."""

    seq_no = serializers.IntegerField()

    class Meta:
        model = fc_models.HTMLComponent
        fields = "__all__"
        optional_fields = ("seq_no",)


class FormQuestionSerializer(serializers.ModelSerializer):
    """Serializer for the `FormQuestion` model."""

    seq_no = serializers.IntegerField()

    class Meta:
        model = fc_models.FormQuestion
        fields = "__all__"


class FormElementOrderSerializer(
    OptionalFieldsMixin,
    serializers.ModelSerializer,
):
    """Serializer for the `FormElementOrder` model."""

    element = serializers.SerializerMethodField()
    element_type = NestedElementSerializer()

    class Meta:
        model = fc_models.FormElementOrder
        fields = "__all__"
        verbose_name = "Form Element Order"
        optional_fields = (
            "element_id",
            "seq_no",
            "form",
        )

    def validate(self, attrs):
        """Validate the element field."""
        if "element" not in attrs:
            raise serializers.ValidationError(
                "You must provide an element field."
            )
        if "element_type" not in attrs:
            raise serializers.ValidationError(
                "You must provide an element_type field."
            )
        return super().validate(attrs)

    @staticmethod
    def create(validated_data: dict) -> fc_models.FormElementOrder:
        """Create a new form element order."""
        ct = get_content_type_from_dict(validated_data["element_type"])
        model = ct.model_class()
        serializer_class = get_seq_no_model_serializer(model)
        serializer = serializer_class(data=validated_data["element"])
        if serializer.is_valid():
            return serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

    @staticmethod
    def update(
        instance: fc_models.FormElementOrder,
        validated_data: dict,
    ):
        """Update an existing form element order."""
        ct = get_content_type_from_dict(validated_data["element_type"])
        model = ct.model_class()
        serializer_class = get_seq_no_model_serializer(model)
        serializer = serializer_class(
            instance.element,
            data=validated_data["element"],
        )
        if serializer.is_valid():
            serializer.save()
            instance.refresh_from_db()
            return instance
        else:
            raise serializers.ValidationError(serializer.errors)

    @staticmethod
    def get_element(obj):
        """Return the serialized element."""
        if isinstance(obj, fc_models.FormElementOrder):
            if obj.element is None:
                return []
            serializer = get_seq_no_model_serializer(obj.element.__class__)
            return serializer(obj.element).data
        else:
            serializer = get_seq_no_model_serializer(obj.__class__)
            return serializer(obj).data

    @classmethod
    def for_form(cls, form_id: int) -> "FormElementOrderSerializer":
        form_element_orders = fc_models.FormElementOrder.objects.filter(
            form_id=form_id
        )
        return cls(form_element_orders, many=True)

    def to_internal_value(self, data: dict):
        """Certain fields are not excluded in the validated data because they
        are non-model fields. This method will include those fields.
        """
        internal_value = super().to_internal_value(data)
        internal_value.update(
            {"id": data.get("id", None), "element": data.get("element", {})}
        )
        return internal_value


class FormSerializer(OptionalFieldsMixin, serializers.ModelSerializer):
    """Serializer for the `Form` model."""

    form_elements = FormElementOrderSerializer(
        many=True,
        required=False,
        allow_null=True,
    )
    url = serializers.URLField(source="get_absolute_url", read_only=True)

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
        optional_fields = (
            "slug",
            "description",
            "start_dt",
            "end_dt",
            "status",
            "form_elements",
        )

    def create(self, validated_data):
        """Create a new form."""
        form_elements = validated_data.pop("form_elements")
        with transaction.atomic():
            form = self._create_form(validated_data)
            self._create_form_elements(form, form_elements)
        return form

    def _create_form(self, validated_data: dict) -> fc_models.Form:
        """Creates a form from the validated data and returns the newly created
        form.
        """
        return fc_models.Form.objects.create(
            **validated_data,
            owner=self.context["request"].user,
        )

    @staticmethod
    def _create_form_elements(
        form: fc_models.Form,
        form_elements: _t.List[dict],
    ) -> _t.List[fc_models.SeqNoBaseModel]:
        """Creates the form elements from the `form_elements` and returns a
        list of newly created form elements.
        """
        created_objs = []
        for form_element in form_elements:
            ct = get_content_type_from_dict(form_element["element_type"])
            element = ct.model_class().objects.create(
                **form_element["element"],
                form=form,
            )
            created_objs.append(element)
        return created_objs


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

    # Note: This is ignored in the coverage test as the only way to test this
    # is to dynamically create a new model which inherits from
    # `SeqNoBaseModel`. This is achievable, however, I have seen this to cause
    # issues in subsequent tests in other projects.
    if model_class not in serializers:  # pragma: no cover
        raise NotImplementedError("No serializer for `model_class`")

    return serializers[model_class]
