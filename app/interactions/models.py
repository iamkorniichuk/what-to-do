from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model

from activities.models import Activity


User = get_user_model()


class InteractionManager(models.Manager):
    like_weight = 1.0
    dislike_weight = 0.5

    def get_user_embedding(self, user):
        if user is None:
            return None

        queryset = self.get_queryset().filter(created_by=user)
        queryset = queryset.annotate(
            weighted_embedding=models.Case(
                models.When(
                    type=Interaction.TypeChoices.LIKE,
                    then=models.F("activity.embedding") * self.like_weight,
                ),
                models.When(
                    type=Interaction.TypeChoices.DISLIKE,
                    then=models.F("activity.embedding") * -self.dislike_weight,
                ),
            )
        )

        user_embedding = queryset.aggregate(
            user_embedding=Coalesce(
                models.Avg("weighted_embedding"), models.Value(None)
            )
        )["user_embedding"]
        return user_embedding


class Interaction(models.Model):
    class Meta:
        ordering = ["created_at"]
        unique_together = [
            ("activity", "created_by"),
        ]

    class TypeChoices(models.IntegerChoices):
        LIKE = 0, "like"
        DISLIKE = 1, "dislike"

    type = models.PositiveSmallIntegerField(choices=TypeChoices.choices)
    activity = models.ForeignKey(Activity, models.CASCADE, related_name="interactions")
    created_by = models.ForeignKey(User, models.CASCADE, related_name="interactions")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = InteractionManager()

    def __str__(self):
        return f"{self.get_type_display()}: {self.created_by} -> {self.activity}"
