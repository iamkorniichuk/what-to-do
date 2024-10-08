from rest_framework.permissions import BasePermission


def has_verified_email(user):
    is_verified = user.email
    return is_verified


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and has_verified_email(user))
