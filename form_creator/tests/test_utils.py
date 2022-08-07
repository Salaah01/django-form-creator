from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from .. import utils


class TestGetContentFromDict(TestCase):
    """Test for the `get_content_from_dict` function."""

    def test_get_form_id(self):
        """Test that a content type object can be retrieved from the content
        type ID.
        """
        ct = ContentType.objects.first()
        self.assertEqual(utils.get_content_type_from_dict({"id": ct.id}), ct)

    def test_test_form_app_label_and_model(self):
        """Test that a content type object can be retrieved from the content
        type's app label and model.
        """
        ct = ContentType.objects.first()
        self.assertEqual(
            utils.get_content_type_from_dict(
                {"app_label": ct.app_label, "model": ct.model}
            ),
            ct,
        )
