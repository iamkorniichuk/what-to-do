from django.db import models
from django.contrib.auth import get_user_model

from activities.models import Activity


User = get_user_model()


class Booking(models.Model):
    appointment_datetime = models.DateTimeField()
    activity = models.ForeignKey(
        Activity,
        models.CASCADE,
        related_name="bookings",
    )
    booked_by = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="bookings",
    )

    def __str__(self):
        return self.pk
