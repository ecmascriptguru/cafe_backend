import django_filters
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Dish


class DishFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        widget=forms.widgets.TextInput(attrs={'placeholder': _('Dish Name')}))

    class Meta:
        model = Dish
        fields = []
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
