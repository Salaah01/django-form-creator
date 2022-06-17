"""This module contains methods to export data from the database."""

import csv
from django.db.models import QuerySet
from . import models as fc_models


def export_questions(form_questions: QuerySet[fc_models.FormQuestion], output):
    """Export the questions in a form to a CSV file."""
    writer = csv.writer(output)
    writer.writerow(
        [
            "Form",
            "Question",
            "Type",
            "Required",
            "Seq. No.",
            "Choices",
            "Related Question",
        ]
    )
    for question in form_questions:
        writer.writerow(
            [
                question.form.title,
                question.question,
                question.field_type,
                question.required and "Yes" or "No",
                question.seq_no,
                question.choices,
                question.related_question,
            ]
        )


def export_responses(form_responses: QuerySet[fc_models.FormResponse], output):
    """Export the responses in a form to a CSV file."""
    writer = csv.writer(output)
    writer.writerow(
        [
            "Form",
            "Username",
            "Email",
            "Answered On",
            "Question",
            "Answer",
        ]
    )
    for response in form_responses:
        writer.writerow(
            [
                response.form_responder.form,
                response.form_responder.user.username,
                response.form_responder.user.email,
                response.form_responder.created_dt,
                response.question.question,
                response.answer,
            ]
        )
