from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Video(TimeStampedModel):
    name = models.CharField(
        max_length=16, verbose_name=_('Video Name'))
    file = models.FileField(
        upload_to='videos/%Y/%m/%d', verbose_name=_('Video File'))
