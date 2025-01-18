from rest_framework.routers import DefaultRouter

from .viewsets import InteractionViewSet


app_name = "interactions"

router = DefaultRouter()
router.register("", InteractionViewSet, "interaction")

urlpatterns = router.urls
