from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from cafe_backend.core.constants.types import ADS_TYPE


ADS_TYPE_CHOICES = (
    (ADS_TYPE.image, 'Image'),
    (ADS_TYPE.video, 'Video'),
)


class Advertisement(TimeStampedModel):
    name = models.CharField(max_length=128)
    file = models.ImageField(upload_to='ads/%Y/%m/%d')
    type = FSMField(choices=ADS_TYPE_CHOICES, default=ADS_TYPE.image)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return "<Ads(%d): %s>" % (self.pk, self.name)
