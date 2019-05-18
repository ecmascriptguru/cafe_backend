from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Music
from .tasks import grab_music_to_s3


@receiver(post_save, sender=Music)
def copy_music_to_s3(sender, instance, created, **kwargs):
    if created:
        grab_music_to_s3.delay([instance.pk])
