import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from cafe_backend.core.constants.types import MONITOR_MESSAGE_TYPE
from ...apps.users.models import User, Table


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_pk = self.scope['url_route']['kwargs']['user_pk']
        self.room_group_name = 'system_monitor_room'
        self.user = User.objects.get(pk=user_pk)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        to = json_data.get('to', None)

        message_type = json_data.get('type', MONITOR_MESSAGE_TYPE.start)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message_type,
                'to': to,
            }
        )

    async def start(self, event):
        await self.send(text_data=json.dumps(event))

    async def stop(self, event):
        await self.send(text_data=json.dumps(event))

    async def reboot(self, event):
        await self.send(text_data=json.dumps(event))
