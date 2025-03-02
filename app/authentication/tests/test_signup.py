from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status, test


User = get_user_model()


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = test.APIClient(enforce_csrf_checks=True)
        self.username = "newuser"
        self.url = reverse("authentication:signup")

    def test_valid(self):
        data = {"username": self.username, "password": "securepassword123"}
        response = self.client.post(self.url, data, format="json")

        self.assertContains(
            response,
            text="refresh",
            status_code=status.HTTP_200_OK,
        )

    def test_no_username(self):
        data = {"email": self.username, "password": "securepassword123"}
        response = self.client.post(self.url, data, format="json")

        self.assertContains(
            response,
            text="username",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_weak_password(self):
        data = {"username": self.username, "password": "pasword"}
        response = self.client.post(self.url, data, format="json")

        self.assertContains(
            response,
            text="password",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
