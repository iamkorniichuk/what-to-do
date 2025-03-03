from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUserOrReadOnly
from configurations.permissions import HasFilledConfiguration

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.prefetch_related("media").all()
    serializer_class = ActivitySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        permissions = super().get_permissions() + [
            IsRelatedToUserOrReadOnly("created_by"),
            HasFilledConfiguration(),
        ]
        return permissions

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user

        queryset = self.get_queryset()
        queryset = queryset.filter(created_by=current_user).all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
