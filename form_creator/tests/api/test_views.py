from types import SimpleNamespace
from model_bakery import baker
from django.test import TestCase
from django.contrib.auth.models import User
from form_creator import models as fc_models
from form_creator.api import views as api_views
from .. import baker_recipes


class TestFormViewSet(TestCase):
    """Tests for `FormViewSet`."""

    def test_get_queryset(self):
        """Test that the queryset is filtered to only include forms the user
        can edit.
        """
        user = baker.make(User)
        baker.make(fc_models.Form, _quantity=2, owner=user)
        baker.make(fc_models.Form, _quantity=2)
        viewset = api_views.FormViewSet()
        viewset.request = SimpleNamespace(user=user)
        queryset = viewset.get_queryset()
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset[0].owner, user)


class TestFormElementViewSet(TestCase):
    """Tests for `FormElementViewSet`."""

    def test_get_queryset(self):
        """Test that the queryset is filtered to only include form elements the
        user can edit.
        """
        user = baker.make(User)
        user_form = baker.make(fc_models.Form, owner=user)
        baker.make(fc_models.Form, _quantity=2)
        baker_recipes.html_component.make(form=user_form, _quantity=2)

        viewset = api_views.FormElementViewSet()
        viewset.request = SimpleNamespace(user=user)
        queryset = viewset.get_queryset()
        self.assertEqual(queryset.count(), 2)
