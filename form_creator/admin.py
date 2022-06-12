from django.contrib import admin
from . import models


class FormQuestionInline(admin.StackedInline):
    model = models.FormQuestion
    extra = 0


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "owner", "start_dt", "end_dt")
    list_filter = ("owner",)
    search_fields = ("title", "description")
    date_hierarchy = "start_dt"
    ordering = ("-start_dt",)
    raw_id_fields = ("owner",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = (FormQuestionInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
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
