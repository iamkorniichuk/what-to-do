from rest_framework.routers import DefaultRouter

from .viewsets import TicketViewSet


app_name = "tickets"

router = DefaultRouter()
router.register("", TicketViewSet, "ticket")

urlpatterns = router.urls
