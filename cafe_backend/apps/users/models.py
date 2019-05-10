from django.db import models
from django.contrib.auth.models import AbstractUser
from django_fsm import FSMField
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import ORDER_STATE, TABLE_STATE


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


class Table(TimeStampedModel):
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
