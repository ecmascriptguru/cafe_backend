from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Emoticon


class EmoticonSerializer(CafeModelSerializer):
    class Meta:
        model = Emoticon
        exclude = (
            'created', 'modified', )
