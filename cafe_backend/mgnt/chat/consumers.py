import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from cafe_backend.apps.users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_pk = self.scope['url_route']['kwargs']['user_pk']
        self.room_group_name = 'default_room'
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
        text_data_json = json.loads(text_data)
        to = text_data_json.get('to', None)

        # Get or create channel between 2 users
        channel, created = self.user.get_channel(to)
        if created:
            # Inform invitation to a channel.
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'channel.new',
                    'message': "You've invited by %s." % channel.name,
                    'from': self.user.to_json(),
                    'to': to
                }
            )

        # Send message to room group
        message = text_data_json['message']
        msg_object = channel.messages.create(
            poster=self.user, content=message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg_object.to_json(),
                'to': to,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
