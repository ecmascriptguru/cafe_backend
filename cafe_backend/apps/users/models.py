from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    is_table = models.BooleanField(default=False)


class Table(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    size = models.PositiveSmallIntegerField()
    male = models.PositiveSmallIntegerField(default=0)
    female = models.PositiveSmallIntegerField(default=0)
    is_vip = models.BooleanField(default=False)

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
