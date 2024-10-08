from django.urls import path

from .views import (
    LoginView,
    LoginRefreshView,
    SignUpView,
    LogoutView,
)


app_name = "authentication"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", LoginRefreshView.as_view(), name="login-refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
