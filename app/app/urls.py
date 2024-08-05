from django.urls import path, include


urlpatterns = [
    path("auth/", include("users.auth_urls")),
    path("activities/", include("activities.urls")),
]
