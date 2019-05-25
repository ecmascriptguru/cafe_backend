from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from cafe_backend.core.constants.types import ADS_TYPE


ADS_TYPE_CHOICES = (
    (ADS_TYPE.image, _('Image')),
    (ADS_TYPE.video, _('Video')),
)


class Advertisement(TimeStampedModel):
    name = models.CharField(
        max_length=128, verbose_name=_('name'))
    file = models.ImageField(
        upload_to='ads/%Y/%m/%d', verbose_name=_('ads_file'))
    type = FSMField(
        choices=ADS_TYPE_CHOICES, default=ADS_TYPE.image,
        verbose_name=_('ads_type'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('is_active'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('advertisement')
        verbose_name_plural = _('advertisements')

    def __str__(self):
        return "<%s(%d): %s>" % (_('Ads'), self.pk, self.name)

    @property
    def url(self):
        return self.file.url
