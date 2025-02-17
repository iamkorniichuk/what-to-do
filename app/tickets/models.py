from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid4,
        editable=False,
    )
    type = models.ForeignKey(
        "ticket_types.TicketType",
        models.CASCADE,
        related_name="tickets",
    )
    booked_by = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    def __str__(self):
        return f"{self.booked_by} -> {self.type}"
