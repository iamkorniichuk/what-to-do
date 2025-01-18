from rest_framework import viewsets

from commons.permissions import IsRelatedToUser

from .models import Interaction
from .serializers import InteractionSerializer


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer

    def get_permissions(self):
        permissions = super().get_permissions() + [IsRelatedToUser("user")]
        return permissions

    def get_queryset(self):
        current_user = self.request.user
        queryset = (
            Interaction.objects.prefetch_related("activity")
            .filter(user=current_user)
            .all()
        )
        return queryset