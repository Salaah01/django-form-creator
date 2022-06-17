from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from model_bakery import baker
from .. import models as fc_models
from ..question_form_fields import FieldTypeChoices


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

    def test_can_edit_anon_user(self):
        """Test that the `can_edit` method returns `False` for an anonymous
        user.
        """
        form = baker.make(fc_models.Form)
        self.assertFalse(form.can_edit(AnonymousUser()))

    def test_completed_by(self):
        """Test that the `completed_by` method returns the correct instance of
        `FormResponder`.
        """
        form = baker.make(fc_models.Form)
        user = baker.make(User)
        form_responder = baker.make(
            fc_models.FormResponder,
            form=form,
            user=user,
        )
        baker.make(fc_models.FormResponder, form=form)
        self.assertEqual(form.completed_by(user), form_responder)

    def test_completed_by_not_completed(self):
        """Test that the `completed_by` method returns `None` when the user
        has not completed the form.
        """
        user = baker.make(User)
        form = baker.make(fc_models.Form)
        baker.make(fc_models.FormResponder, form=form)
        self.assertIsNone(form.completed_by(user))

    def test_completed_by_none_user(self):
        """Test that the `completed_by` method returns `None` when the user
        is `None`.
        """
        form = baker.make(fc_models.Form)
        self.assertIsNone(form.completed_by(None))

    def test_can_complete_form(self):
        """Test that the `can_complete_form` method returns the correct
        boolean.
        """
        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
        )
        user = baker.make(User)
        self.assertTrue(form.can_complete_form(user))

    def test_can_complete_form_not_live(self):
        """Test that the `can_complete_form` method returns the correct
        boolean when the form is not live.
        """
        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.DRAFT,
        )
        user = baker.make(User)
        self.assertFalse(form.can_complete_form(user))

    def test_can_complete_form_editor(self):
        """Test that the `can_complete_form` method returns the correct
        boolean for an editor.
        """
        user = baker.make(User)
        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
        )
        form.editors.add(user)
        self.assertFalse(form.can_complete_form(user))

    def test_can_complete_form_completed(self):
        """Test that the `can_complete_form` method returns the correct
        boolean when the form is completed by the user.
        """
        form = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
        )
        user = baker.make(User)
        baker.make(fc_models.FormResponder, form=form, user=user)
        self.assertFalse(form.can_complete_form(user))

    def test_can_complete_form_anon_user(self):
        """Test that the `can_complete_form` method returns `False` for an
        anonymous user.
        """
        form = baker.make(fc_models.Form)
        self.assertFalse(form.can_complete_form(AnonymousUser()))

    def test_get_absolute_url(self):
        """Test that the `get_absolute_url` method returns a string
        instance.
        """
        self.assertIsInstance(
            baker.make(fc_models.Form).get_absolute_url(),
            str,
        )

    def test_get_edit_url(self):
        """Test that the `get_edit_url` method returns a string instance."""
        self.assertIsInstance(
            baker.make(fc_models.Form).get_edit_url(),
            str,
        )

    def test_get_delete_url(self):
        """Test that the `get_delete_url` method returns a string instance."""
        self.assertIsInstance(
            baker.make(fc_models.Form).get_delete_url(),
            str,
        )

    def test_get_edit_questions_url(self):
        """Test that the `get_edit_questions_url` method returns a string
        instance.
        """
        self.assertIsInstance(
            baker.make(fc_models.Form).get_edit_questions_url(),
            str,
        )

    def test_get_respond_url(self):
        """Test that the `get_respond_url` method returns a string instance."""
        self.assertIsInstance(
            baker.make(fc_models.Form).get_respond_url(),
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

    def test_can_delete_anon_user(self):
        """Test that the `can_delete` method returns `False` for an
        anonymous user.
        """
        self.assertFalse(baker.make(fc_models.Form).can_delete(None))
        self.assertFalse(
            baker.make(fc_models.Form).can_delete(AnonymousUser())
        )

    def test_can_delete(self):
        """Test that the `can_delete` method returns `True` for the
        owner.
        """
        form = baker.make(fc_models.Form, owner=baker.make(User))
        self.assertTrue(form.can_delete(form.owner))

    def test_num_responses(self):
        """Test that the `num_responses` method returns the correct
        number of responses.
        """
        form = baker.make(fc_models.Form)
        baker.make(fc_models.FormResponder, form=form)
        baker.make(fc_models.FormResponder, form=form)
        self.assertEqual(form.num_responses, 2)


class TestFormQuestion(TestCase):
    """Test the FormQuestion model."""

    def test_str(self):
        """Test that the `__str__` method returns a string instance."""
        self.assertIsInstance(str(baker.make(fc_models.FormQuestion)), str)

    def test_choice_list(self):
        """Test that the `choice_list` method returns a list of choices."""
        form = baker.make(fc_models.FormQuestion, choices="a|b")
        self.assertEqual(form.choice_list, ["a", "b"])

    def test_clean_no_choice(self):
        """Test that the `clean` method raises an error when there are no
        choices but a field type requiring choices is selected.
        """
        form = baker.make(
            fc_models.FormQuestion,
            field_type=FieldTypeChoices.CHOICE,
            choices="",
        )
        with self.assertRaises(ValidationError):
            form.clean()

    def test_clean_non_choice_field(self):
        """Test that the `clean` method raises an error when there are choices
        but a field type not requiring choices is selected.
        """
        form = baker.make(
            fc_models.FormQuestion,
            field_type=FieldTypeChoices.TEXT,
            choices="a|b",
        )
        with self.assertRaises(ValidationError):
            form.clean()


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
