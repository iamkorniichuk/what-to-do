from rest_framework import serializers

from .models import TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ("pk", "name", "description")
        read_only_fields = ("pk",)
