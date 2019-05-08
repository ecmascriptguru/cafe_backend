from cafe_backend.core.apis.serializers import serializers, CafeModelSerializer
from .models import Table


class TableSerializer(CafeModelSerializer):
    class Meta:
        model = Table
        fields = ('pk', 'name', 'size', 'female', 'male', )
        extra_kwargs = {
            'name': {'read_only': True},
            'size': {'read_only': True},
            'male': {'read_only': True},
            'female': {'read_only': True}}
