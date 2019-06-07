from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Video


class VideoSerializer(CafeModelSerializer):
    class Meta:
        model = Video
        exclude = (
            'created', 'modified', )
