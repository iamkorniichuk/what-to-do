# Generated by Django 5.1.7 on 2025-03-24 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("territories", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="territory",
            name="code",
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
