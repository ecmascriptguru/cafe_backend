from django.db import models
from django_fsm import FSMField
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.types import CHAT_ROOM_TYPE


CHANNEL_TYPE_CHOICES = (
    (CHAT_ROOM_TYPE.direct, 'Direct'),
    (CHAT_ROOM_TYPE.private, 'Private'),
    (CHAT_ROOM_TYPE.public, 'Public'))


class Channel(TimeStampedModel):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    channel_type = FSMField(
        choices=CHANNEL_TYPE_CHOICES, default=CHAT_ROOM_TYPE.private)

    class Meta:
        ordering = ('created', )

    @classmethod
    def get_public_channel(cls):
        channel, created = Channel.objects.get_or_create(
            name='Public', channel_type=CHAT_ROOM_TYPE.public)
        return channel

    def quick_messages(self):
        return self.messages.all()[:3]


class Attendee(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='attendees')
    is_active = models.BooleanField(default=True)


class Message(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='messages')
    poster = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=65536)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return "<Msg(%d):%s>(%s)" % (
            self.pk, self.poster.name, self.content)

    def to_json(self):
        return {
            'channel_id': self.channel.pk,
            'id': self.pk,
            'from': self.poster.to_json(),
            'message': self.content
        }
