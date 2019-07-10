from cafe_backend.core.apis.serializers import (
    CafeModelSerializer, serializers)
from cafe_backend.apps.users.serializers import TableSerializer
from .models import Channel, CHANNEL_TYPE_CHOICES, Message, Attendee


class MessageSerializer(CafeModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'poster', 'poster_name', 'created', 'content', 'channel')


class MessagePKField(serializers.RelatedField):
    def get_queryset(self, *args, **kwargs):
        user = self.context['request'].user
        channel_pk = self.context['request'].parser_context['kwargs']['pk']
        queryset = Message.objects.filter(channel_id=channel_pk)
        if hasattr(user, 'table'):
            print("SLDKFJLSKDJFLSKDJF")
            queryset = queryset.filter(
                created__gte=user.table.cleared)
        return queryset

    def to_representation(self, value):
        return value.to_json()


class AttendeeSerializer(CafeModelSerializer):
    table = TableSerializer()

    class Meta:
        model = Attendee
        fields = (
            'user', 'table', )


class ChannelSerializer(CafeModelSerializer):
    attendees = AttendeeSerializer(many=True, read_only=True)
    # messages = MessagePKField(many=True)
    message_set = MessageSerializer(
        many=True, source='quick_messages', read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'message_set', 'channel_type', 'attendees')

    # def get_fields(self, *args, **kwargs):
    #     fields = super(ChannelSerializer, self).get_fields(*args, **kwargs)
    #     # if hasattr(self, 'table'):
    #     #     fields['messages'].queryset = fields['messages'].\
    #     #         queryset.filter(created_at__gte=self.table.cleared)
    #     return fields
