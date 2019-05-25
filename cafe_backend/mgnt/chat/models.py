from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.types import CHAT_ROOM_TYPE


CHANNEL_TYPE_CHOICES = (
    (CHAT_ROOM_TYPE.direct, _('Direct')),
    (CHAT_ROOM_TYPE.private, _('Private')),
    (CHAT_ROOM_TYPE.public, _('Public')))


class Channel(TimeStampedModel):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    description = models.TextField(
        max_length=256, verbose_name=_('description'))
    channel_type = FSMField(
        choices=CHANNEL_TYPE_CHOICES, default=CHAT_ROOM_TYPE.private,
        verbose_name=_('channel type'))

    class Meta:
        ordering = ('created', )
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    @classmethod
    def get_public_channel(cls):
        channel, created = Channel.objects.get_or_create(
            name='Public', channel_type=CHAT_ROOM_TYPE.public)
        return channel

    def quick_messages(self):
        return self.messages.all()[:6]


class Attendee(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='attendees')
    is_active = models.BooleanField(default=True, verbose_name=_('active?'))

    class Meta:
        unique_together = ['channel', 'user', ]
        verbose_name = _('attendee')
        verbose_name_plural = _('attendees')

    @property
    def table(self):
        if hasattr(self.user, 'table'):
            return self.user.table
        else:
            return None


class Message(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='messages')
    poster = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('poster'))
    content = models.TextField(max_length=65536, verbose_name=_('content'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    @property
    def poster_name(self):
        return self.poster.first_name

    def __str__(self):
        return "<Msg(%d):%s>(%s)" % (
            self.pk, self.poster.name, self.content)

    def to_json(self):
        return {
            'channel_id': self.channel.pk,
            'id': self.pk,
            'from': self.poster.to_json(),
            'content': self.content,
            'poster': self.poster.pk,
            'poster_name': self.poster.first_name,
            'created': str(self.created)
        }
