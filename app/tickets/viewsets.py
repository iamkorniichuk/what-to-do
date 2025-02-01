from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUser

from .models import TicketType, Ticket
from .serializers import (
    CreateTicketSerializer,
    UpdateTicketSerializer,
    TicketSerializer,
)


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

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user
        queryset = Ticket.objects.filter(booked_by=current_user).all()

        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
