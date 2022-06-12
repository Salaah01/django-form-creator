from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.test import TestCase
from django.test.client import RequestFactory
from model_bakery import baker
from .. import decorators, models as fc_models


class TestWithFormDecorator(TestCase):
    """Tests for the `with_form` decorator."""

    def setUp(self):
        self.user = baker.make(fc_models.User)
        self.factory = RequestFactory()
        self.form = baker.make(fc_models.Form)

    def test_object_does_not_exist(self):
        """Test that a 404 is raised when the form does not exist."""

        @decorators.with_form()
        def a_view(request, pk, slug):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(Http404):
            a_view(request, pk=1, slug="abc")

    def test_object_does_exist(self):
        """Test that the form is returned when the form exists."""

        @decorators.with_form()
        def a_view(request, form):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user
        response = a_view(request, pk=self.form.pk, slug=self.form.slug)
        self.assertEqual(response.status_code, 200)

    def test_can_can_passes(self):
        """Test that the view is loaded for a user who has editable permissions
        when this is required.
        """

        @decorators.with_form(can_edit=True)
        def a_view(request, form):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user
        self.form.owner = self.user
        self.form.save()

        response = a_view(request, pk=self.form.pk, slug=self.form.slug)
        self.assertEqual(response.status_code, 200)

    def test_can_edit_fails(self):
        """Test that the view is not loaded for a user who does not have
        editable permissions when this is required.
        """

        @decorators.with_form(can_edit=True)
        def a_view(request, form):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            a_view(request, pk=self.form.pk, slug=self.form.slug)

    def test_can_delete_passes(self):
        """Test that the view is loaded for a user who has delete permissions
        when this is required.
        """

        @decorators.with_form(can_delete=True)
        def a_view(request, form):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user
        self.form.owner = self.user
        self.form.save()

        response = a_view(request, pk=self.form.pk, slug=self.form.slug)
        self.assertEqual(response.status_code, 200)

    def test_can_delete_fails(self):
        """Test that the view is not loaded for a user who does not have
        delete permissions when this is required.
        """

        @decorators.with_form(can_delete=True)
        def a_view(request, form):
            return HttpResponse()

        request = self.factory.get("/")
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            a_view(request, pk=self.form.pk, slug=self.form.slug)
