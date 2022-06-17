"""This module contains tests for the `exporters` module."""

from django.test import TestCase
from django.http import HttpResponse
from model_bakery import baker
from .. import models as fc_models, exporters as fc_exporters


class TestExportQuestions(TestCase):
    """Tests for the `export_questions` function."""

    def setUp(self):
        baker.make(fc_models.FormQuestion)
        baker.make(fc_models.FormQuestion)
        self.response = HttpResponse(content="text/csv")
        self.response["Content-Disposition"] = "attachment; filename=test.csv"

    def test_export_questions(self):
        """Test that questions are exported to a CSV file."""
        fc_exporters.export_questions(
            fc_models.FormQuestion.objects.all(), self.response
        )

        content = self.response.content.decode("utf-8")
        for form_question in fc_models.FormQuestion.objects.all():
            self.assertIn(form_question.form.title, content)
            self.assertIn(form_question.question, content)
            self.assertIn(form_question.field_type, content)
            self.assertIn(str(form_question.seq_no), content)


class TestExportResponses(TestCase):
    """Tests for the `export_responses` function."""

    def setUp(self):
        baker.make(fc_models.FormResponse)
        baker.make(fc_models.FormResponse)
        self.response = HttpResponse(content="text/csv")
        self.response["Content-Disposition"] = "attachment; filename=test.csv"

    def test_export_responses(self):
        """Test that responses are exported to a CSV file."""
        fc_exporters.export_responses(
            fc_models.FormResponse.objects.all(), self.response
        )

        content = self.response.content.decode("utf-8")
        for form_response in fc_models.FormResponse.objects.all():
            self.assertIn(form_response.form_responder.form.title, content)
            self.assertIn(form_response.form_responder.user.username, content)
            self.assertIn(
                str(form_response.form_responder.created_dt), content
            )
            self.assertIn(form_response.question.question, content)
