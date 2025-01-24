from rest_framework import serializers

from activities.models import Activity
from activities.serializers import ActivitySerializer
from users.serializers import UserSerializer

from .models import Ticket, TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            "pk",
            "name",
            "description",
            "activity",
            "activity_pk",
        )
        read_only_fields = ("pk", "activity")

    activity = ActivitySerializer(required=False)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "pk",
            "type",
            "type_pk",
            "booked_by",
            "booked_by_pk",
        )
        read_only_fields = ("pk", "type", "activity", "booked_by")

    type = TicketTypeSerializer(required=False)
    booked_by = UserSerializer(required=False)
    booked_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="booked_by",
    )


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            "pk",
            "name",
            "description",
            "activity",
            "activity_pk",
            "amount",
        )
        read_only_fields = ("pk",)

    activity = ActivitySerializer(required=False, read_only=True)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    amount = serializers.IntegerField(min_value=1, write_only=True)

    def create(self, validated_data):
        amount = validated_data.pop("amount")
        ticket_type = super().create(validated_data)
        self.bulk_create_ticket(ticket_type, amount)
        return ticket_type

    def bulk_create_ticket(self, ticket_type, amount):
        tickets = [Ticket(type=ticket_type) for _ in range(amount)]
        Ticket.objects.bulk_create(tickets)


class UpdateTicketSerializer(CreateTicketSerializer):
    class Meta:
        model = TicketType
        fields = (
            "pk",
            "name",
            "description",
            "activity",
            "activity_pk",
            "amount",
        )
        read_only_fields = (
            "pk",
            "name",
            "description",
            "activity",
            "activity_pk",
        )

    def validate_amount(self, value):
        if len(self.instance.available_tickets) < value:
            raise serializers.ValidationError("You can't remove already booked tickets")
        return value

    def update(self, instance, validated_data):
        old_amount = len(instance.tickets.all())
        new_amount = validated_data.get("amount", old_amount)

        if new_amount < old_amount:
            amount_to_delete = old_amount - new_amount
            self.bulk_delete_ticket(instance, amount_to_delete)
        elif new_amount > old_amount:
            amount_to_create = new_amount - old_amount
            self.bulk_create_ticket(instance, amount_to_create)

        return super().update(instance, validated_data)

    def bulk_delete_ticket(self, ticket_type, amount):
        tickets = ticket_type.available_tickets[:amount]
        return [obj.delete() for obj in tickets]
