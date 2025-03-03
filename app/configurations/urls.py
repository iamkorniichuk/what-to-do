from django.urls import path

from .viewsets import ConfigurationViewSet


app_name = "configurations"


urlpatterns = [
    path(
        "my/",
        ConfigurationViewSet.as_view({"get": "my", "put": "my", "patch": "my"}),
        name="configuration-my",
    ),
]
