from django.test import TestCase
from django.contrib.auth import get_user_model
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
            fc_models.Form, editors=baker.make(User, _quantity=2)
        )
        self.assertTrue(form.can_edit(form.editors.first()))

    def test_can_edit_other(self):
        """Test that other users cannot edit the form."""
        form = baker.make(fc_models.Form)
        self.assertFalse(form.can_edit(baker.make(User)))

    # def test_get_absolute_url(self):
    #     """Test that the `get_absolute_url` method returns a string instance.
    #     """
    #     self.assertIsInstance(
    #         baker.make(fc_models.Form).get_absolute_url(), str,
    #     )


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
