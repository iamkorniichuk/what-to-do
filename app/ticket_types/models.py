from django.db import models
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

from activities.models import Activity
from tickets.models import Ticket


User = get_user_model()


class TicketTypeManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()

        available_tickets = Ticket.objects.filter(booked_by__isnull=True)
        queryset = queryset.prefetch_related(
            Prefetch(
                "tickets",
                queryset=available_tickets,
                to_attr="available_tickets",
            )
        )
        return queryset


class TicketType(models.Model):
    class Meta:
        unique_together = [
            ("name", "activity"),
        ]

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    activity = models.ForeignKey(Activity, models.CASCADE, related_name="ticket_types")

    objects = TicketTypeManager()

    def __str__(self):
        return self.name
