from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from model_bakery import baker
from .. import models as fc_models


User = get_user_model()


class TestForm(TestCase):
    """Test the Form model."""

    def test_str(self):
        """Test that the `__str__` method returns a string instance."""
        self.assertIsInstance(str(baker.make(fc_models.Form)), str)

    def test_can_edit_owner(self):
        """Test that the owner can edit the form."""
        form = baker.make(fc_models.Form, owner=baker.make(User))
        self.assertTrue(form.can_edit(form.owner))

    def test_can_edit_editors(self):
        """Test that editors can edit the form."""
        form = baker.make(
            fc_models.Form,
            editors=baker.make(User, _quantity=2),
        )
        self.assertTrue(form.can_edit(form.editors.first()))

    def test_can_edit_other(self):
        """Test that other users cannot edit the form."""
        form = baker.make(fc_models.Form)
        self.assertFalse(form.can_edit(baker.make(User)))

    def test_get_absolute_url(self):
        """Test that the `get_absolute_url` method returns a string
        instance.
        """
        self.assertIsInstance(
            baker.make(fc_models.Form).get_absolute_url(),
            str,
        )

    def test_save_slug(self):
        """Test that the `save` method sets the slug."""
        form = baker.make(fc_models.Form, title="Test Form", slug="")
        self.assertEqual(form.slug, "test-form")

    def test_is_live_is_live(self):
        """Test that the `is_live` method returns `True` when the form is
        live.
        """

        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=timezone.now() + timedelta(days=1),
        )
        self.assertTrue(form.is_live())

    def test_is_live_start_dt(self):
        """Test that the `is_live` returns the correct boolean when tweaking
        the start date.
        """

        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() + timedelta(days=1),
            end_dt=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(form.is_live())

    def test_is_live_end_dt(self):
        """Test that the `is_live` returns the correct boolean when tweaking
        the end date.
        """

        # End date in past
        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=timezone.now() - timedelta(days=1),
        )
        self.assertFalse(form.is_live())

        # No end date
        form.end_dt = None
        self.assertTrue(form.is_live())

    def test_is_live_status(self):
        """Test that the `is_live` returns the correct boolean when tweaking
        the status.
        """

        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.DRAFT,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(form.is_live())

    def test_get_editable_forms_anon_user(self):
        """Test that the `get_editable_forms` method returns an empty queryset
        for an anonymous user.
        """
        self.assertQuerysetEqual(fc_models.Form.get_editable_forms(None), [])
        self.assertQuerysetEqual(
            fc_models.Form.get_editable_forms(AnonymousUser()),
            [],
        )

    def test_get_editable_forms(self):
        """Test that the `get_editable_forms` method returns a queryset of
        forms that the user can edit.
        """
        user = baker.make(User)
        owned_form = baker.make(fc_models.Form, owner=user)
        editable_form = baker.make(fc_models.Form, editors=[user])
        baker.make(fc_models.Form)

        results = fc_models.Form.get_editable_forms(user)
        self.assertEqual(results.count(), 2)
        self.assertIn(owned_form, results)
        self.assertIn(editable_form, results)


class TestFormQuestion(TestCase):
    """Test the FormQuestion model."""

    def test_str(self):
        """Test that the `__str__` method returns a string instance."""
        self.assertIsInstance(str(baker.make(fc_models.FormQuestion)), str)


class TestFormResponder(TestCase):
    """Test the FormResponder model."""

    def test_str(self):
        """Test that the `__str__` method returns a string instance."""
        self.assertIsInstance(str(baker.make(fc_models.FormResponder)), str)


class TestFormResponse(TestCase):
    """Test the FormResponse model."""

    def test_str(self):
        """Test that the `__str__` method returns a string instance."""
        self.assertIsInstance(str(baker.make(fc_models.FormResponse)), str)
