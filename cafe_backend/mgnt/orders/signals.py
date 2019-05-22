from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order
from .tasks import send_changed_order


@receiver(post_save, sender=Order)
def send_order_status(sender, instance, created, **kwargs):
    send_changed_order.delay(instance.pk, created)
