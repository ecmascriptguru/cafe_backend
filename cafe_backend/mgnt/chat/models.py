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
    name = models.CharField(max_length=32, verbose_name=_('Name'))
    description = models.TextField(
        max_length=256, verbose_name=_('Description'))
    channel_type = FSMField(
        choices=CHANNEL_TYPE_CHOICES, default=CHAT_ROOM_TYPE.private,
        verbose_name=_('Channel type'))

    class Meta:
        ordering = ('created', )
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    @classmethod
    def get_public_channel(cls):
        channel, created = Channel.objects.get_or_create(
            name='Public', channel_type=CHAT_ROOM_TYPE.public)
        return channel

    def quick_messages(self):
        return self.messages.all()


class Attendee(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='attendees',
        verbose_name=_('Channel'))
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='attendees',
        verbose_name=_('User'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active?'))

    class Meta:
        unique_together = ['channel', 'user', ]
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')

    @property
    def table(self):
        if hasattr(self.user, 'table'):
            return self.user.table
        else:
            return None


class Message(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Channel'))
    poster = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Poster'))
    content = models.TextField(max_length=65536, verbose_name=_('Content'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    @property
    def poster_name(self):
        return self.poster.first_name

    def __str__(self):
        return "<%s(%d):%s>(%s)" % (
            _('Message'), self.pk, self.poster.name, self.content)

    def to_json(self):
        if hasattr(self.poster, 'table'):
            male = self.poster.table.male
            female = self.poster.table.female
        else:
            male = 0
            female = 0

        return {
            'channel_id': self.channel.pk,
            'id': self.pk,
            'from': self.poster.to_json(),
            'content': self.content,
            'poster': self.poster.pk,
            'poster_name': self.poster.first_name,
            'is_table': self.poster.is_table,
            'male': male,
            'female': female,
            'created': str(self.created)
        }
