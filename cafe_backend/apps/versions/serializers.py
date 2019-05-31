from ...core.apis.serializers import serializers, CafeModelSerializer
from .models import Version


class VersionSerializer(CafeModelSerializer):
    class Meta:
        model = Version
        fields = ('name', 'release_note', 'download_url', )
