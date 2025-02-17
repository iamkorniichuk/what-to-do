from rest_framework import serializers

from .models import TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ("pk", "name", "description", "available_amount")
        read_only_fields = ("pk",)

    available_amount = serializers.SerializerMethodField()

    def get_available_amount(self, obj):
        available_tickets = TicketType.objects.get(pk=obj.pk).available_tickets
        return len(available_tickets)
