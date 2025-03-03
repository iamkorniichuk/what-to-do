from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Configuration(models.Model):
    is_remote_allowed = models.BooleanField(default=True, blank=True)
    allowed_distance = models.FloatField(default=10, blank=True)
    start_location = models.PointField(srid=4326, null=True, blank=True)
    related_to = models.OneToOneField(
        User,
        models.CASCADE,
        related_name="configuration",
    )

    def __str__(self):
        return str(self.related_to)
