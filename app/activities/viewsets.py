from django.shortcuts import get_object_or_404
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
        queryset = Activity.objects.filter(is_published=True)
        return queryset

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user

        queryset = Activity.objects.filter(created_by=current_user).all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=True)
    def like(self, request, pk=None):
        interaction_type = Interaction.TypeChoices.LIKE
        return self.request_set_interaction(request, pk, interaction_type)

    @action(["post"], detail=True)
    def dislike(self, request, pk=None):
        interaction_type = Interaction.TypeChoices.DISLIKE
        return self.request_set_interaction(request, pk, interaction_type)

    def request_set_interaction(self, request, activity_pk, interaction_type):
        current_user = request.user
        # Don't use `self.get_object()` to avoid object permissions' checks
        activity = get_object_or_404(Activity, pk=activity_pk)

        obj, _ = Interaction.objects.update_or_create(
            created_by=current_user,
            activity=activity,
            defaults={"type": interaction_type},
        )

        serializer = InteractionSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
