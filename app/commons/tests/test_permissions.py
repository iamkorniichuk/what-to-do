from unittest.mock import MagicMock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from commons.permissions import IsRelatedToUser


User = get_user_model()


class IsRelatedToUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            username="user-1",
            password="securepassword123",
        )
        cls.user_2 = User.objects.create_user(
            username="user-2",
            password="securepassword123",
        )

    def test_valid(self):
        mock_request = MagicMock(user=self.user_1)

        nested_mock_model = MagicMock(created_by=self.user_1)
        parent_mock_model = MagicMock(nested_model=nested_mock_model)

        permission = IsRelatedToUser("nested_model.created_by")
        is_granted = permission.has_object_permission(
            mock_request,
            view=None,
            obj=parent_mock_model,
        )

        self.assertTrue(is_granted)

    def test_not_related(self):
        mock_request = MagicMock(user=self.user_1)

        nested_mock_model = MagicMock(created_by=self.user_2)
        parent_mock_model = MagicMock(nested_model=nested_mock_model)

        permission = IsRelatedToUser("nested_model.created_by")
        is_granted = permission.has_object_permission(
            mock_request,
            view=None,
            obj=parent_mock_model,
        )

        self.assertFalse(is_granted)

    def test_unauthorized_user(self):
        mock_request = MagicMock(user=AnonymousUser())
        mock_model = MagicMock(created_by=None)

        permission = IsRelatedToUser("created_by")
        is_granted = permission.has_object_permission(
            mock_request,
            view=None,
            obj=mock_model,
        )

        self.assertFalse(is_granted)
