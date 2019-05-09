from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Advertisement


class AdsSerializer(CafeModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'name', 'url', 'type', )
