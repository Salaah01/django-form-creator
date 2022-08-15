"""Tests for the `signals` module."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from .. import models as fc_models
from . import baker_recipes

User = get_user_model()


class TestOnSeqNoInstanceSaved(TestCase):
    """Tests for the `on_seq_no_instance_saved` signal."""

    def test_instance_created(self):
        """Test that a new instance of `FormElementOrder` is created when a new
        model instance inheriting from `SeqNoBaseModel` is created.
        """
        html_component = baker_recipes.html_component.make()
        self.assertEqual(fc_models.FormElementOrder.objects.count(), 1)
        self.assertEqual(
            fc_models.FormElementOrder.objects.first().element,
            html_component,
        )

    def test_instance_updated(self):
        """Test that the `FormElementOrder` instance is updated when a model
        instance inheriting from `SeqNoBaseModel` is updated.
        """
        html_component = baker_recipes.html_component.make(seq_no=5)
        html_component.seq_no = 10
        html_component.save()
        self.assertEqual(fc_models.FormElementOrder.objects.count(), 1)
        self.assertEqual(fc_models.FormElementOrder.objects.first().seq_no, 10)

    def test_no_related_instance_save(self):
        """Test that when a model instance which does not inherit from
        `SeqNoBaseModel` is saved, no `FormElementOrder` instance is created.
        """
        baker.make(User)
        self.assertFalse(fc_models.FormElementOrder.objects.exists())


class TestOnSeqNoInstanceDeleted(TestCase):
    """Tests for the `on_seq_no_instance_deleted` signal."""

    def test_instance_deleted(self):
        """Test that the `FormElementOrder` instance is deleted when a model
        instance inheriting from `SeqNoBaseModel` is deleted.
        """
        html_component = baker_recipes.html_component.make()
        self.assertEqual(fc_models.FormElementOrder.objects.count(), 1)
        html_component.delete()
        self.assertFalse(fc_models.FormElementOrder.objects.exists())
