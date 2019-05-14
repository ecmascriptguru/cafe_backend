from django.db.models.signals import post_save
from django.dispatch import receiver
from cafe_backend.mgnt.chat.models import Channel, CHAT_ROOM_TYPE
from .models import User


@receiver(post_save, sender=User)
def create_attendee_for_new_user(sender, instance, created, **kwargs):
    if created:
        channel, created = Channel.objects.get_or_create(
            name='Public', channel_type=CHAT_ROOM_TYPE.public)
        channel.attendees.create(user=instance)
