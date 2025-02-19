from django.urls import path

from .viewsets import UserViewSet


app_name = "users"


urlpatterns = [
    path(
        "my/",
        UserViewSet.as_view({"get": "my", "put": "my", "patch": "my"}),
        name="user-my",
    ),
    path("<int:pk>/", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
]
