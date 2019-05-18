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

        if instance.is_table:
            users = User.objects.filter(is_table=True).exclude(table=None)
            count = 1
            # Create its own channel
            channel = Channel.objects.create(
                name=instance.first_name,
                channel_type=CHAT_ROOM_TYPE.private)
            channel.attendees.create(user=instance)
            for t2 in users:
                channel = Channel.objects.create(
                    name="%s-%s" % (instance.first_name, t2.first_name),
                    channel_type=CHAT_ROOM_TYPE.private)
                channel.attendees.create(user=instance)
                channel.attendees.create(user=t2)
                count += 1

        print("%d attendees for private channels created successfully." % count)


@receiver(post_delete, sender=Table)
def delete_user_with_table_delete(sender, instance, **kwargs):
    instance.user.delete()
