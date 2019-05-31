from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from model_utils.models import TimeStampedModel


class Version(TimeStampedModel):
    class Meta:
        ordering = ('-created', )
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')

    name = models.CharField(
        max_length=16, verbose_name=_('Name'), unique=True)
    release_note = models.TextField(verbose_name=_('Release Note'))
    file = models.FileField(
        upload_to='versions/%Y/%m/%d', verbose_name=_('File'))

    def __str__(self):
        return self.name

    @property
    def url(self):
        return self.file.url

    @classmethod
    def get_version(cls, version_name=None):
        if version_name is None:
            return cls.objects.first()
        else:
            return cls.objects.get(name=version_name)

    def get_absolute_url(self):
        return "%s?version=%s" % (
            reverse_lazy('versions:app_downloadview'), self.name)

    @property
    def download_url(self):
        return self.get_absolute_url()
