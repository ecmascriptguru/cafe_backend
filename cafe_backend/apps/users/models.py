from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import ORDER_STATE, TABLE_STATE
from cafe_backend.mgnt.chat.models import Channel


class User(AbstractUser):
    is_table = models.BooleanField(default=False, verbose_name=_('Table?'))

    @property
    def name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        else:
            return self.username

    def get_active_channels(self):
        return Channel.objects.filter(
            attendees__user__pk=self.pk)

    def to_json(self):
        return {
            'id': self.pk,
            'is_superuser': self.is_superuser,
            'name': self.name}

    def get_channel(self, to=None):
        if to is None:
            return Channel.get_public_channel()
        else:
            to_channel = Channel.objects.get(pk=to)
            return to_channel


class Table(TimeStampedModel):
    class Meta:
        ordering = ('user__first_name', )
        verbose_name = _('Table')
        verbose_name_plural = _('Tables')

    TABLE_STATE_OPTIONS = (
        (TABLE_STATE.blank, _('Blank')),
        (TABLE_STATE.using, _('Using')),
        (TABLE_STATE.reserved, _('Reserved')))

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name=_('User'))
    size = models.PositiveSmallIntegerField(verbose_name=_('Size'))
    male = models.PositiveSmallIntegerField(default=0, verbose_name=_('Male'))
    female = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('Female'))
    is_vip = models.BooleanField(default=False, verbose_name=_('VIP?'))
    state = FSMField(
        choices=TABLE_STATE_OPTIONS, default=TABLE_STATE.blank,
        verbose_name=_('State'))
    socket_counter = models.PositiveSmallIntegerField(default=0)
    is_online = models.BooleanField(default=False, verbose_name=_('Online?'))
    cleared = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Cleared'))
    deposit = models.FloatField(
        verbose_name=_('Deposit'), validators=[MinValueValidator(0.0)],
        default=0.0)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "user": self.user.pk,
            "size": self.size,
            "name": self.name,
            "male": self.male,
            "female": self.female,
            "state": self.state
        }

    @transition(
        field='state',
        source=(TABLE_STATE.using, TABLE_STATE.reserved),
        target=TABLE_STATE.blank)
    def clear(self):
        if self.order and self.order.state != ORDER_STATE.archived:
            order = self.order
            order.details['customers']['male'] = self.male
            order.details['customers']['female'] = self.female
            order.archive()
            order.save()

        self.male = 0
        self.female = 0

        for attendee in self.user.attendees.all():
            attendee.channel.messages.filter(poster=self.user).delete()

        # TODO: Clean bookings
        for booking in self.requested_bookings.all():
            booking.archive()

        for booking in self.received_bookings.all():
            booking.archive()

        self.cleared = timezone.now()

    def can_clear(self):
        return self.order is None or self.order.is_delivered

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tables:table_updateview', args=[self.pk])

    @property
    def imei(self):
        return self.user.username

    @imei.setter
    def imei(self, value):
        self.user.username = value
        self.user.set_password(value)
        self.user.save()

    @property
    def name(self):
        return self.user.first_name

    @name.setter
    def name(self, value):
        self.user.first_name = value
        self.user.save()

    @property
    def order(self):
        if len(self.orders.exclude(state__in=[
                ORDER_STATE.canceled, ORDER_STATE.archived]).all()) > 0:
            return self.orders.exclude(state__in=[
                ORDER_STATE.canceled, ORDER_STATE.archived]).first()
        else:
            return None

    @classmethod
    def get_choices(cls):
        tables = cls.objects.all()
        return tuple([(t.pk, t.name) for t in tables])

    @classmethod
    def get_report(cls):
        total = len(cls.objects.all())
        using = len(cls.objects.filter(state=TABLE_STATE.using))
        percent = int(using / total * 100)
        return {'total': total, 'using': using, 'percent': percent}

    @classmethod
    def using_tables(cls):
        return cls.objects.filter(state=TABLE_STATE.using)

    @property
    def call(self):
        end_time = timezone.now() + timedelta(minutes=1)
        qs = self.calls.filter(modified__lte=end_time)
        if qs.exists():
            return qs.first()
        else:
            return self.calls.create(table=self)


class Employee(TimeStampedModel):
    class Meta:
        ordering = ('pk', )
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name=_('User'))

    @property
    def imei(self):
        return self.user.username

    @imei.setter
    def imei(self, value):
        self.user.username = value
        self.user.set_password(value)
        self.user.save()

    @property
    def name(self):
        return self.user.first_name

    @name.setter
    def name(self, value):
        self.user.first_name = value
        self.user.save()

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name
        }
