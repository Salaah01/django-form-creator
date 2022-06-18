from django.test import SimpleTestCase
from .. import form_fields


class TestFieldsLoad(SimpleTestCase):
    """Test that each custom form field loads."""

    def test_date_field(self):
        """Test that the date field loads."""
        form_fields.DateField()

    def test_datetime_field(self):
        """Test that the datetime field loads."""
        form_fields.DateTimeField()

    def test_time_field(self):
        """Test that the time field loads."""
        form_fields.TimeField()
