from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem
from ...apps.users.models import Table, TABLE_STATE
from ...core.constants.types import DISH_POSITION
from .tasks import (
    send_changed_order, send_changed_order_item, send_dish_booking_status,
    print_order, print_order_item)


@receiver(post_save, sender=Order)
def send_order_status(sender, instance, created, **kwargs):
    send_changed_order.delay(instance.pk, created)
    if created:
        if instance.table.state == TABLE_STATE.blank:
            table = instance.table
            table.state = TABLE_STATE.reserved
            table.save()

    if len(instance.print_items) > 0:
        ids = [item.pk for item in instance.print_items]
        print_order.delay(instance.pk, ids)


@receiver(post_save, sender=OrderItem)
def send_order_item_status(sender, instance, created, **kwargs):
    send_changed_order_item.delay(instance.pk, created)
    if instance.is_booking_order_item():
        send_dish_booking_status.delay(instance.pk, created)

    if created:
        if instance.order.table.state == TABLE_STATE.blank:
            instance.order.table.state = TABLE_STATE.reserved
            instance.order.table.save()

        if instance.dish.position == DISH_POSITION.chicken:
            print_order_item.delay(instance.pk)
