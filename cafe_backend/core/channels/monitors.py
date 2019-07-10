import json
import asyncio
import websockets
from django.conf import settings
from cafe_backend.core.constants.types import MONITOR_MESSAGE_TYPE
from cafe_backend.apps.users.models import User


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
            '%s/ws/monitor/%d/' % (settings.SOCKET_SERVER_HOST, from_user),
            message))


def send_table_command(table_pk, command):
    admin = User.objects.filter(is_superuser=True).first()

    message = {
        "type": command, 'to': table_pk}
    try:
        send_message_to_mobile(admin.pk, message)
    except Exception as e:
        pass
