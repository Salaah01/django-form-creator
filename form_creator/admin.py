from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.forms import Textarea
from django.urls import resolve
from . import models as fc_models, exporters as fc_exporters


class TextAreaFormFieldOverride:
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 70})},
    }


class FormQuestionInline(TextAreaFormFieldOverride, admin.StackedInline):
    model = fc_models.FormQuestion
    extra = 0
    classes = ["collapse"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "related_question":
            obj_id = resolve(request.path).kwargs.get("object_id")
            if obj_id:
                kwargs["queryset"] = fc_models.FormQuestion.objects.filter(
                    form_id=obj_id
                )
            else:
                kwargs["queryset"] = fc_models.FormQuestion.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormResponderInline(TextAreaFormFieldOverride, admin.TabularInline):
    model = fc_models.FormResponder
    extra = 0
    raw_id_fields = ("user",)
    fields = (
        "id",
        "user",
        "created_dt",
    )
    readonly_fields = (
        "user",
        "created_dt",
    )
    show_change_link = True


class FormResponseInline(TextAreaFormFieldOverride, admin.TabularInline):
    model = fc_models.FormResponse
    extra = 0
    fields = ("question", "answer")
    raw_id_fields = ("question",)


@admin.register(fc_models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "start_dt", "end_dt", "num_responses")
    list_filter = ("owner",)
    search_fields = ("title", "description")
    date_hierarchy = "start_dt"
    ordering = ("-start_dt",)
    raw_id_fields = ("owner",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("num_responses",)
    inlines = (FormQuestionInline, FormResponderInline)
    actions = ["export_questions", "export_responses"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "num_responses",
                    "description",
                    "owner",
                    "status",
                    "start_dt",
                    "end_dt",
                )
            },
        ),
        ("Editors", {"fields": ("editors",)}),
    )

    @admin.action(description="Export questions")
    def export_questions(
        self,
        request: HttpRequest,
        queryset: QuerySet[fc_models.Form],
    ) -> HttpResponse:
        """Export questions to a CSV file."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=questions.csv"
        fc_exporters.export_questions(
            fc_models.FormQuestion.objects.filter(
                form_id__in=queryset.values_list("id", flat=True)
            ),
            response,
        )
        return response

    @admin.action(description="Export responses")
    def export_responses(
        self,
        request: HttpRequest,
        queryset: QuerySet[fc_models.Form],
    ) -> HttpResponse:
        """Export responses to a CSV file."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=responses.csv"
        fc_exporters.export_responses(
            fc_models.FormResponse.objects.filter(
                form_responder__form_id__in=queryset.values_list(
                    "id", flat=True
                )
            ),
            response,
        )
        return response


@admin.register(fc_models.FormResponder)
class FormResponderAdmin(admin.ModelAdmin):
    list_display = ("form", "user", "created_dt")
    search_fields = (
        "form__title",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    date_hierarchy = "created_dt"
    raw_id_fields = ("form", "user")
    inlines = (FormResponseInline,)
