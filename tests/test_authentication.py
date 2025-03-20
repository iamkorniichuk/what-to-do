import pytest
from django.urls import reverse_lazy


@pytest.mark.django_db
class TestAuthentication:
    signup_url = reverse_lazy("authentication:signup")
    login_url = reverse_lazy("authentication:login")
    login_refresh_url = reverse_lazy("authentication:login-refresh")
    logout_url = reverse_lazy("authentication:logout")

    def test_signup(self, api_client, user_credentials):
        response = api_client.post(self.signup_url, user_credentials)

        assert response.status_code == 201
        assert "access" in response.data.keys()
        assert "refresh" in response.data.keys()

    def test_login(self, api_client, signup_user, user_credentials):
        response = api_client.post(self.login_url, user_credentials)

        assert response.status_code == 200
        assert "access" in response.data.keys()
        assert "refresh" in response.data.keys()

    def test_login_refresh(self, api_client, signup_user):
        data = {"refresh": signup_user["refresh"]}

        response = api_client.post(self.login_refresh_url, data)

        assert response.status_code == 200
        assert "access" in response.data.keys()

    def test_logout(self, api_client, signup_user):
        data = {"refresh": signup_user["refresh"]}

        response = api_client.post(self.logout_url, data)
        assert response.status_code == 200

        response = api_client.post(self.login_refresh_url, data)
        assert response.status_code == 401
        assert "access" not in response.data.keys()
