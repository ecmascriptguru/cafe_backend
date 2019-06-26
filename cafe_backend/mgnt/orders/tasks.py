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
def print_order(order_pk, item_ids=[], print_all=False):
    order = Order.objects.get(pk=order_pk)
    if print_all:
        url = "%s%s" % (
                settings.HOSTNAME,
                reverse_lazy(
                    'orders:order_full_printview', kwargs={'pk': order_pk})
            )

        if settings.DEBUG:
            print("Printing full order", url)
        else:
            response = EYPrint.print_58(url)
            json_data = response.json()
    else:
        items = order.items.filter(pk__in=item_ids)

        if len(items) > 0:
            url = "%s%s?items=%s" % (
                settings.HOSTNAME,
                reverse_lazy(
                    'orders:order_printview', kwargs={'pk': order_pk}),
                '+'.join([str(id) for id in item_ids])
            )

            if settings.DEBUG:
                print("Printing order", url)
            else:
                response = EYPrint.print_58(url)
                json_data = response.json()
                if json_data.get('result') == 'success':
                    order.print_items.update(is_printed=True)


@shared_task
def print_order_item(order_item_pk):
    time.sleep(1)
    item = OrderItem.objects.get(pk=order_item_pk)
    url = "%s%s" % (
        settings.HOSTNAME, reverse_lazy(
            'orders:order_item_printview', kwargs={'pk': order_item_pk}
        ))
    if not settings.DEBUG:
        EYPrint.print_80(url)
    else:
        print("Printing order item", url)


@shared_task
def mark_order_items_as_printed(order_item_ids):
    time.sleep(10)
    return OrderItem.objects.filter(pk__in=order_item_ids).update(
        is_printed=True)


@shared_task
def print_orders(order_ids):
    orders = Order.objects.filter(pk__in=order_ids)
    if len(orders) > 0:
        url = "%s%s?orders=%s" % (
            settings.HOSTNAME,
            reverse_lazy(
                'orders:orders_printview'),
            '+'.join([str(id) for id in order_ids])
        )

        if settings.DEBUG:
            print("Printing orders", url)
        else:
            response = EYPrint.print_58(url)
            json_data = response.json()
            return json_data
    else:
        return "Skipping Blank Data in printing orders report."
