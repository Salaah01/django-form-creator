from django.test import TestCase
from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from model_bakery import baker
from .. import forms as fc_forms, models as fc_models
from ..question_form_fields import FieldTypeChoices

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


class TestCaptureResponseForm(TestCase):
    """Test the CaptureResponseForm."""

    @classmethod
    def setUpTestData(cls):
        """Set up the test data."""
        cls.form = baker.make(fc_models.Form)
        cls.text_q = baker.make(fc_models.FormQuestion, form=cls.form)
        cls.choice_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            field_type=FieldTypeChoices.CHOICE,
            choices="a|b|c",
        )

    def test_init(self):
        """Test the initialiser ensuring that the form loads correctly."""
        form = fc_forms.CaptureResponseForm(self.form)
        self.assertEqual(form.form, self.form)

    def test_loads_fields(self):
        """Test that the form loads the correct fields."""
        form = fc_forms.CaptureResponseForm(self.form)
        self.assertEqual(len(form.fields), 2)

        text_q_field = form.fields["question_%s" % self.text_q.id]
        choice_q_field = form.fields["question_%s" % self.choice_q.id]

        self.assertEqual(text_q_field.label, self.text_q.question)
        self.assertEqual(choice_q_field.label, self.choice_q.question)

        self.assertIsInstance(text_q_field.widget, forms.TextInput)
        self.assertIsInstance(choice_q_field.widget, forms.Select)

    def test_load_choices(self):
        """Test that form loads the choices correctly for the choice field."""
        form = fc_forms.CaptureResponseForm(self.form)
        choice_q_field = form.fields["question_%s" % self.choice_q.id]
        self.assertEqual(
            choice_q_field.widget.choices,
            [("a", "a"), ("b", "b"), ("c", "c")],
        )

    def test_save(self):
        """Test that the form saves correctly."""
        form = fc_forms.CaptureResponseForm(
            self.form,
            data={
                "question_%s" % self.text_q.id: "q1",
                "question_%s" % self.choice_q.id: "a",
            },
        )
        form.is_valid()

        form_response = form.save(baker.make(User))

        self.assertEqual(fc_models.FormResponder.objects.count(), 1)
        self.assertEqual(
            fc_models.FormResponder.objects.first(),
            form_response,
        )
        self.assertEqual(form_response.responses.count(), 2)
        self.assertEqual(
            set(
                form_response.responses.all().values_list(
                    "question_id", flat=True
                )
            ),
            {self.text_q.id, self.choice_q.id},
        )
        self.assertEqual(
            form_response.responses.get(question=self.text_q).answer,
            "q1",
        )
        self.assertEqual(
            form_response.responses.get(question=self.choice_q).answer,
            "a",
        )
