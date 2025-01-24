from rest_framework import viewsets, mixins

from commons.permissions import IsRelatedToUser

from .models import Ticket, TicketType
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
        if self.request.action == "create":
            return CreateTicketSerializer
        if self.request.action in ["update", "partial_update"]:
            return UpdateTicketSerializer

    def perform_create(self, serializer):
        data = serializer.data
        amount = data.pop("amount")
        ticket_type = serializer.create(data)

        self.bulk_create_ticket(ticket_type, amount)

        return ticket_type

    def perform_update(self, serializer):
        ticket_type = serializer.instance

        old_amount = len(ticket_type.tickets)
        new_amount = serializer.data["amount"]

        if new_amount < old_amount:
            amount = old_amount - new_amount
            self.bulk_delete_ticket(ticket_type, amount)
        else:
            amount = new_amount - old_amount
            self.bulk_create_ticket(ticket_type, amount)

        return ticket_type

    def bulk_create_ticket(self, ticket_type, amount):
        tickets = []
        for _ in range(amount):
            tickets.append(Ticket(type=ticket_type))
        return Ticket.objects.bulk_create(tickets)

    def bulk_delete_ticket(self, ticket_type, amount):
        tickets = ticket_type.available_tickets[:amount]
        tickets.delete()
        return tickets
