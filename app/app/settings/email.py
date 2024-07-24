from .base import env


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
