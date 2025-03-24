# Generated by Django 5.1.7 on 2025-03-24 08:18

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Territory",
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
                ("code", models.CharField(max_length=10, unique=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "boundaries",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "country"),
                            (1, "region"),
                            (2, "district"),
                            (3, "settlement"),
                        ]
                    ),
                ),
                (
                    "upper_level",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lower_levels",
                        to="territories.territory",
                    ),
                ),
            ],
        ),
    ]
