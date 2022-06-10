from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from .. import forms as fc_forms


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
