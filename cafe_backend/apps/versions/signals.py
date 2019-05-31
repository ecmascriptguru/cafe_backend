from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Version


@receiver(post_delete, sender=Version)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)
