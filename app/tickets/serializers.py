from rest_framework import serializers

from users.serializers import UserSerializer
from ticket_types.serializers import TicketTypeSerializer
from ticket_types.models import TicketType

from .models import Ticket


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
    type_pk = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(),
        source="type",
    )
    booked_by = UserSerializer(required=False)
    booked_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="booked_by",
    )
