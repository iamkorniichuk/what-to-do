from rest_framework.routers import DefaultRouter

from .viewsets import TicketScanViewSet


app_name = "ticket_scans"

router = DefaultRouter()
router.register("", TicketScanViewSet, "ticket_scan")

urlpatterns = router.urls
