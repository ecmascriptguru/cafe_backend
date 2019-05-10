from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Event


class EventSerializer(CafeModelSerializer):
    class Meta:
        model = Event
        exclude = ('created', 'updated', 'type', 'repeat',)
