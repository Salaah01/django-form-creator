"""Tests for the `form_creator_tags` module."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from .. import models as fc_models
from ..templatetags import form_creator_tags


User = get_user_model()


class TestCanEditForm(TestCase):
    """Tests for the `can_edit_form` filter."""

    def setUp(self):
        self.user = baker.make(User)
        self.form = baker.make(fc_models.Form)

    def test_can_edit_form_true(self):
        """Test that the filter returns True when the user is the owner."""
        self.form.owner = self.user
        self.form.save()
        self.assertTrue(form_creator_tags.can_edit_form(self.form, self.user))

    def test_can_edit_form_false(self):
        """Test that the filter returns False when the user is not the
        owner.
        """
        self.assertFalse(form_creator_tags.can_edit_form(self.form, self.user))


class TestCanDeleteForm(TestCase):
    """Tests for the `can_delete_form` filter."""

    def setUp(self):
        self.user = baker.make(User)
        self.form = baker.make(fc_models.Form)

    def test_can_delete_form_true(self):
        """Test that the filter returns True when the user is the owner."""
        self.form.owner = self.user
        self.form.save()
        self.assertTrue(
            form_creator_tags.can_delete_form(self.form, self.user)
        )

    def test_can_delete_form_false(self):
        """Test that the filter returns False when the user is not the
        owner.
        """
        self.assertFalse(
            form_creator_tags.can_delete_form(self.form, self.user)
        )


class TestCanCompleteForm(TestCase):
    """Tests for the `can_complete_form` filter."""

    def setUp(self):
        self.user = baker.make(User)
        self.form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
        )

    def test_can_complete_form_true(self):
        """Test that the filter returns True when the user is the owner."""
        self.assertTrue(
            form_creator_tags.can_complete_form(self.form, self.user)
        )

    def test_can_complete_form_false(self):
        """Test that the filter returns False when the user is not the
        owner.
        """
        self.form.owner = self.user
        self.form.save()
        self.assertFalse(
            form_creator_tags.can_complete_form(self.form, self.user)
        )


class TestFormCompletedOn(TestCase):
    """Tests for the `form_completed_on` filter."""

    def setUp(self):
        self.user = baker.make(User)
        self.form = baker.make(fc_models.Form)

    def test_form_not_completed(self):
        """Test that the filter returns an empty string when the form is not
        completed.
        """
        self.assertEqual(
            form_creator_tags.form_completed_on(self.form, self.user),
            "",
        )

    def test_form_completed(self):
        """Test that the filter returns a string representation of a date
        when the form is completed.
        """
        responder = baker.make(
            fc_models.FormResponder, form=self.form, user=self.user
        )
        self.assertEqual(
            form_creator_tags.form_completed_on(self.form, self.user),
            responder.created_dt.strftime("%Y-%m-%d"),
        )
