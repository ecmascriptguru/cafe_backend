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

    class Meta:
        ordering = ('-modified', )
