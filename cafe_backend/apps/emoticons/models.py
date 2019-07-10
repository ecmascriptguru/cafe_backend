from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Emoticon(TimeStampedModel):
    name = models.CharField(
        max_length=32, verbose_name=_('Name'))
    file = models.FileField(
        upload_to='dishes/%Y/%m/%d', verbose_name=_('Emoticon File'))

    class Meta:
        verbose_name = _('Emoticon')
        verbose_name_plural = _('Emoticons')

    @property
    def url(self):
        return self.file.url
