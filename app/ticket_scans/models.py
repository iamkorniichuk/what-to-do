import uuid  # NOQA
from django.db import models

from activities.models import Activity
from tickets.models import Ticket


class TicketScan(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        models.CASCADE,
        related_name="ticket_scans",
    )
    activity = models.ForeignKey(
        Activity,
        models.CASCADE,
        related_name="ticket_scans",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.ticket} {self.created_at}"
