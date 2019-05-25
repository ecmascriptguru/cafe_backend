from celery import shared_task
from ...core.channels.sockets import (
    broadcast_order_status, broadcast_order_item_status,
    notify_dish_booking_status)
from .models import Order, OrderItem


@shared_task
def send_changed_order(order_pk, created):
    order = Order.objects.get(pk=order_pk)
    broadcast_order_status(order, created)


@shared_task
def send_changed_order_item(order_item_pk, created):
    order_item = OrderItem.objects.get(pk=order_item_pk)
    broadcast_order_item_status(order_item, created)


@shared_task
def send_dish_booking_status(order_item_pk, created):
    order_item = OrderItem.objects.get(pk=order_item_pk)
    notify_dish_booking_status(order_item, created)
