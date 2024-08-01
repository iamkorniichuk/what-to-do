from rest_framework.serializers import CharField
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)


class RegisterSerializer(BaseRegisterSerializer):
    password1 = None
    password2 = None

    password = CharField(write_only=True)

    def validate_password(self, password):
        return super().validate_password1(password)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", ""),
        }
