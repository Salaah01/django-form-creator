import re
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views import View
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from . import models as fc_models, forms as fc_forms, exporters as fc_exporters
from .decorators import with_form, redirect_if_form_completed


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

    def get_context_data(self, **kwargs):
        """Adds permissions to the context."""
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["can_edit"] = obj.can_edit(self.request.user)
        context["can_delete"] = obj.can_delete(self.request.user)
        context["completed_form"] = obj.completed_by(self.request.user)
        context["can_complete_form"] = obj.can_complete_form(self.request.user)
        return context


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


class FormQuestionsEditView(View):
    """View to manage questions for a form. Within this view the user would be
    able to add/edit/delete questions.
    """

    template_name = "form_creator/form_questions_edit.html"

    @method_decorator(with_form(can_edit=True), name="dispatch")
    def get(self, request: HttpRequest, form: fc_models.Form) -> HttpResponse:

        extra = 0 if form.questions.count() else 1
        FormQuestionFS = modelformset_factory(
            fc_models.FormQuestion,
            form=fc_forms.FormQuestionForm,
            extra=extra,
            can_delete=True,
        )

        return render(
            request,
            self.template_name,
            {
                "object": form,
                "formset": FormQuestionFS(
                    initial=form.questions.all().values(),
                    form_kwargs={"form_id": form.id},
                ),
            },
        )

    @method_decorator(with_form(can_edit=True), name="dispatch")
    def post(self, request: HttpRequest, form: fc_models.Form) -> HttpResponse:

        extra = 0 if form.questions.count() else 1
        FormQuestionFS = modelformset_factory(
            fc_models.FormQuestion,
            form=fc_forms.FormQuestionForm,
            extra=extra,
            can_delete=True,
        )

        formset = FormQuestionFS(
            request.POST, form_kwargs={"form_id": form.id}
        )
        if not formset.has_changed():
            return redirect(form.get_absolute_url())

        if formset.is_valid():
            formset.save()
            messages.success(request, "Questions edited.")
            return redirect(form.get_absolute_url())
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                self.template_name,
                {
                    "object": form,
                    "formset": formset,
                },
            )


class FormResponseView(View):
    """View for users to respond to questions in a form."""

    template_name = "form_creator/form_response.html"
    success_url = None

    @method_decorator(login_required, name="dispatch")
    @method_decorator(with_form(), name="dispatch")
    @method_decorator(redirect_if_form_completed(), name="dispatch")
    def get(self, request: HttpRequest, form: fc_models.Form) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {"object": form, "form": fc_forms.CaptureResponseForm(form)},
        )

    @method_decorator(login_required, name="dispatch")
    @method_decorator(with_form(), name="dispatch")
    @method_decorator(redirect_if_form_completed(), name="dispatch")
    def post(self, request: HttpRequest, form: fc_models.Form) -> HttpResponse:
        response_form = fc_forms.CaptureResponseForm(form, request.POST)
        if response_form.is_valid():
            response_form.save(request.user)
            messages.success(request, "Response saved.")
            return redirect(self.success_url or form.get_absolute_url())
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                self.template_name,
                {"object": form, "form": response_form},
            )


@with_form(can_edit=True)
def download_questions(
    request: HttpRequest, form: fc_models.Form
) -> HttpResponse:
    """View to download a form's questions as a CSV file."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=questions.csv"
    fc_exporters.export_questions(
        fc_models.FormQuestion.objects.filter(form=form),
        response,
    )
    return response


@with_form(can_edit=True)
def download_responses(
    request: HttpRequest, form: fc_models.Form
) -> HttpResponse:
    """View to download a form's responses as a CSV file."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=responses.csv"
    fc_exporters.export_responses(
        fc_models.FormResponse.objects.filter(form_responder__form=form),
        response,
    )
    return response
