# Generated by Django 5.1.7 on 2025-03-25 07:39

from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class TrgmExtension(CreateExtension):
    def __init__(self):
        self.name = "pg_trgm"


class Migration(migrations.Migration):
    dependencies = [
        ("commons", "0002_pgvector"),
    ]

    operations = [
        TrgmExtension(),
    ]
