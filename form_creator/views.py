import re
from django.shortcuts import get_object_or_404
from django.db.models import Q, QuerySet
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models as fc_models, forms as fc_forms


class FormBaseView(View):
    model = fc_models.Form
    form_class = fc_forms.NewForm
    editor_choices = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        if self.editor_choices:
            kwargs["editor_choices"] = self.editor_choices
        return kwargs


class SingleItemMixin:
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


class FormDetailView(FormBaseView, SingleItemMixin, DetailView):
    """View to display a form."""

    template_name = "form_creator/form_detail.html"


class FormUpdateView(FormBaseView, SingleItemMixin, UpdateView):
    """View to edit a form."""

    template_name = "form_creator/form_edit.html"


class FormDeleteView(FormBaseView, SingleItemMixin, DeleteView):
    """View to delete a form."""

    template_name = "form_creator/form_delete.html"
