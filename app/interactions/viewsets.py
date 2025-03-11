from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUser

from .serializers import Interaction, InteractionSerializer


class InteractionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Interaction.objects.prefetch_related("activity").all()
    serializer_class = InteractionSerializer

    def get_permissions(self):
        permissions = super().get_permissions() + [IsRelatedToUser("created_by")]
        return permissions

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user

        queryset = self.get_queryset()
        queryset = queryset.filter(created_by=current_user).all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
