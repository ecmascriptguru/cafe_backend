from cafe_backend.core.apis.serializers import (
    CafeModelSerializer, serializers)
from .models import Channel, CHANNEL_TYPE_CHOICES


class ChannelSerializer(CafeModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
