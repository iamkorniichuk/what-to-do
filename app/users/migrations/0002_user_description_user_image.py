# Generated by Django 5.1 on 2025-01-19 12:25

import commons.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="users/",
                validators=[
                    commons.validators.FileSizeValidator(15728640),
                    commons.validators.ContentTypeValidator(
                        "image/heic", "image/heif", "image/jpeg", "image/png"
                    ),
                ],
            ),
        ),
    ]
