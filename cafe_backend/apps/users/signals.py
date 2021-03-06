from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cafe_backend.mgnt.chat.models import Channel, CHAT_ROOM_TYPE
from ...mgnt.orders.models import Order
from .models import User, Table, TABLE_STATE
from .tasks import send_table_change_to_all


@receiver(post_save, sender=User)
def create_channels_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Create public channel
        channel = Channel.get_public_channel()
        channel.attendees.create(user=instance)


@receiver(post_save, sender=Table)
def create_channes_for_new_table(sender, instance, created, **kwargs):
    if created:
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
    else:
        # Should send message via socket.
        send_table_change_to_all.delay(instance.pk)

    # if instance.state == TABLE_STATE.using and instance.order is None:
    #     Order.objects.create(table=instance)

    # if instance.order is not None:
    #     order = instance.order
    #     order.details['customers'] = {
    #         'male': instance.male,
    #         'female': instance.female}
    #     order.save()


@receiver(post_delete, sender=Table)
def delete_user_with_table_delete(sender, instance, **kwargs):
    if instance.user is not None:
        instance.user.delete()
