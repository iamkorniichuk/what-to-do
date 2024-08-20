from rest_framework.permissions import BasePermission
from allauth.account.utils import has_verified_email


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and has_verified_email(user))
