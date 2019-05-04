from django.db import models
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

    @classmethod
    def contacts(cls):
        return cls.objects.filter(
            booking_type__in=[
                BOOKING_TYPE.contact, BOOKING_TYPE.dish])

    @classmethod
    def table_bookings(cls):
        return cls.objects.filter(
            booking_type__in=[
                BOOKING_TYPE.exchange, BOOKING_TYPE.merge])


class BookingMessage(TimeStampedModel):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='messages')
    poster = models.ForeignKey(
        'users.Table', on_delete=models.CASCADE)
    content = models.TextField(max_length=65536)

    class Meta:
        ordering = ('-modified', )
