from rest_framework import serializers

from .models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ("pk", "is_remote_allowed", "allowed_distance", "start_location")
