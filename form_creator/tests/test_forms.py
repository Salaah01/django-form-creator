from django.test import TestCase
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from model_bakery import baker
from .. import forms as fc_forms, models as fc_models


User = get_user_model()


class TestNewForm(TestCase):
    def test_form_loads(self):
        """Test that the form actually loads."""
        baker.make(User, _quantity=2)
        editors = User.objects.all()
        owner = baker.make(User)
        form = fc_forms.NewForm(
            user=owner,
            editor_choices=editors,
        )

        self.assertEqual(form.fields["owner"].initial, owner)
        self.assertEqual(
            set(form.fields["editors"].queryset.values_list("id")),
            set(editors.values_list("id")),
        )

    def test_form_no_editors(self):
        """Test the form load with no editors."""
        form = fc_forms.NewForm(
            user=baker.make(User),
        )

        self.assertEqual(
            set(form.fields["editors"].queryset.values_list("id")),
            set(),
        )


class TestDeleteForm(TestCase):
    def test_form_loads(self):
        """Test that the form actually loads."""
        form = baker.make(fc_models.Form)
        fc_forms.DeleteForm(instance=form, user=form.owner)

    def test_clean_user(self):
        """Test that the `clean` method accepts a valid user."""

        form = baker.make(fc_models.Form)
        fc_forms.DeleteForm(instance=form, user=form.owner)
        form.clean_fields()

    def test_clean_user_invalid(self):
        """Test that the `clean` method rejects an invalid user."""

        with self.assertRaises(ValidationError):
            form = fc_forms.DeleteForm(
                instance=baker.make(fc_models.Form),
                user=baker.make(User),
            )
            form.clean()


class TestFormQuestionForm(TestCase):
    """Test the FormQuestionForm."""

    def test_init(self):
        """Test the initialiser ensuring that the form loads correctly."""
        form = fc_forms.FormQuestionForm(1)
        self.assertEqual(form.form_id, 1)

    def test_save_existing_form(self):
        """Test that an existing form saves correctly."""
        form_1_obj = baker.make(fc_models.Form, title="q1")
        form_2_obj = baker.make(fc_models.Form, title="q2")
        form_question_obj = baker.make(fc_models.FormQuestion, form=form_1_obj)
        form_question = fc_forms.FormQuestionForm(
            form_id=form_2_obj.id,
            data=form_question_obj.__dict__,
        )
        form_question.is_valid()
        saved_obj = form_question.save()
        self.assertEqual(saved_obj.form, form_2_obj)

    def test_save_new_form(self):
        """Test that a new form saves correctly."""
        form_obj = baker.make(fc_models.Form, title="q1")
        form = fc_forms.FormQuestionForm(
            form_id=form_obj.id,
            initial={
                "question": "q1",
            },
        )
        form.is_valid()
        form.save()
        self.assertEqual(fc_models.FormQuestion.objects.count(), 1)
