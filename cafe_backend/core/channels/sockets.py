import json
import asyncio
import websockets
from django.conf import settings
from cafe_backend.core.constants.types import SOCKET_MESSAGE_TYPE
from cafe_backend.apps.users.models import User
from cafe_backend.mgnt.chat.models import Channel, CHAT_ROOM_TYPE
from cafe_backend.apps.videos.models import Video


async def send_message_to_socket_server(uri, message):
    """Send message to socket server specified by parameters
    - uri: String       uri of socket server with path
    - message: JSON     Message to be sent to the socket.
    """
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))


def send_message_to_mobile(from_user, message):
    """Shortcut to send message as a user specified by parameter
    - from_user: User PK    Primary key of sender
    - message: JSON         Message to be send
    """
    asyncio.get_event_loop().run_until_complete(
        send_message_to_socket_server(
            '%s/ws/chat/%d/' % (settings.SOCKET_SERVER_HOST, from_user),
            message))


def broadcast_events(events):
    admin = User.objects.filter(is_superuser=True).first()
    public_channel = Channel.get_public_channel()

    count = 0
    for event in events:
        message = {
            "type": SOCKET_MESSAGE_TYPE.event,
            "event": event.pk, 'to': public_channel.pk}
        try:
            send_message_to_mobile(admin.pk, message)
            count += 1
        except Exception as e:
            pass
    return count


def broadcast_table_changes(table_pk):
    admin = User.objects.filter(is_superuser=True).first()
    public_channel = Channel.get_public_channel()

    count = 0
    message = {
        "type": SOCKET_MESSAGE_TYPE.table,
        "table": table_pk, 'to': public_channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        pass


def broadcast_order_status(order, created):
    admin = User.objects.filter(is_superuser=True).first()
    table_user = order.table.user
    channel = Channel.objects.filter(
        channel_type=CHAT_ROOM_TYPE.private,
        attendees__user__pk=table_user.pk).first()
    message = {
        "type": SOCKET_MESSAGE_TYPE.order,
        "created": created, "order": order.pk,
        "to": channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        print(str(e))


def broadcast_order_item_status(order_item, created):
    admin = User.objects.filter(is_superuser=True).first()
    table_user = order_item.order.table.user
    channel = Channel.objects.filter(
        channel_type=CHAT_ROOM_TYPE.private,
        attendees__user__pk=table_user.pk).first()
    message = {
        "type": SOCKET_MESSAGE_TYPE.order_item,
        "created": created, "order_item": order_item.pk,
        "to": channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        print(str(e))


def notify_dish_booking_status(order_item, created):
    admin = User.objects.filter(is_superuser=True).first()
    from_table = order_item.order.table
    to_table = order_item.to_table
    channel = Channel.objects.filter(
        channel_type=CHAT_ROOM_TYPE.private,
        attendees__user__pk=to_table.user.pk).first()
    message = {
        "type": SOCKET_MESSAGE_TYPE.dish_booking,
        "created": created, "order_item": order_item.pk,
        "from_table": from_table.pk,
        "to": channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        print(str(e))


def send_ringtone_to_admin(table):
    admin = User.objects.filter(is_superuser=True).first()
    table_user = table.user
    channel = Channel.objects.filter(
        channel_type=CHAT_ROOM_TYPE.private,
        attendees__user__pk=table_user.pk).first()
    message = {
        "type": SOCKET_MESSAGE_TYPE.ring, "table": table.pk,
        "to": channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        print(str(e))


def broadcast_video_event(video_pk):
    admin = User.objects.filter(is_superuser=True).first()
    public_channel = Channel.get_public_channel()

    count = 0
    message = {
        "type": SOCKET_MESSAGE_TYPE.video_event,
        "video": video_pk, 'to': public_channel.pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        pass
