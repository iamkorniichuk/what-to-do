from django.db import models
from django.contrib.auth import get_user_model

from .validators import ContentTypeValidator, FileSizeValidator


User = get_user_model()


class Activity(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")
    user = models.ForeignKey(User, models.CASCADE, related_name="activities")
    is_published = models.BooleanField(default=False, blank=True)

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
