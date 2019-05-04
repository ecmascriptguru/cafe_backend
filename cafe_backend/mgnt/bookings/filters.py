import django_filters
from django.db import models
from .models import Booking


class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'requester': ['exact'],
            'receiver': ['exact'],
            'booking_type': ['exact'],
            'state': ['exact'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
         }
