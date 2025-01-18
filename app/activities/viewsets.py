from django.db.models import Q
from rest_framework import viewsets, parsers

from commons.permissions import IsRelatedToUserOrReadOnly

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.prefetch_related("media").all()
    serializer_class = ActivitySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "update":
            permissions += [IsRelatedToUserOrReadOnly("user")]
        return permissions

    def get_queryset(self):
        current_user = self.request.user
        is_visible = Q(user=current_user) | Q(is_published=True)
        queryset = Activity.objects.filter(is_visible)
        return queryset
