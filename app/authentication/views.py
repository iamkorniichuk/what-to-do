from rest_framework.permissions import IsAuthenticated, AllowAny
from dj_rest_auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordResetView as BasePasswordResetView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from dj_rest_auth.registration.views import (
    RegisterView as BaseRegisterView,
    VerifyEmailView as BaseVerifyEmailView,
    ConfirmEmailView as BaseConfirmEmailView,
    ResendEmailVerificationView as BaseResendEmailVerificationView,
)

from .permissions import IsEmailVerified


class LoginView(BaseLoginView):
    permission_classes = [AllowAny]


class LogoutView(BaseLogoutView):
    permission_classes = [IsAuthenticated]


class RegisterView(BaseRegisterView):
    permission_classes = [AllowAny]


class PasswordResetView(BasePasswordResetView):
    permission_classes = [IsEmailVerified]


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    permission_classes = [IsEmailVerified]


class PasswordChangeView(BasePasswordChangeView):
    permission_classes = [IsEmailVerified]


class VerifyEmailView(BaseVerifyEmailView):
    permission_classes = [IsAuthenticated]


class ResendEmailVerificationView(BaseResendEmailVerificationView):
    permission_classes = [IsAuthenticated]


class ConfirmEmailView(BaseConfirmEmailView):
    permission_classes = [AllowAny]
