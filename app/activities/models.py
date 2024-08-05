from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Activity(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")
    user = models.ForeignKey(User, models.CASCADE, related_name="activities")
    is_published = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name
