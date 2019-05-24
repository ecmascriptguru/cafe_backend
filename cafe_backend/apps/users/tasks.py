from celery import shared_task
from ...core.channels.sockets import (
    send_ringtone_to_admin, broadcast_table_changes)
from .models import Table


@shared_task
def send_ringtone_alarm_to_admin(table_pk):
    table = Table.objects.get(pk=table_pk)
    send_ringtone_to_admin(table)


@shared_task
def send_table_change_to_all(table_pk):
    broadcast_table_changes(table_pk)
