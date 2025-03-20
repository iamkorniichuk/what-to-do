import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user_credentials():
    return {"username": "newuser", "password": "testpass123"}


@pytest.fixture
def signup_user(api_client, user_credentials):
    from django.urls import reverse

    signup_url = reverse("authentication:signup")
    response = api_client.post(signup_url, user_credentials)

    return response.data


@pytest.fixture
def auth_client(api_client, signup_user):
    access_token = signup_user["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client
