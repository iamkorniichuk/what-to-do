from rest_framework.permissions import BasePermission


class HasFilledConfiguration(BasePermission):
    error_message = "You need to fill the configuration."

    def __init__(self):
        self.message = {"configuration": self.error_message}

    def has_permission(self, request, view):
        current_user = request.user
        configuration = getattr(current_user, "configuration", None)

        if configuration is None:
            return False

        is_start_location_set = configuration.start_location is not None

        return is_start_location_set
