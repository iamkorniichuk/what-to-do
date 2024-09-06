from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_around.permissions import IsRelatedToUserOrReadOnly
from drf_around.mixins import OverrideDataMixin

from .models import Activity, InteractionTypes, Interaction
from .serializers import ActivitySerializer


class ActivityViewSet(OverrideDataMixin, ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        return self.create_interaction(InteractionTypes.LIKE)

    @action(methods=["post"], detail=True)
    def dislike(self, request, pk=None):
        return self.create_interaction(InteractionTypes.DISLIKE)

    @action(methods=["post"], detail=True)
    def watch_later(self, request, pk=None):
        return self.create_interaction(InteractionTypes.WATCH_LATER)

    def create_interaction(self, type):
        activity = self.get_object()
        user = self.request.user
        Interaction.objects.create(
            activity=activity,
            user=user,
            type=type,
        )
        serializer = self.get_serializer(activity)
        return Response(serializer.data)

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"current_user": self.request.user})
        return context
