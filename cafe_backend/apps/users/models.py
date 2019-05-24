from django.db import models
from django.contrib.auth.models import AbstractUser
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import ORDER_STATE, TABLE_STATE
from cafe_backend.mgnt.chat.models import Channel


class User(AbstractUser):
    is_table = models.BooleanField(default=False)

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
            'name': self.name}

    def get_channel(self, to=None):
        if to is None:
            return Channel.get_public_channel()
        else:
            to_channel = Channel.objects.get(pk=to)
            return to_channel


class Table(TimeStampedModel):
    class Meta:
        ordering = ('pk', )

    TABLE_STATE_OPTIONS = (
        (TABLE_STATE.blank, 'Blank'),
        (TABLE_STATE.using, 'Using'),
        (TABLE_STATE.reserved, 'Reserved'),
        (TABLE_STATE.waiting, 'Waiting'))

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    size = models.PositiveSmallIntegerField()
    male = models.PositiveSmallIntegerField(default=0)
    female = models.PositiveSmallIntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    state = FSMField(
        choices=TABLE_STATE_OPTIONS, default=TABLE_STATE.blank)

    def __str__(self):
        return "<Table(%d): %s>" % (self.pk, self.name)

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
        source=(TABLE_STATE.using, TABLE_STATE.reserved, TABLE_STATE.waiting),
        target=TABLE_STATE.blank)
    def clear(self):
        pass

    def can_clear(self):
        print(self.order)
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

    def clean_table(self):
        if self.order.state != ORDER_STATE.archived:
            self.order.archive()

        # TODO: Clean bookings
        for booking in self.bookings:
            booking.archive()

    @property
    def bookings(self):
        return self.requested_bookings.all() + self.requested_bookings.all()
