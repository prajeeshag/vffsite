from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, TOTPDevice

@receiver(post_save, sender=User)
def create_TOTPDevice(sender, instance, created, **kwargs):
    if created:
        TOTPDevice.objects.create(user=instance)