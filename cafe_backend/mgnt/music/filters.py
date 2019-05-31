import django_filters
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput
from django.db import models
from django import forms
from .models import Playlist


class PlaylistFilter(django_filters.FilterSet):
    music__title = django_filters.CharFilter(
        widget=TextInput(attrs={'placeholder': _('Title')}),
        lookup_expr='icontains')
    music__author = django_filters.CharFilter(
        widget=TextInput(attrs={'placeholder': _('Author')}),
        lookup_expr='icontains')

    class Meta:
        model = Playlist
        fields = {
            'table': ['exact'],
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
