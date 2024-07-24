REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "users.permissions.IsEmailVerified",
    ],
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
