from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from activities.models import Activity


User = get_user_model()


class InteractionTypes(models.IntegerChoices):
    LIKE = 0, "like"
    DISLIKE = 1, "dislike"


class Interaction(models.Model):
    class Meta:
        ordering = ["created_at"]
        unique_together = [
            ("activity", "user"),
        ]

    activity = models.ForeignKey(Activity, models.CASCADE, related_name="interactions")
    user = models.ForeignKey(User, models.CASCADE, related_name="interactions")
    type = models.PositiveSmallIntegerField(choices=InteractionTypes.choices)
    created_at = models.DateTimeField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()}: {self.user} -> {self.activity}"
