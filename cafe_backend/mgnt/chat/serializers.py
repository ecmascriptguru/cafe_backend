from cafe_backend.core.apis.serializers import (
    CafeModelSerializer, serializers)
from cafe_backend.apps.users.serializers import TableSerializer
from .models import Channel, CHANNEL_TYPE_CHOICES, Message, Attendee


class MessageSerializer(CafeModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'poster', 'poster_name', 'created', 'content', 'channel')


class AttendeeSerializer(CafeModelSerializer):
    table = TableSerializer()

    class Meta:
        model = Attendee
        fields = (
            'user', 'table', )


class ChannelSerializer(serializers.ModelSerializer):   # CafeModelSerializer):
    attendees = AttendeeSerializer(many=True, read_only=True)
    message_set = MessageSerializer(
        many=True, source='quick_messages', read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'message_set', 'channel_type', 'attendees')

    def get_fields(self, *args, **kwargs):
        fields = super(ChannelSerializer, self).get_fields(*args, **kwargs)
        if hasattr(self, 'table'):
            fields['message_set'].queryset = fields['message_set'].\
                queryset.filter(created_at__gte=self.table.cleared)
        return fields
