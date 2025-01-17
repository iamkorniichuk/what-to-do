from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, parsers

from .models import Activity, InteractionTypes, Interaction
from .serializers import ActivitySerializer
from .permissions import IsRelatedToUserOrReadOnly


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.prefetch_related("media").all()
    serializer_class = ActivitySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "update":
            permissions += [IsRelatedToUserOrReadOnly("user")]
        return permissions

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        return self.set_interaction(InteractionTypes.LIKE)

    @action(methods=["post"], detail=True)
    def dislike(self, request, pk=None):
        return self.set_interaction(InteractionTypes.DISLIKE)

    @action(methods=["post"], detail=True)
    def watch_later(self, request, pk=None):
        return self.set_interaction(InteractionTypes.WATCH_LATER)

    def set_interaction(self, interaction_type):
        current_activity = self.get_object()
        current_user = self.request.user

        Interaction.objects.update_or_create(
            activity=current_activity,
            user=current_user,
            defaults={"type": interaction_type},
        )
        serializer = self.get_serializer(current_activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        current_user = self.request.user
        available_filter = Q(user=current_user) | Q(is_published=True)
        queryset = Activity.objects.filter(available_filter)
        return queryset
