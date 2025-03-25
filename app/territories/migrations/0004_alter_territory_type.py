# Generated by Django 5.1.7 on 2025-03-25 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("territories", "0003_territory_name_trigram_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="territory",
            name="type",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "country"),
                    (1, "region"),
                    (2, "district"),
                    (3, "community"),
                    (4, "settlement"),
                ]
            ),
        ),
    ]
