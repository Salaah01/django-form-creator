from django.shortcuts import render
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


class FormCreateView(FormBaseView, CreateView):
    """View to create a new form."""

    template_name = "form_creator/form_create.html"


class FormDetailView(FormBaseView, DetailView):
    """View to display a form."""

    template_name = "form_creator/form_detail.html"


class FormEditView(FormBaseView, UpdateView):
    """View to edit a form."""

    template_name = "form_creator/form_edit.html"
