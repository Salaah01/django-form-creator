from django.urls import path, include
from . import views

app_name = "form_creator"

urlpatterns = [
    path("react-form/", views.react_form, name="react_form_create"),
    path("react-form/<int:pk>/", views.react_form, name="react_form_edit"),
    path("forms/", views.FormListView.as_view(), name="form_list"),
    path("forms/create/", views.FormCreateView.as_view(), name="form_create"),
    path(
        "forms/<int:pk>-<slug:slug>/",
        views.FormDetailView.as_view(),
        name="form_detail",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/edit/",
        views.FormUpdateView.as_view(),
        name="form_edit",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/delete/",
        views.FormDeleteView.as_view(),
        name="form_delete",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/response/",
        views.FormResponseView.as_view(),
        name="form_response",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/export/questions/",
        views.download_questions,
        name="download_questions",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/export/responses/",
        views.download_responses,
        name="download_responses",
    ),
    path(
        "forms/<int:pk>-<slug:slug>/questions/edit/",
        views.FormQuestionsEditView.as_view(),
        name="form_questions_edit",
    ),
    path("api/", include("form_creator.api.routers")),
]
