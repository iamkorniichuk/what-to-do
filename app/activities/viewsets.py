from django.db.models import Q
from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUserOrReadOnly

from interactions.models import Interaction
from interactions.serializers import InteractionSerializer

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.prefetch_related("media").all()
    serializer_class = ActivitySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        permissions = super().get_permissions() + [
            IsRelatedToUserOrReadOnly("created_by")
        ]
        return permissions

    def get_queryset(self):
        current_user = self.request.user
        is_visible = Q(created_by=current_user) | Q(is_published=True)
        queryset = Activity.objects.filter(is_visible)
        return queryset

    @action(["post"], detail=True)
    def like(self, request, pk=None):
        interaction_type = Interaction.TypeChoices.LIKE
        return self.request_set_interaction(interaction_type)

    @action(["post"], detail=True)
    def dislike(self, request, pk=None):
        interaction_type = Interaction.TypeChoices.DISLIKE
        return self.request_set_interaction(interaction_type)

    def request_set_interaction(self, interaction_type):
        user = self.request.user
        activity = self.get_object()

        obj, _ = Interaction.objects.update_or_create(
            created_by=user,
            activity=activity,
            defaults={"type": interaction_type},
        )

        serializer = InteractionSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
