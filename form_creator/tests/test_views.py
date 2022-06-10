from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import mock
from model_bakery import baker
from .. import views as fc_views

User = get_user_model()


class TestFormCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.client.force_login(self.user)

    def test_form_create_view_loads(self):
        """Test that the form actually loads."""
        response = self.client.get(reverse("form_create"))
        self.assertEqual(response.status_code, 200)

    def test_get_form_kwargs(self):
        """Test the `get_form_kwargs` method loads the editors when
        provided.
        """
        baker.make(User, _quantity=2)
        editors = User.objects.all()

        with mock.patch.object(
            fc_views.FormBaseView, "editor_choices", editors
        ):
            response = self.client.get(reverse("form_create"))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                set(
                    response.context["form"]
                    .fields["editors"]
                    .queryset.values_list("id")
                ),
                set(editors.values_list("id")),
            )
