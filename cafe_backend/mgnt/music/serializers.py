from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from cafe_backend.apps.users.serializers import TableSerializer
from .models import Music, Playlist


class MusicSerializer(CafeModelSerializer):
    music_url = serializers.URLField(read_only=True)

    class Meta:
        model = Music
        fields = '__all__'
        extra_kwargs = {
            'title': {'read_only': True},
            'author': {'read_only': True},
            'url': {'read_only': True},
            'pic_url': {'read_only': True},
        }

    def create(self, validated_data):
        exist, instance = Music.exists(validated_data['external_id'])
        if exist:
            super(MusicSerializer, self).create(validated_data)
        else:
            success, instance = Music.find_music(validated_data['external_id'])
            if not success:
                raise serializers.ValidationError({
                    'external_id': ['Invalid. Song not found.']})
            return instance


class PlaylistSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(
        source='get_customer_name', read_only=True)
    title = serializers.StringRelatedField(
        source='get_title', read_only=True)
    url = serializers.StringRelatedField(
        source='get_url', read_only=True)
    picture = serializers.StringRelatedField(
        source='get_pic_url', read_only=True)

    class Meta:
        model = Playlist
        fields = ('customer', 'title', 'url', 'picture', 'created',)


class MusicSubscribeSerializer(CafeModelSerializer):
    external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Playlist
        fields = ('table', 'external_id', )
        extra_kwargs = {
            'table': {'read_only': True}}

    def create(self, validated_data):
        validated_data['table'] = self.table
        external_id = validated_data.pop('external_id')
        status, music = Music.find_music(external_id)
        validated_data['music'] = music
        return super(MusicSubscribeSerializer, self).create(validated_data)
