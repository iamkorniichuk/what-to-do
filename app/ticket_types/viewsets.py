from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUser

from .models import TicketType
from .ticket_serializers import (
    CreateTicketTypeSerializer,
    UpdateTicketTypeSerializer,
)


class TicketTypeViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
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
            return CreateTicketTypeSerializer
        if self.action in ["update", "partial_update"]:
            return UpdateTicketTypeSerializer

    @action(["post"], detail=True)
    def book(self, request, pk=None):
        queryset = self.get_queryset()
        ticket_type = get_object_or_404(queryset, pk=pk)

        current_user = request.user

        is_booking_limit_exceeded = ticket_type.tickets.filter(
            booked_by=current_user
        ).exists()
        if is_booking_limit_exceeded:
            return Response(
                "You can't book more than one ticket",
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_tickets = ticket_type.available_tickets
        if len(available_tickets) == 0:
            return Response("No available tickets", status=status.HTTP_400_BAD_REQUEST)

        ticket = available_tickets[0]
        ticket.booked_by = current_user
        ticket.save()

        return Response("Is successfully booked", status=status.HTTP_200_OK)
