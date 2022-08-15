"""Tests for the `api.serializers` module."""

from types import SimpleNamespace
from model_bakery import baker
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from rest_framework import serializers
from form_creator import models as fc_models
from form_creator.api import serializers as api_serializers
from .. import baker_recipes


class TestNestedElementSerializer(TestCase):
    """Tests for `NestedElementSerializer`."""

    def test_validate_valid_attr(self):
        """Test the `validate` method where the attributes provided are
        valid.
        """
        attrs = {"id": ContentType.objects.first().id}
        api_serializers.NestedElementSerializer().validate(attrs)

    def test_validate_no_exist_ct(self):
        """Test that the `validate` method raises a `ValidationError` if the
        attrs provided do not correspond to an existing `ContentType`
        object.
        """
        with self.assertRaises(serializers.ValidationError):
            api_serializers.NestedElementSerializer().validate({"id": -1})

    def test_validate_key_error(self):
        """Test that the `validate` method raises a `ValidationError` if the
        attributes provided lead to a `KeyError`.
        """
        with self.assertRaises(serializers.ValidationError):
            api_serializers.NestedElementSerializer().validate({})


class TestGetSeqNoModelSerializer(TestCase):
    """Tests for the `get_seq_no_model_serializer` function."""

    def test_does_not_have_valid_subclass(self):
        """Test that when provided with a model class which does not have a
        valid subclass, the function raises a `ValueError`.
        """
        with self.assertRaises(ValueError):
            api_serializers.get_seq_no_model_serializer(ContentType)

    def test_gets_serializer(self):
        """Test that when provided with a model class which has a valid
        subclass, the function returns the correct serializer.
        """
        serializer = api_serializers.get_seq_no_model_serializer(
            fc_models.HTMLComponent
        )
        self.assertEqual(serializer, api_serializers.HTMLComponentSerializer)


class TestFormElementOrderSerializer(TestCase):
    """Tests for the `FormElementOrderSerializer`."""

    serializer = api_serializers.FormElementOrderSerializer

    def test_get_element(self):
        """Test that the `get_element` method returns a serialized element."""
        baker_recipes.html_component.make()
        serialized_data = self.serializer.get_element(
            fc_models.FormElementOrder.objects.first()
        )
        self.assertIsInstance(serialized_data, dict)

    def test_get_element_non_form_element_order_inst(self):
        """Test that the `get_element` method returns a serialized element when
        the object is not a `FormElementOrder` instance.
        """
        element = baker_recipes.html_component.make()
        serialized_data = self.serializer.get_element(element)
        self.assertIsInstance(serialized_data, dict)

    def test_get_element_non_element(self):
        """Test that the `get_element` method returns a serialized element when
        the `element` attribute in a `FormElementOrder` instance is `None`.
        """
        baker_recipes.html_component.make()
        form_element_order = fc_models.FormElementOrder.objects.first()
        form_element_order.element_id = 9999
        form_element_order.save()

        serialized_data = self.serializer.get_element(form_element_order)
        self.assertEqual(serialized_data, [])

    def test_for_form(self):
        """Test that a serializer is returned for a form."""
        form = baker.make(fc_models.Form)
        serializer = self.serializer.for_form(form.id).__class__
        self.assertEqual(serializer, serializers.ListSerializer)

    def test_to_internal_data(self):
        """Test that the `internal_data` adds all items to the validated
        data.
        """
        html_element = baker_recipes.html_component.make()
        ct = ContentType.objects.get_for_model(html_element)
        data = {
            "id": html_element.id,
            "element": {
                "seq_no": html_element.seq_no,
                "html": html_element.html,
            },
            "element_type": {
                "id": ct.id,
                "app_label": ct.app_label,
                "model": ct.model,
            },
        }
        validated_data = self.serializer().to_internal_value(data)

        self.assertEqual(validated_data.get("id"), data["id"])
        self.assertEqual(
            dict(validated_data.get("element", {})),
            data["element"],
        )
        self.assertEqual(
            dict(validated_data.get("element_type", {})),
            data["element_type"],
        )

    def test_validate_no_element(self):
        """Test that a validation error is raised when no element is
        provided.
        """
        with self.assertRaises(serializers.ValidationError):
            self.serializer().validate({"element_type": {}})

    def test_validate_no_element_type(self):
        """Test that a validation error is raised when no element type is
        provided.
        """
        with self.assertRaises(serializers.ValidationError):
            self.serializer().validate({"element": {}})

    def test_validate_passes(self):
        """Test that the `validate` method passes when the data is valid."""
        self.serializer().validate({"element": {}, "element_type": {}})

    def test_create(self):
        """Test the `create` method."""
        form = baker.make(fc_models.Form)
        data = {
            "element": {
                "form": form.id,
                "seq_no": 99,
                "html": "<h1><strong>Header 2</strong></h1>",
            },
            "element_type": {
                "app_label": "form_creator",
                "model": "htmlcomponent",
            },
            "form": form.id,
        }
        api_serializers.FormElementOrderSerializer.create(data)

        self.assertEqual(fc_models.FormElementOrder.objects.all().count(), 1)
        self.assertEqual(fc_models.HTMLComponent.objects.all().count(), 1)
        form_element_order = fc_models.FormElementOrder.objects.first()
        element = fc_models.HTMLComponent.objects.first()

        self.assertEqual(form_element_order.seq_no, 99)
        self.assertEqual(form_element_order.form, form)
        self.assertEqual(
            form_element_order.element_type,
            ContentType.objects.get_for_model(fc_models.HTMLComponent),
        )
        self.assertEqual(element.html, "<h1><strong>Header 2</strong></h1>")

    def test_create_invalid_data(self):
        """Test that the `create` method raises a `ValidationError` if the
        data provided is invalid.
        """
        data = {
            "element": {
                "form": "1",
            },
            "element_type": {
                "app_label": "form_creator",
                "model": "htmlcomponent",
            },
            "form": "1",
        }
        with self.assertRaises(serializers.ValidationError):
            api_serializers.FormElementOrderSerializer.create(data)

    def test_update(self):
        """Test that the `update` method updates the instance."""
        form = baker.make(fc_models.Form)
        html_component = baker_recipes.html_component.make(form=form)

        data = {
            "element": {
                "form": form.id,
                "seq_no": 99,
                "html": "updated",
            },
            "element_type": {
                "app_label": "form_creator",
                "model": "htmlcomponent",
            },
        }

        api_serializers.FormElementOrderSerializer().update(
            fc_models.FormElementOrder.objects.first(),
            data,
        )

        self.assertEqual(fc_models.HTMLComponent.objects.all().count(), 1)
        html_component = fc_models.HTMLComponent.objects.first()
        self.assertEqual(html_component.seq_no, 99)
        self.assertEqual(html_component.html, "updated")

    def test_update_invalid_data(self):
        """Test that the `update` method raises a `ValidationError` if the
        data provided is invalid.
        """
        form = baker.make(fc_models.Form)
        baker_recipes.html_component.make(form=form)

        data = {
            "element": {
                "form": form.id,
            },
            "element_type": {
                "app_label": "form_creator",
                "model": "htmlcomponent",
            },
        }

        with self.assertRaises(serializers.ValidationError):
            api_serializers.FormElementOrderSerializer().update(
                fc_models.FormElementOrder.objects.first(),
                data,
            )


