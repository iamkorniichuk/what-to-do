from rest_framework.permissions import BasePermission


def has_verified_contact(user, related_name):
    has_contact = hasattr(user, related_name)
    if not has_contact:
        return False

    contact = getattr(user, related_name)
    return contact.is_verified


def has_verified_email(user):
    return has_verified_contact(user, "email")


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and has_verified_email(user))
