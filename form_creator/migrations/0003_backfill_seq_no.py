"""This migration populates data on the `FormElementOrder` model taking the
`seq_no` field from the `FormQuestion` model.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def backfill_seq_no(apps, schema_editor):
    FormQuestion = apps.get_model("form_creator", "FormQuestion")
    FormElementOrder = apps.get_model("form_creator", "FormElementOrder")
    ContentType = apps.get_model("contenttypes", "ContentType")

    form_question_ct = ContentType.objects.get_for_model(FormQuestion)

    for form_question in FormQuestion.objects.all().select_related("form"):
        FormElementOrder.objects.create(
            form=form_question.form,
            element_type=form_question_ct,
            element_id=form_question.id,
            seq_no=form_question.seq_no,
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('form_creator', '0002_alter_form_status_alter_formquestion_seq_no_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_seq_no),
    ]
    
