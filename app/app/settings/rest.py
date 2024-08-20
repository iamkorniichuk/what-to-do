REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "authentication.permissions.IsEmailVerified",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.authentication.BearerAuthentication",
    ],
}
