from rest_framework.routers import DefaultRouter

from .viewsets import TicketTypeViewSet


app_name = "ticket_types"

router = DefaultRouter()
router.register("", TicketTypeViewSet, "ticket_type")

urlpatterns = router.urls
