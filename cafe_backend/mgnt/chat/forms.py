from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field
from .models import Channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = (,)
