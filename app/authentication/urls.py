from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from .views import SignUpView


app_name = "authentication"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
]
