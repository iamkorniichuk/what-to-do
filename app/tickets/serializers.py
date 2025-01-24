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
            "type",
            "type_name",
            "type_description",
            "activity",
            "activity_pk",
            "amount",
        )
        read_only_fields = ("type", "activity")

    type = TicketTypeSerializer(required=False)
    type_name = serializers.CharField(source="name")
    type_description = serializers.CharField(source="description")
    activity = ActivitySerializer(required=False)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    amount = serializers.IntegerField(min_value=1)


class UpdateTicketSerializer(CreateTicketSerializer):
    class Meta:
        model = TicketType
        fields = (
            "type",
            "type_name",
            "type_description",
            "activity",
            "activity_pk",
            "amount",
        )
        read_only_fields = (
            "type",
            "type_name",
            "type_description",
            "activity",
            "activity_pk",
        )

    def validate_amount(self, value):
        if len(self.instance.available_tickets) < value:
            raise serializers.ValidationError("You can't remove already booked tickets")
