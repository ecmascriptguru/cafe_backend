from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Call(TimeStampedModel):
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Call')
        verbose_name_plural = _('Calls')

    table = models.ForeignKey(
        'users.Table', related_name='calls', on_delete=models.CASCADE,
        verbose_name=_('Table'))
    employee = models.ForeignKey(
        'users.Employee', related_name='calls', on_delete=models.CASCADE,
        verbose_name=_('Employee'), default=None, null=True, blank=True)

    def __str__(self):
        return "<Call(%s):%s>" % (self.table.name, self.employee.name)

    def to_json(self):
        return {
            'id': self.pk,
            'table': self.table.to_json(),
            'employee': self.employee.to_json()
        }
