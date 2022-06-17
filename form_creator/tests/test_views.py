from types import SimpleNamespace
from django.test import TestCase, Client
from django.urls import reverse
from django.http import Http404
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
import mock
from model_bakery import baker
from .. import views as fc_views, models as fc_models
from ..question_form_fields import FieldTypeChoices

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
        response = self.client.get(reverse("form_creator:form_create"))
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
            response = self.client.get(reverse("form_creator:form_create"))
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
                "form_creator:form_delete",
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
                "form_creator:form_delete",
                kwargs={
                    "pk": form_instance.id,
                    "slug": form_instance.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 403)


class TestFromQuestionEditView(TestCase):
    """Tests the `FormQuestionEditView` class."""

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.form = baker.make(fc_models.Form, owner=cls.user)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.question_1 = baker.make(
            fc_models.FormQuestion,
            form=self.form,
        )
        self.question_2 = baker.make(
            fc_models.FormQuestion,
            form=self.form,
        )

    def test_get_view_loads(self):
        """Test that the form actually loads."""
        response = self.client.get(
            reverse(
                "form_creator:form_questions_edit",
                kwargs={
                    "pk": self.question_1.form.id,
                    "slug": self.question_1.form.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        """Test a post request with one change and one delete."""
        self.client.post(
            reverse(
                "form_creator:form_questions_edit",
                kwargs={
                    "pk": self.question_1.form.id,
                    "slug": self.question_1.form.slug,
                },
            ),
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "2",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-id": str(self.question_1.id),
                "form-0-question": "question 1",
                "form-0-field_type": "text",
                "form-0-seq_no": "1",
                "form-1-DELETE": "on",
                "form-1-id": str(self.question_2.id),
            },
            instance=self.question_1,
        )

        self.assertEqual(fc_models.FormQuestion.objects.count(), 1)
        self.assertFalse(
            fc_models.FormQuestion.objects.filter(
                id=self.question_2.id,
            ).exists()
        )

    def test_post_view_not_changed(self):
        """Test a post request with no changes."""
        res = self.client.post(
            reverse(
                "form_creator:form_questions_edit",
                kwargs={
                    "pk": self.question_1.form.id,
                    "slug": self.question_1.form.slug,
                },
            ),
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "1",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-id": str(self.question_1.id),
                "form-0-question": self.question_1.question,
                "form-0-field_type": self.question_1.field_type,
                "form-0-seq_no": self.question_1.seq_no,
            },
        )

        self.assertEqual(
            res.url,
            reverse(
                "form_creator:form_detail",
                kwargs={"pk": self.form.id, "slug": self.form.slug},
            ),
        )

    def test_post_view_with_errors(self):
        """Test a post request with errors."""
        res = self.client.post(
            reverse(
                "form_creator:form_questions_edit",
                kwargs={
                    "pk": self.question_1.form.id,
                    "slug": self.question_1.form.slug,
                },
            ),
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "1",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-id": str(self.question_1.id),
                "form-0-question": "",
                "form-0-field_type": "zzzz",
                "form-0-seq_no": "1",
            },
        )

        self.assertEqual(res.status_code, 200)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please correct the errors below.",
        )


class TestFormResponseView(TestCase):
    """Tests the `FormResponseView` class."""

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.form = baker.make(fc_models.Form)
        cls.text_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            required=True,
        )
        cls.choice_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            field_type=FieldTypeChoices.CHOICE,
            choices="a|b|c",
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def view_url(self) -> str:
        """Return the URL for the view."""
        return reverse(
            "form_creator:form_response",
            kwargs={
                "pk": self.form.id,
                "slug": self.form.slug,
            },
        )

    def test_get_view_loads(self):
        """Test that the form actually loads."""
        response = self.client.get(self.view_url())
        self.assertEqual(response.status_code, 200)

    def test_redirect_completed(self):
        """If the form is completed, redirect the user."""
        baker.make(fc_models.FormResponder, form=self.form, user=self.user)
        response = self.client.get(self.view_url())
        self.assertEqual(response.status_code, 302)

    def test_post(self):
        """Test a post request."""
        response = self.client.post(
            self.view_url(),
            data={
                f"question_{self.text_q.id}": "text answer",
                f"question_{self.choice_q.id}": "b",
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(fc_models.FormResponder.objects.count(), 1)

        form_response = fc_models.FormResponder.objects.first()

        self.assertEqual(form_response.responses.count(), 2)
        self.assertEqual(
            set(
                form_response.responses.all().values_list(
                    "question_id", flat=True
                )
            ),
            {self.text_q.id, self.choice_q.id},
        )
        self.assertEqual(
            form_response.responses.get(question=self.text_q).answer,
            "text answer",
        )
        self.assertEqual(
            form_response.responses.get(question=self.choice_q).answer,
            "b",
        )

    def test_post_invalid_form(self):
        """Test a post request with invalid form."""
        response = self.client.post(
            self.view_url(),
            data={
                f"question_{self.text_q.id}": "",
                f"question_{self.choice_q.id}": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(fc_models.FormResponder.objects.count(), 0)


class TestDownloadQuestions(TestCase):
    """Tests the `download_questions view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.form = baker.make(fc_models.Form, owner=cls.user)
        cls.text_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            required=True,
        )
        cls.choice_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            field_type=FieldTypeChoices.CHOICE,
            choices="a|b|c",
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_loads(self):
        """Test that the form actually loads."""
        response = self.client.get(
            reverse(
                "form_creator:download_questions",
                kwargs={
                    "pk": self.form.id,
                    "slug": self.form.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)


class TestDownloadResponses(TestCase):
    """Tests the `download_responses view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.form = baker.make(fc_models.Form, owner=cls.user)
        cls.text_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            required=True,
        )
        cls.choice_q = baker.make(
            fc_models.FormQuestion,
            form=cls.form,
            field_type=FieldTypeChoices.CHOICE,
            choices="a|b|c",
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_loads(self):
        """Test that the form actually loads."""
        response = self.client.get(
            reverse(
                "form_creator:download_responses",
                kwargs={
                    "pk": self.form.id,
                    "slug": self.form.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
