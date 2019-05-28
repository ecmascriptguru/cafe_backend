import django_filters
from django.db import models
from django import forms
from .models import Playlist


class PlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = Playlist
        fields = {
            'table': ['exact'],
            'music__title': ['icontains'],
            'music__author': ['icontains'],
            'is_active': ['exact'],
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
