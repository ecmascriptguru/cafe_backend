from celery import shared_task
from ...core.channels.sockets import broadcast_order_status
from .models import Order


@shared_task
def send_changed_order(order_pk, created):
    order = Order.objects.get(pk=order_pk)
    print(order)
    broadcast_order_status(order, created)
