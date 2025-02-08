from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.GenericViewSet):
    queryset = Ticket.objects.all()

    @action(["get"], detail=False)
    def my(self, request):
        current_user = request.user
        queryset = Ticket.objects.filter(booked_by=current_user).all()

        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
