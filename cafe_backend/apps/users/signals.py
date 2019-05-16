from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cafe_backend.mgnt.chat.models import Channel, CHAT_ROOM_TYPE
from .models import User, Table


@receiver(post_save, sender=User)
def create_attendee_for_new_user(sender, instance, created, **kwargs):
    if created:
        channel = Channel.get_public_channel()
        channel.attendees.create(user=instance)


@receiver(post_delete, sender=Table)
def delete_user_with_table_delete(sender, instance, **kwargs):
    instance.user.delete()
