from django.contrib import admin
from . import models


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "owner", "start_dt", "end_dt")
    list_filter = ("owner",)
    search_fields = ("title", "description")
    date_hierarchy = "start_dt"
    ordering = ("-start_dt",)
    raw_id_fields = ("owner",)
    prepopulated_fields = {"slug": ("title",)}
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
