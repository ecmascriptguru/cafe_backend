from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Event


@receiver(post_delete, sender=Event)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)
