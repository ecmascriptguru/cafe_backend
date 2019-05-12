from datetime import datetime, timedelta
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django_fsm import FSMField
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.types import EVENT_TYPE, EVENT_REPEAT_TYPE


EVENT_TYPE_CHOICES = (
    (EVENT_TYPE.image, 'Image'),
    (EVENT_TYPE.video, 'Video'),
)

EVENT_REPEAT_TYPE_CHOICES = (
    (EVENT_REPEAT_TYPE.only_once, 'Only Once'),
    (EVENT_REPEAT_TYPE.every_day, 'Every Day'),
    (EVENT_REPEAT_TYPE.every_week, 'Every Week'),
)


class Event(TimeStampedModel):
    name = models.CharField(max_length=128)
    event_type = FSMField(
        choices=EVENT_TYPE_CHOICES, default=EVENT_TYPE.image)
    file = models.ImageField(upload_to='events/%Y/%m/%d')
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    repeat = FSMField(
        choices=EVENT_REPEAT_TYPE_CHOICES, default=EVENT_REPEAT_TYPE.only_once)
    event_date = models.DateField(null=True, blank=True, default=None)
    at = models.TimeField()
    details = JSONField(default={}, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('at', )

    def clean(self):
        super(Event, self).clean()
        if self.repeat == EVENT_REPEAT_TYPE.only_once and\
                self.event_date is None:
            raise ValidationError({
                'event_date': 'Required for only once repeat type.'})

    def __str__(self):
        return "<Event(%d):%s>" % (self.pk, self.name)

    @classmethod
    def active_events(cls):
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

        # TODO: event time filtering
        qs = qs.filter(
            at__gte=datetime.now().time(),
            at__lte=(datetime.now() + timedelta(
                minutes=settings.EVENT_QUERY_INTERVAL)).time()
        )
        return qs
