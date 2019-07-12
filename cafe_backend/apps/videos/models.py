from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Video(TimeStampedModel):
    name = models.CharField(
        max_length=16, verbose_name=_('Video Name'))
    file = models.FileField(
        upload_to='videos/%Y/%m/%d', verbose_name=_('Video File'))

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'url': self.file.url}

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
