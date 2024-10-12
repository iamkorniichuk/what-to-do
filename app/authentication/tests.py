from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .utils import validate_access_token, validate_refresh_token, get_tokens


SIGN_UP_URL = reverse("authentication:signup")
LOGIN_URL = reverse("authentication:login")
LOGIN_REFRESH_URL = reverse("authentication:login-refresh")
LOGOUT_URL = reverse("authentication:logout")

User = get_user_model()


class AuthenticationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existing_user_credentials = {
            "email": "user1@test.com",
            "password": "insecure-password-123",
        }
        cls.existing_user = User.objects.create_user(**cls.existing_user_credentials)
        cls.new_user_credentials = {
            "email": "user2@test.com",
            "password": "insecure-password-123",
        }

        return super().setUpTestData()

    def is_refresh_token_valid(self, response):
        token, _ = get_tokens(response)
        return validate_refresh_token(token)

    def is_access_token_valid(self, response):
        _, token = get_tokens(response)
        return validate_access_token(token)

    def test_sign_up(self):
        response = self.client.post(
            SIGN_UP_URL,
            self.new_user_credentials,
            "json",
        )

        assert self.is_access_token_valid(response) and self.is_refresh_token_valid(
            response
        )

        is_user_created = User.objects.filter(
            email=self.new_user_credentials["email"]
        ).exists()

        assert is_user_created

    def test_login(self):
        response = self.client.post(
            LOGIN_URL,
            self.existing_user_credentials,
            "json",
        )

        assert self.is_access_token_valid(response) and self.is_refresh_token_valid(
            response
        )

    def test_login_refresh(self):
        response = self.client.post(
            LOGIN_URL,
            self.existing_user_credentials,
            "json",
        )
        refresh_token, _ = get_tokens(response)

        data = {"refresh_token": refresh_token}
        response = self.client.post(
            LOGIN_REFRESH_URL,
            data,
            "json",
        )

        assert self.is_access_token_valid(response)
