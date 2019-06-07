import django_filters as filters
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Video


class VideoFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.widgets.TextInput(attrs={
            'placeholder': _('Video Name')}))

    class Meta:
        model = Video
        fields = {}
        filter_overrides = {
            models.CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
         }
