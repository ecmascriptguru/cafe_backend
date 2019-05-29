import django_filters
from django.db import models
from django import forms
from .models import Dish


class DishFilter(django_filters.FilterSet):
    class Meta:
        model = Dish
        fields = {
            'name': ['icontains'],
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
