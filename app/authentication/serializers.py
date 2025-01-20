from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "password")
        read_only_fields = ("pk",)
        extra_kwargs = {"password": {"write_only": True}}
