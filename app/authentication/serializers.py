from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "password", "refresh", "access")
        read_only_fields = ("pk",)
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"write_only": True},
        }

    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

    def get_access(self, obj):
        token = RefreshToken.for_user(obj).access_token
        return str(token)

    def validate_password(self, value):
        user = self.instance
        validate_password(value, user)
        return value
