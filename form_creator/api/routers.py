from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register("forms", views.FormViewSet, basename="form")
router.register(
    "form-elements",
    views.FormElementViewSet,
    basename="form-element",
)
router.register(
    "html-components",
    views.HTMLComponentViewSet,
    basename="html-component",
)
router.register(
    "form-questions",
    views.FormQuestionViewSet,
    basename="form-question",
)

urlpatterns = router.urls
app_name = "api"
