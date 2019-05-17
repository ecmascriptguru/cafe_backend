import json
import asyncio
import websockets
from django.conf import settings
from cafe_backend.core.constants.types import SOCKET_MESSAGE_TYPE
from cafe_backend.apps.users.models import User
from cafe_backend.mgnt.chat.models import Channel


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
