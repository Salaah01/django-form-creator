from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register("forms", views.FormViewSet, basename="form")
urlpatterns = router.urls
app_name = "api"
