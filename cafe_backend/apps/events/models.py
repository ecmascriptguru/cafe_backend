from django.db import models
from django.core.exceptions import ValidationError
from django_fsm import FSMField
from django.contrib.postgres.fields import JSONField
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
    at = models.TimeField()
    details = JSONField(default={}, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('at', )

    def __str__(self):
        return "<Event(%d):%s>" % (self.pk, self.name)
