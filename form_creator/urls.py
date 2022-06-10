from django.urls import path
from . import views

app_name = "form_creator"

urlpatterns = [
    path("form/create/", views.FormCreateView.as_view(), name="form_create"),
    path(
        "form/<int:pk>-<slug:slug>/",
        views.FormDetailView.as_view(),
        name="form_detail",
    ),
    path(
        "form/<int:pk>-<slug:slug>/edit/",
        views.FormEditView.as_view(),
        name="form_edit",
    ),
]
