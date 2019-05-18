from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Attendee, CHAT_ROOM_TYPE


@receiver(post_delete, sender=Attendee)
def delete_channels_with_attendee_delete(sender, instance, **kwargs):
    count = 0
    if instance.channel.channel_type == CHAT_ROOM_TYPE.private:
        instance.channel.delete()
