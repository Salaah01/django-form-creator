"""Tests for the `question_form_fields` module."""

from django.test import SimpleTestCase
from .. import question_form_fields


class TestIsChoiceField(SimpleTestCase):
    """Tests for the `is_choice_field` function."""

    def test_is_choice_field(self):
        """Test that the function returns True for the choice fields."""
        self.assertTrue(question_form_fields.is_choice_field("choice"))
        self.assertTrue(
            question_form_fields.is_choice_field("multiple_choice"),
        )

    def test_is_not_choice_field(self):
        """Test that the function returns False for non choice fields."""
        for field in question_form_fields.FieldTypeChoices:
            if field not in ("choice", "multiple_choice"):
                self.assertFalse(
                    question_form_fields.is_choice_field(field),
                    f"{field} is a choice field.",
                )
