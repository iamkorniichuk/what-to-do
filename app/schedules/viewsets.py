from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from commons.permissions import IsRelatedToUserOrReadOnly

from .serializers import Schedule, ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        permissions = super().get_permissions() + [
            IsRelatedToUserOrReadOnly("created_by"),
        ]
        return permissions

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user

        queryset = self.get_queryset()
        queryset = queryset.filter(created_by=current_user).all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
