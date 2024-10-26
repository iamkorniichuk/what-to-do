from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainSerializer,
)


User = get_user_model()


class LoginRefreshSerializer(TokenRefreshSerializer):
    refresh_token = TokenRefreshSerializer._declared_fields["refresh"]
    access_token = TokenRefreshSerializer._declared_fields["access"]

    refresh = None
    access = None

    def validate(self, attrs):
        tokens = {"refresh": attrs["refresh_token"]}
        valid_tokens = super().validate(tokens)
        data = {"access_token": valid_tokens["access"]}
        return data


class LoginSerializer(TokenObtainSerializer):
    efault_error_messages = {"no_active_account": "Invalid credentials provided"}
    token_class = RefreshToken

    def to_representation(self, instance):
        data = super().to_representation(instance)
        token = self.get_token(self.user)
        data["refresh_token"] = str(token)
        data["access_token"] = str(token.access_token)
        return data

    def validate(self, credentials):
        super().validate(credentials)
        return credentials


class SignUpSerializer(serializers.ModelSerializer, LoginSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
        }

    def __init__(self, *args, **kwargs):
        serializers.ModelSerializer.__init__(self, *args, **kwargs)

    def validate(self, data):
        validated_data = serializers.ModelSerializer.validate(self, data)
        return validated_data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        LoginSerializer.validate(self, validated_data)
        return user
