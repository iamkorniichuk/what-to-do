from rest_framework import viewsets, mixins

from commons.permissions import IsRelatedToUser

from .models import TicketType
from .serializers import CreateTicketSerializer, UpdateTicketSerializer


class TicketViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TicketType.objects.all()

    def get_permissions(self):
        permissions = super().get_permissions() + [
            IsRelatedToUser("activity.created_by")
        ]
        return permissions

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTicketSerializer
        if self.action in ["update", "partial_update"]:
            return UpdateTicketSerializer
