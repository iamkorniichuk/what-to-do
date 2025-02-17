from rest_framework import viewsets, mixins

from .models import TicketScan
from .serializers import TicketScanSerializer


class TicketScanViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TicketScan.objects.all()
    serializer_class = TicketScanSerializer
