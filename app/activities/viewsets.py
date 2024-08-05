from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from drf_around.permissions import IsRelatedToUserOrReadOnly
from drf_around.mixins import OverrideDataMixin

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(OverrideDataMixin, ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_overriding_data(self):
        current_user = self.request.user
        data = {"user": current_user.pk}
        return data

    def get_queryset(self):
        current_user = self.request.user
        available_filter = Q(user=current_user) | Q(is_published=True)
        queryset = Activity.objects.filter(available_filter)
        return queryset

    def get_permissions(self):
        permissions = super().get_permissions() + [IsRelatedToUserOrReadOnly("user")]
        return permissions
