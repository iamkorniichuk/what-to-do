from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Configuration


User = get_user_model()


@receiver(post_save, sender=User)
def create_configuration(sender, instance, created, *args, **kwargs):
    if not created:
        return

    Configuration.objects.create(related_to=instance)
