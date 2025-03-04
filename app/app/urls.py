from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("activities/", include("activities.urls")),
    path("auth/", include("authentication.urls")),
    path("interactions/", include("interactions.urls")),
    path("users/", include("users.urls")),
    path("tickets/", include("tickets.urls")),
    path("ticket_types/", include("ticket_types.urls")),
    path("ticket_scans/", include("ticket_scans.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
