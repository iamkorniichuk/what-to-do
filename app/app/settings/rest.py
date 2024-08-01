REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "users.permissions.IsEmailVerified",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "users.authentication.BearerAuthentication",
    ],
}
