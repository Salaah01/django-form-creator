"""example URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("form-creator/", include("form_creator.urls")),
]
