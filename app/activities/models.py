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


class InteractionTypes(models.IntegerChoices):
    LIKE = 0, "Like"
    DISLIKE = 1, "Dislike"
    WATCH_LATER = 2, "Watch Later"


class Interaction(models.Model):
    class Meta:
        unique_together = [
            ("activity", "user"),
        ]

    activity = models.ForeignKey(Activity, models.CASCADE, related_name="interactions")
    user = models.ForeignKey(User, models.CASCADE, related_name="interactions")
    type = models.PositiveSmallIntegerField(choices=InteractionTypes.choices)

    def __str__(self):
        return f"{self.get_type_display()}: {self.user}-{self.activity}"
