import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from cafe_backend.core.constants.types import SOCKET_MESSAGE_TYPE
from ...apps.users.models import User, Table
from ...apps.events.models import Event
from ...mgnt.orders.models import Order, OrderItem


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
        json_data = json.loads(text_data)
        to = json_data.get('to', None)

        # Get or create channel between 2 users
        channel = self.user.get_channel(to)
        message_type = json_data.get('type', SOCKET_MESSAGE_TYPE.chat)

        if message_type == SOCKET_MESSAGE_TYPE.chat:
            # Send message to room group
            message = json_data['message']
            msg_object = channel.messages.create(
                poster=self.user, content=message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': message_type,
                    'message': msg_object.to_json(),
                    'to': to,
                }
            )
        elif message_type == SOCKET_MESSAGE_TYPE.event:
            event_pk = json_data['event']
            event = Event.objects.get(pk=event_pk)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': message_type,
                    'to': to,
                    'event': event.to_json()
                }
            )
        elif message_type == SOCKET_MESSAGE_TYPE.order:
            order_pk = json_data['order']
            created = json_data['created']
            order = Order.objects.get(pk=order_pk)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': message_type,
                    'to': to,
                    'created': created,
                    'order': order.to_json()
                }
            )
        elif message_type == SOCKET_MESSAGE_TYPE.order_item:
            order_item_pk = json_data['order']
            created = json_data['created']
            order_item = OrderItem.objects.get(pk=order_item_pk)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': message_type,
                    'to': to,
                    'created': created,
                    'order': order_item.to_json()
                }
            )
        elif message_type == SOCKET_MESSAGE_TYPE.qr_code:
            qr_code = json_data['qr_code']
            message = json_data['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': message_type,
                    'message': {
                        "poster": self.user.pk,
                        "poster_name": self.user.first_name,
                        "content": message,
                    },
                    'qr_code': qr_code,
                    'to': to,
                }
            )
        elif message_type == SOCKET_MESSAGE_TYPE.ring:
            table_pk = json_data['table']
            table = Table.objects.get(pk=table_pk)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': message_type,
                    'table': table.to_json(),
                    'to': to,
                }
            )
        else:
            print("UNKNOWN MESSAGE FOUND!")

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def notification_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def notification_order(self, event):
        await self.send(text_data=json.dumps(event))

    async def notification_order_item(self, event):
        await self.send(text_data=json.dumps(event))

    async def qr_code(self, event):
        await self.send(text_data=json.dumps(event))

    async def ring(self, event):
        await self.send(text_data=json.dumps(event))
