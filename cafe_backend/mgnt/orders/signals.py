from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem
from .tasks import send_changed_order, send_changed_order_item


@receiver(post_save, sender=Order)
def send_order_status(sender, instance, created, **kwargs):
    send_changed_order.delay(instance.pk, created)


# @receiver(post_save, sender=OrderItem)
# def send_order_item_status(sender, instance, created, **kwargs):
#     send_changed_order_item.delay(instance.pk, created)
