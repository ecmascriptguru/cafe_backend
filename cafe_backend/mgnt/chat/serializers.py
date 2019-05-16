from cafe_backend.core.apis.serializers import (
    CafeModelSerializer, serializers)
from .models import Channel, CHANNEL_TYPE_CHOICES, Message


class MessageSerializer(CafeModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChannelSerializer(CafeModelSerializer):
    message_set = MessageSerializer(
        many=True, source='quick_messages', read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'message_set', 'channel_type', )
