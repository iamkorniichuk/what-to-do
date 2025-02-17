from rest_framework import serializers

from activities.serializers import ActivitySerializer
from activities.models import Activity
from tickets.serializers import TicketSerializer
from tickets.models import Ticket

from .models import TicketScan


class TicketScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketScan
        fields = (
            "pk",
            "ticket",
            "ticket_pk",
            "activity",
            "activity_pk",
            "created_at",
            "is_valid",
            "times_scanned",
        )
        read_only_fields = (
            "pk",
            "ticket",
            "activity",
            "created_at",
        )

    ticket = TicketSerializer(required=False, read_only=True)
    ticket_pk = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source="ticket",
    )
    activity = ActivitySerializer(required=False, read_only=True)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    is_valid = serializers.SerializerMethodField()
    times_scanned = serializers.SerializerMethodField()

    def get_is_valid(self, obj):
        required_activity = obj.activity
        provided_activity = obj.ticket.type.activity
        return required_activity == provided_activity

    def get_times_scanned(self, obj):
        current_activity = obj.activity
        current_ticket = obj.ticket

        ticket_scans = TicketScan.objects.filter(
            activity=current_activity,
            ticket=current_ticket,
        ).all()
        return len(ticket_scans)
