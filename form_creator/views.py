import re
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models as fc_models, forms as fc_forms


class FormBaseView(View):
    model = fc_models.Form
    form_class = fc_forms.NewForm
    editor_choices = None
    success_url = reverse_lazy("form_creator:form_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        if self.editor_choices:
            kwargs["editor_choices"] = self.editor_choices
        return kwargs


class FormSingleItemMixin:
    def get_object(self, *args, **kwargs):
        pattern = re.compile("/forms/(\\d{1,})-(.*?)/")
        pk, slug = pattern.search(self.request.path).groups()
        return get_object_or_404(self.model, pk=pk, slug=slug)


class FormListView(FormBaseView, ListView):
    """List all forms. A owner and editor can see forms of all statuses.
    All other users can only see live forms.
    """

    def get_queryset(self) -> QuerySet[fc_models.Form]:
        """If the user is a staff member, return all forms. Otherwise, return
        only live forms and those which the user can edit/owns.
        """
        if self.request.user.is_staff:
            return self.model.objects.all()

        # Forms that are editable by the user
        qs = self.model.get_editable_forms(self.request.user)

        # Forms that are live
        qs |= self.model.objects.live()

        return qs


class FormCreateView(FormBaseView, CreateView):
    """View to create a new form."""

    template_name = "form_creator/form_create.html"


class FormDetailView(FormBaseView, FormSingleItemMixin, DetailView):
    """View to display a form."""

    template_name = "form_creator/form_detail.html"


class FormUpdateView(FormBaseView, FormSingleItemMixin, UpdateView):
    """View to edit a form."""

    template_name = "form_creator/form_edit.html"


class FormDeleteView(FormBaseView, FormSingleItemMixin, DeleteView):
    """View to delete a form."""

    form_class = fc_forms.DeleteForm
    template_name = "form_creator/form_delete.html"

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        if not self.object.can_delete(request.user):
            raise PermissionDenied(
                "You must be the owner to delete this form."
            )
        return res

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("editor_choices", None)
        kwargs["instance"] = self.get_object()
        return kwargs
