from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cafe_backend.mgnt.chat.models import Channel, CHAT_ROOM_TYPE
from .models import User, Table


@receiver(post_save, sender=User)
def create_channels_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Create public channel
        channel = Channel.get_public_channel()
        channel.attendees.create(user=instance)


@receiver(post_save, sender=Table)
def create_channes_for_new_table(sender, instance, created, **kwargs):
    tables = Table.objects.all()
    # Create its own channel
    channel = Channel.objects.create(
        name=instance.name,
        channel_type=CHAT_ROOM_TYPE.private)
    channel.attendees.create(user=instance.user)
    for t2 in tables:
        channel = Channel.objects.create(
            name="%s-%s" % (instance.name, t2.name),
            channel_type=CHAT_ROOM_TYPE.private)
        channel.attendees.get_or_create(user=instance.user)
        channel.attendees.get_or_create(user=t2.user)


@receiver(post_delete, sender=Table)
def delete_user_with_table_delete(sender, instance, **kwargs):
    if instance.user is not None:
        instance.user.delete()
