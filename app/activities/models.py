from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from pgvector.django import VectorField
from pgvector.django import L2Distance

from commons.validators import ContentTypeValidator, FileSizeValidator

from schedules.models import Schedule


User = get_user_model()


class ActivityManager(models.Manager):
    def order_by_embedding_distance(self, embedding):
        queryset = (
            self.get_queryset()
            .alias(distance=L2Distance("embedding", embedding))
            .order_by("distance")
        )
        return queryset


class ActivityTypeChoices(models.IntegerChoices):
    RECURRING = 0, "recurring"
    ONE_TIME = 1, "one-time"


class Activity(models.Model):
    class Meta:
        default_related_name = "activities"

    default_type_choice = None

    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.CASCADE)
    location = models.PointField(srid=4326, null=True, blank=True)
    type = models.PositiveSmallIntegerField(
        editable=False,
        blank=True,
        choices=ActivityTypeChoices,
        default=default_type_choice,
    )
    duration = models.DurationField()
    embedding = VectorField()

    objects = ActivityManager()

    def __str__(self):
        return self.name


class ActivityMedia(models.Model):
    class Meta:
        ordering = ["order"]

    activity = models.ForeignKey(Activity, models.CASCADE, related_name="media")
    file = models.FileField(
        upload_to="activities/",
        validators=[
            FileSizeValidator(30 * 1024 * 1024),
            ContentTypeValidator(
                "image/heic",
                "image/heif",
                "image/jpeg",
                "image/png",
                "video/mp4",
                "video/webm",
            ),
        ],
    )
    order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity} -> {self.order}"


class RecurringActivity(Activity):
    class Meta:
        default_related_name = "recurring_activities"

    default_type_choice = ActivityTypeChoices.RECURRING

    schedule = models.ForeignKey(Schedule, models.PROTECT)
