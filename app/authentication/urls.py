from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    VerifyEmailView,
    ResendEmailVerificationView,
    ConfirmEmailView,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("password/reset/", PasswordResetView.as_view(), name="account_reset_password"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="account_reset_password_done",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path("signup/", RegisterView.as_view(), name="account_signup"),
    path(
        "signup/account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "signup/verify-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "signup/verify-email/resend",
        ResendEmailVerificationView.as_view(),
        name="account_email_verification_resent",
    ),
]
