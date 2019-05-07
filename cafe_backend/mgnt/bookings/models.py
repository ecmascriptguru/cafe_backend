from django.db import models
from django.core.validators import ValidationError
from django.contrib.postgres.fields import JSONField
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel


class BOOKING_TYPE:
    contact = 'c'
    dish = 'd'
    exchange = 'e'
    merge = 'm'


BOOKING_TYPE_CHOICES = (
    (BOOKING_TYPE.contact, 'Contact'),
    (BOOKING_TYPE.dish, 'Dish'),
    (BOOKING_TYPE.exchange, 'Exchange'),
    (BOOKING_TYPE.merge, 'Merge'),
)


class BOOKING_STATE:
    default = 'd'
    approved = 'a'
    rejected = 'r'


BOOKING_STATE_CHOICES = (
    (BOOKING_STATE.default, 'Requested'),
    (BOOKING_STATE.approved, 'Approved'),
    (BOOKING_STATE.rejected, 'Rejected'),
)


class Booking(TimeStampedModel):
    requester = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='requested_bookings', null=True)
    receiver = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='received_bookings', null=True)
    booking_type = FSMField(
        choices=BOOKING_TYPE_CHOICES, default=BOOKING_TYPE.contact)
    state = FSMField(
        choices=BOOKING_STATE_CHOICES, default=BOOKING_STATE.default)
    details = JSONField(default={})

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return "<%s Booking from %s to %s>" % (
            self.booking_type, self.requester.name, self.receiver.name)

    def clean(self):
        super(Booking, self).clean()
        if self.requester == self.receiver:
            raise ValidationError(
                {'receiver': 'Booking should be made between '
                    'different tables.'})
        if self.booking_type == BOOKING_TYPE.contact:
            if not self.details.get('qr_code'):
                raise ValidationError({
                    'details': 'qr_code is required in contact booking.'})
        elif self.booking_type == BOOKING_TYPE.dish:
            pass
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
    def approve(self):
        pass

    @transition(
        field=state,
        source=BOOKING_STATE.default, target=BOOKING_STATE.rejected,
        conditions=[])
    def reject(self):
        pass


class BookingMessage(TimeStampedModel):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='messages')
    poster = models.ForeignKey(
        'users.Table', on_delete=models.CASCADE)
    content = models.TextField(max_length=65536)

    class Meta:
        ordering = ('-modified', )

    @property
    def is_reply(self):
        return self.poster != self.booking.requester

    def clean(self):
        super(BookingMessage, self).clean()
        if self.poster not in [self.booking.requester, self.booking.receiver]:
            raise ValidationError({
                'poster': 'This table was not belong to this channel.'
            })
