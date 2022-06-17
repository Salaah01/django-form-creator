"""Tests for the `admin` module."""

from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse
from model_bakery import baker
from .. import admin as fc_admin, models as fc_models


class TestFormQuestionInline(TestCase):
    """Tests for the `FormQuestionInline` class."""

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(fc_models.User, is_superuser=True, is_staff=True)
        cls.form = baker.make(fc_models.Form)
        cls.questions = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            _quantity=2,
        )
        baker.make(fc_models.FormQuestion)

    def setUp(self):
        self.client = Client()
        self.client.force_login(user=self.user)

    def change_form_url(self) -> str:
        """Return the URL to the admin page to edit the form."""
        return reverse("admin:form_creator_form_change", args=[self.form.id])

    @staticmethod
    def add_form_url() -> str:
        """Return the URL to the admin page to add a form."""
        return reverse("admin:form_creator_form_add")

    def test_related_questions_change_form(self):
        """Test that the related questions queryset presents questions related
        to this form.
        """
        response = self.client.get(self.change_form_url())

        self.assertEqual(
            (
                response.context["inline_admin_form"]
                .formset.forms[0]
                .fields["related_question"]
                .queryset.count()
            ),
            len(self.questions),
        )

    def test_related_questions_add_form(self):
        """Test that the related questions queryset provides no options when
        adding a new form.
        """

        self.assertEqual(
            (
                self.client.get(self.add_form_url())
                .context[0]["inline_admin_formsets"][0]
                .formset.form()
                .fields["related_question"]
                .queryset.count()
            ),
            0,
        )


class TestAdminForm(TestCase):
    """Tests for the `FormAdmin` class."""

    @classmethod
    def setUpTestData(cls):
        cls.form = baker.make(fc_models.Form)
        cls.question = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            _quantity=2,
        )
        cls.responses = baker.make(
            fc_models.FormResponse,
            form_responder__form=cls.form,
            _quantity=2,
        )

    def test_export_questions(self):
        """Test that the export questions view returns a CSV file."""
        questions = fc_admin.FormAdmin.export_questions(
            None, None, fc_models.Form.objects.filter(id=self.form.id)
        )
        self.assertIsInstance(questions, HttpResponse)
        self.assertEqual(questions["Content-Type"], "text/csv")

    def test_export_responses(self):
        """Test that the export responses view returns a CSV file."""
        responses = fc_admin.FormAdmin.export_responses(
            None, None, fc_models.Form.objects.filter(id=self.form.id)
        )
        self.assertIsInstance(responses, HttpResponse)
        self.assertEqual(responses["Content-Type"], "text/csv")
