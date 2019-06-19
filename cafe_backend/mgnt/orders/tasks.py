import time
from celery import shared_task
from django.conf import settings
from django.urls import reverse_lazy
from ...core.channels.sockets import (
    broadcast_order_status, broadcast_order_item_status,
    notify_dish_booking_status)
from ...libs.printer.eyprint import EYPrint
from .models import Order, OrderItem


@shared_task
def send_changed_order(order_pk, created):
    order = Order.objects.get(pk=order_pk)
    broadcast_order_status(order, created)


@shared_task
def send_changed_order_item(order_item_pk, created):
    time.sleep(1)
    order_item = OrderItem.objects.get(pk=order_item_pk)
    broadcast_order_item_status(order_item, created)


@shared_task
def send_dish_booking_status(order_item_pk, created):
    order_item = OrderItem.objects.get(pk=order_item_pk)
    notify_dish_booking_status(order_item, created)


@shared_task
def print_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    items = order.print_items.all()
    if len(items) > 0:
        url = "%s%s" % (
            settings.HOSTNAME, reverse_lazy(
                'orders:order_printview', kwargs={'pk': order_pk})
        )
        callback_url = "%s%s" % (
            settings.HOSTNAME, reverse_lazy(
                'orders:order_print_callbackview', kwargs={'pk': order_pk})
        )

        response = EYPrint.print_58(url, callback=callback_url)
        json_data = response.json()
        if json_data.get('result') == 'success':
            time.sleep(20)
            order.print_items.update(is_printed=True)


@shared_task
def print_order_item(order_item_pk):
    time.sleep(1)
    item = OrderItem.objects.get(pk=order_item_pk)
    url = "%s%s" % (
        settings.HOSTNAME, reverse_lazy(
            'orders:order_item_printview', kwargs={'pk': order_item_pk}
        ))
    EYPrint.print_80(url)


@shared_task
def mark_order_items_as_printed(order_item_ids):
    time.sleep(10)
    return OrderItem.objects.filter(pk__in=order_item_ids).update(
        is_printed=True)
