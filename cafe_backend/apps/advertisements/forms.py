from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Div, HTML, Field)
from sorl.thumbnail.admin.current import AdminImageWidget
from .models import Advertisement, ADS_TYPE


class AdsForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('name', 'file', 'type', 'dish', 'is_active', )
        widgets = {
            'file': AdminImageWidget()}

    def __init__(self, *args, **kwargs):
        super(AdsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'), Field('file'),
            Field('type'), Field('dish'),
            Field('is_active'),
            ButtonHolder(
                Submit('submit', 'Save changes')
            )
        )

    def clean(self):
        cleaned_data = super(AdsForm, self).clean()
        if cleaned_data['type'] == ADS_TYPE.internal and\
                cleaned_data['dish'] is None:
            self.add_error(
                'dish', _('Dish is required for internal advertisement.'))
        return cleaned_data
