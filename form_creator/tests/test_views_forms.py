from types import SimpleNamespace
from django.test import TestCase, Client
from django.urls import reverse
from django.http import Http404
from django.contrib.auth import get_user_model
import mock
from model_bakery import baker
from .. import views as fc_views, models as fc_models

User = get_user_model()


class TestFormSingleItemMixin(TestCase):
    def test_get_object(self):
        """Test that the `get_object` method returns the correct object."""
        form_instance = baker.make(fc_models.Form)

        self_obj = SimpleNamespace(
            request=SimpleNamespace(
                path=f"/forms/{form_instance.id}-{form_instance.slug}/",
            ),
            model=fc_models.Form,
        )
        self.assertEqual(
            fc_views.FormSingleItemMixin.get_object(self_obj),
            form_instance,
        )

    def test_get_object_invalid(self):
        self_obj = SimpleNamespace(
            request=SimpleNamespace(
                path="/forms/1-abc/",
            ),
            model=fc_models.Form,
        )
        with self.assertRaises(Http404):
            fc_views.FormSingleItemMixin.get_object(self_obj)


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


class TestFormListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = baker.make(User)
        cls.editor = baker.make(User)
        cls.owners_form = baker.make(fc_models.Form, owner=cls.owner)
        cls.editors_form = baker.make(fc_models.Form, editors=[cls.editor])
        baker.make(fc_models.Form)

    @staticmethod
    def self_obj(user: User):
        return SimpleNamespace(
            request=SimpleNamespace(
                user=user,
            ),
            model=fc_models.Form,
        )

    def test_get_queryset_staff(self):
        """Test that the `get_queryset` method returns all forms for staff."""
        self_obj = self.self_obj(baker.make(User, is_staff=True))
        self.assertEqual(
            fc_views.FormListView.get_queryset(self_obj).count(),
            3,
        )

    def test_get_queryset_owner(self):
        """Test that the `get_queryset` method returns only the owner's
        forms.
        """
        self_obj = self.self_obj(self.owner)
        result = fc_views.FormListView.get_queryset(self_obj)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.owners_form)

    def test_get_queryset_editor(self):
        """Test that the `get_queryset` method returns only the editor's
        forms.
        """
        self_obj = self.self_obj(self.editor)
        result = fc_views.FormListView.get_queryset(self_obj)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.editors_form)


class TestFormDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.client.force_login(self.user)

    def test_get_view_loads(self):
        """Test that the form actually loads."""
        form_instance = baker.make(fc_models.Form, owner=self.user)
        response = self.client.get(
            reverse(
                "form_delete",
                kwargs={
                    "pk": form_instance.id,
                    "slug": form_instance.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_view_403(self):
        """Test that the form returns a 403 if the user is not the owner."""
        form_instance = baker.make(fc_models.Form)
        response = self.client.get(
            reverse(
                "form_delete",
                kwargs={
                    "pk": form_instance.id,
                    "slug": form_instance.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 403)
