# Generated by Django 5.1.7 on 2025-03-25 09:43

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("territories", "0002_alter_territory_code"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="territory",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"], name="name_trigram_index", opclasses=("gin_trgm_ops",)
            ),
        ),
    ]
