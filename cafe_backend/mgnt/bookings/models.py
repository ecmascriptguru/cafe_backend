from django.db import models
from django.core.validators import ValidationError
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import BOOKING_STATE


class BOOKING_TYPE:
    contact = 'c'
    dish = 'd'
    exchange = 'e'
    merge = 'm'


BOOKING_TYPE_CHOICES = (
    (BOOKING_TYPE.contact, _('Contact')),
    (BOOKING_TYPE.dish, _('Dish')),
    (BOOKING_TYPE.exchange, _('Exchange')),
    (BOOKING_TYPE.merge, _('Merge')),
)


BOOKING_STATE_CHOICES = (
    (BOOKING_STATE.default, _('Requested')),
    (BOOKING_STATE.approved, _('Approved')),
    (BOOKING_STATE.rejected, _('Rejected')),
    (BOOKING_STATE.canceled, _('Canceled')),
    (BOOKING_STATE.archived, _('Archived')),
)


class Booking(TimeStampedModel):
    requester = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='requested_bookings', null=True,
        verbose_name=_('requester'))
    receiver = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='received_bookings', null=True,
        verbose_name=_('receiver'))
    booking_type = FSMField(
        choices=BOOKING_TYPE_CHOICES, default=BOOKING_TYPE.contact,
        verbose_name=_('booking_type'))
    state = FSMField(
        choices=BOOKING_STATE_CHOICES, default=BOOKING_STATE.default,
        verbose_name=_('state'))
    details = JSONField(default={}, verbose_name=_('details'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')

    def __str__(self):
        return "<%s %s(%d) from %s to %s>" % (
            self.booking_type, _('Booking'), self.pk,
            self.requester.name, self.receiver.name)

    def clean(self):
        super(Booking, self).clean()
        if self.requester == self.receiver:
            raise ValidationError(
                {'receiver': _('Booking should be made between different \
                    tables.')})
        if self.booking_type == BOOKING_TYPE.contact:
            if not self.details.get('qr_code'):
                raise ValidationError({
                    'details': _('qr_code is required in contact booking.')})
        elif self.booking_type == BOOKING_TYPE.dish:
            if not self.details.get('order_items') or\
                    not isinstance(self.details.get('order_items')) or\
                    len(self.details.get('order_items')) == 0:
                raise ValidationError({
                    'details': _('A dish should be sent at least.')})
        else:
            pass

    @classmethod
    def contacts(cls):
        return cls.objects.filter(booking_type=BOOKING_TYPE.contact)

    @classmethod
    def dishes(cls):
        return cls.objects.filter(booking_type=BOOKING_TYPE.dish)

    @classmethod
    def table_bookings(cls):
        return cls.objects.filter(
            booking_type__in=[
                BOOKING_TYPE.exchange, BOOKING_TYPE.merge])

    @property
    def qr_code(self):
        return self.details.get('qr_code')

    @property
    def message(self):
        if len(self.messages.all()) > 0:
            return self.messages.first().content
        else:
            return ''

    @property
    def order_items(self):
        order_item_ids = self.details.get('order_items', [])
        return self.requester.order.order_items.filter(pk__in=order_item_ids)

    @transition(
        field=state,
        source=BOOKING_STATE.default, target=BOOKING_STATE.approved)
    def approve(self, message):
        self.messages.create(poster=self.receiver, content=message)

    @transition(
        field=state,
        source=BOOKING_STATE.default, target=BOOKING_STATE.rejected,
        conditions=[])
    def reject(self, message):
        self.messages.create(poster=self.receiver, content=message)

    @transition(
        field=state,
        source=BOOKING_STATE.default, target=BOOKING_STATE.canceled,
        conditions=[])
    def cancel(self, message):
        self.messages.create(poster=self.receiver, content=message)

    def archive(self):
        self.state = BOOKING_STATE.archived


class BookingMessage(TimeStampedModel):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='messages')
    poster = models.ForeignKey(
        'users.Table', on_delete=models.CASCADE, verbose_name=_('poster'))
    content = models.TextField(max_length=65536, verbose_name=_('content'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    @property
    def is_reply(self):
        return self.poster != self.booking.requester

    def clean(self):
        super(BookingMessage, self).clean()
        if self.poster not in [self.booking.requester, self.booking.receiver]:
            raise ValidationError({
                'poster': _('This table was not belong to this channel.')
            })
