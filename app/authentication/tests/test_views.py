from unittest.mock import patch, MagicMock, ANY

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status, test

from authentication.views import SignUpView


User = get_user_model()


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.factory = test.APIRequestFactory()
        self.username = "newuser"
        self.url = reverse("authentication:signup")

    def test_valid(self):
        data = {"username": self.username, "password": "securepassword123"}
        response, mocks = self.mock_signup(data)

        mocks["save"].assert_called_once()
        mocks["authenticate"].assert_called_once_with(
            username=data["username"],
            password=data["password"],
            request=ANY,
        )
        mocks["create"].assert_called_once_with(
            user=mocks["user"],
            token=response.data["refresh"],
            jti=ANY,
            expires_at=ANY,
            created_at=ANY,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_username(self):
        data = {"email": self.username, "password": "securepassword123"}
        response, mocks = self.mock_signup(data)

        mocks["save"].assert_not_called()
        mocks["authenticate"].assert_not_called()
        mocks["create"].assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("authentication.serializers.SignUpSerializer.save")
    @patch("rest_framework_simplejwt.serializers.authenticate")
    @patch(
        "rest_framework_simplejwt.token_blacklist.models.OutstandingToken.objects.create"
    )
    def mock_signup(self, data, _mock_create, _mock_authenticate, _mock_save):
        _mock_user = MagicMock(
            spec=User,
            id=1,
            username=self.username,
            is_active=True,
            _state=MagicMock(db=None),
        )
        _mock_save.return_value = _mock_user
        _mock_authenticate.return_value = _mock_user

        request = self.factory.post(self.url, data, format="json")
        response = SignUpView.as_view()(request)

        return response, {
            "create": _mock_create,
            "authenticate": _mock_authenticate,
            "save": _mock_save,
            "user": _mock_user,
        }