class TestFormSerializer(TestCase):
    """Tests for the `FormSerializer` class."""

    serializer = api_serializers.FormSerializer

    def test_create_form(self):
        """Test that the `_create_form` method creates a form."""
        self_obj = SimpleNamespace(
            context={"request": SimpleNamespace(user=baker.make(User))}
        )
        form = self.serializer._create_form(self_obj, {"title": "Test"})

        # Test that the object has actually been created.
        self.assertEqual(fc_models.Form.objects.count(), 1)

        # Test that the object has the correct attributes.
        self.assertEqual(form.title, "Test")
        self.assertEqual(form.slug, "test")
        self.assertEqual(form.status, fc_models.Form.StatusChoices.DRAFT)
        self.assertIsNotNone(form.start_dt)

    def test_create_form_elements(self):
        """Test that the `create_form_elements` method is able to create an
        element.
        """
        form = baker.make(fc_models.Form)
        data = [
            {
                "element_type": {
                    "id": ContentType.objects.get_for_model(
                        fc_models.HTMLComponent
                    ).id
                },
                "element": {"html": "<h1>Component</h1>"},
            }
        ]

        created_objs = self.serializer._create_form_elements(form, data)

        self.assertEqual(len(created_objs), 1)
        self.assertEqual(fc_models.HTMLComponent.objects.count(), 1)

        created_obj = created_objs[0]

        self.assertEqual(fc_models.HTMLComponent.objects.get(), created_obj)
        self.assertEqual(created_obj.form, form)
        self.assertEqual(created_obj.html, "<h1>Component</h1>")

    def test_create(self):
        """Test that the `create` method creates a form along with form
        elements.
        """
        data = {
            "slug": "",
            "title": "with-form-elements",
            "start_dt": None,
            "end_dt": None,
            "status": None,
            "form_elements": [
                {
                    "element": {
                        "seq_no": 1,
                        "html": "<h1><strong>Header 2</strong></h1>",
                    },
                    "element_type": {
                        "app_label": "form_creator",
                        "model": "htmlcomponent",
                    },
                },
                {
                    "element": {
                        "seq_no": 2,
                        "field_type": "text",
                        "question": "q2",
                        "description": "",
                        "required": False,
                        "choices": "",
                    },
                    "element_type": {
                        "id": 1,
                        "app_label": "form_creator",
                        "model": "formquestion",
                    },
                },
            ],
        }

        form = self.serializer(
            context={"request": SimpleNamespace(user=baker.make(User))}
        ).create(data)

        self.assertEqual(fc_models.Form.objects.count(), 1)
        self.assertEqual(fc_models.Form.objects.get(), form)
