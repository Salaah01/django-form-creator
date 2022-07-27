import mock
from django.test import TestCase
from .. import checks


def mocked_is_content_types_loaded():
    return False


class TestChecks(TestCase):
    """Tests for Django system checks."""

    @mock.patch(
        "form_creator.checks.is_content_types_loaded",
        mocked_is_content_types_loaded,
    )
    def test_content_type_loaded(self):
        """Check that a warning is raised when the content type model is not
        loaded.
        """

        errors = checks.check_content_types_is_loaded(None)
        self.assertEqual(len(errors), 1)
