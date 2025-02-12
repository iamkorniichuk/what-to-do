# Generated by Django 5.1 on 2025-01-18 17:51

import commons.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField(blank=True, default="")),
                ("is_published", models.BooleanField(blank=True, default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActivityMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="activities/",
                        validators=[
                            commons.validators.FileSizeValidator(31457280),
                            commons.validators.ContentTypeValidator(
                                "image/heic",
                                "image/heif",
                                "image/jpeg",
                                "image/png",
                                "video/mp4",
                                "video/webm",
                            ),
                        ],
                    ),
                ),
                ("order", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media",
                        to="activities.activity",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
