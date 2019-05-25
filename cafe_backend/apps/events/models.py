from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django_fsm import FSMField
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.types import EVENT_TYPE, EVENT_REPEAT_TYPE


EVENT_TYPE_CHOICES = (
    (EVENT_TYPE.image, _('Image')),
    (EVENT_TYPE.video, _('Video')),
)

EVENT_REPEAT_TYPE_CHOICES = (
    (EVENT_REPEAT_TYPE.only_once, _('Only Once')),
    (EVENT_REPEAT_TYPE.every_day, _('Every Day')),
    (EVENT_REPEAT_TYPE.every_week, _('Every Week')),
)


class Event(TimeStampedModel):
    name = models.CharField(
        max_length=128, verbose_name=_('Name'))
    event_type = FSMField(
        choices=EVENT_TYPE_CHOICES, default=EVENT_TYPE.image,
        verbose_name=_('Event Type'))
    file = models.ImageField(
        upload_to='events/%Y/%m/%d', verbose_name=_('File'))
    from_date = models.DateField(null=True, verbose_name=_('Start date'))
    to_date = models.DateField(null=True, verbose_name=_('End date'))
    repeat = FSMField(
        choices=EVENT_REPEAT_TYPE_CHOICES, default=EVENT_REPEAT_TYPE.only_once,
        verbose_name=_('Repeat Type'))
    event_date = models.DateField(
        null=True, blank=True, default=None, verbose_name=_('Event Date'))
    at = models.TimeField(verbose_name=_('Event Time'))
    details = JSONField(default={}, blank=True, verbose_name=_('Details'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active?'))

    class Meta:
        ordering = ('at', )
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def clean(self):
        super(Event, self).clean()
        if self.repeat == EVENT_REPEAT_TYPE.only_once and\
                self.event_date is None:
            raise ValidationError({
                'event_date': _('Required for only once repeat type.')})

    def __str__(self):
        return "<%s(%d):%s>" % (_('event'), self.pk, self.name)

    def to_json(self):
        return {
            'name': self.name,
            'type': self.event_type,
            'url': self.file.url,
            'date': self.event_date and self.event_date.isoformat() or '',
            'at': self.at.isoformat()
        }

    @classmethod
    def today_events(cls):
        # TODO: Active Filtering
        qs = cls.objects.filter(is_active=True)

        # TODO: Date(From and To) Filter
        qs = qs.filter(
            Q(
                Q(to_date=None) | Q(to_date__gte=datetime.now())
            ),
            Q(
                Q(from_date=None) | Q(from_date__lte=datetime.now())
            ))

        # TODO: Repeat type filtering
        temp_keyword = "details__weekdays__%s" % datetime.now().\
            strftime("%a").lower()
        weekday_kwargs = {temp_keyword: True}
        qs = qs.filter(
            Q(
                repeat=EVENT_REPEAT_TYPE.every_day) |
            Q(
                repeat=EVENT_REPEAT_TYPE.only_once,
                event_date=datetime.today()) |
            Q(
                repeat=EVENT_REPEAT_TYPE.every_week,
                **weekday_kwargs)
        )
        return qs

    @classmethod
    def active_events(cls):
        qs = cls.today_events()
        # TODO: event time filtering
        qs = qs.filter(
            at__gte=datetime.now().time(),
            at__lte=(datetime.now() + timedelta(
                minutes=settings.EVENT_QUERY_INTERVAL)).time()
        )
        return qs
