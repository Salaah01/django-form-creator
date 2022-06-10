from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker
from .. import models as fc_models


class TestForms(TestCase):
    """Tests custom managers and querysets associated with the Form model."""

    def test_live_qs(self):
        """Test the live queryset only returns live forms."""

        # Inactive form
        baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.INACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=None,
        )

        # Form that hasn't started yet
        baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() + timedelta(days=1),
            end_dt=None,
        )

        # Form that has ended
        baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1, hours=1),
            end_dt=timezone.now() - timedelta(days=1),
        )

        # Live forms
        live_form_1 = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=timezone.now() + timedelta(days=1),
        )
        live_form_2 = baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=None,
        )

        results = fc_models.Form.objects.filter().live()
        self.assertEqual(results.count(), 2)
        self.assertIn(live_form_1, results)
        self.assertIn(live_form_2, results)

    def test_live_manager_method(self):
        """Test the manager's `live` method."""
        baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.INACTIVE,
        )
        baker.make(
            fc_models.Form,
            status=fc_models.Form.StatusChoices.ACTIVE,
            start_dt=timezone.now() - timedelta(days=1),
            end_dt=timezone.now() + timedelta(days=1),
        )

        results = set(
            fc_models.Form.objects.live().values_list("id", flat=True)
        )
        expected_results = set(
            fc_models.Form.objects.filter().live().values_list("id", flat=True)
        )
        self.assertEqual(results, expected_results)
