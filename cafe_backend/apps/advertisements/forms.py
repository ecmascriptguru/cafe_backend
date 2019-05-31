from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Div, HTML, Field)
from sorl.thumbnail.admin.current import AdminImageWidget
from .models import Advertisement


class AdsForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('name', 'file', 'type', 'is_active', )
        widgets = {
            'file': AdminImageWidget()}

    def __init__(self, *args, **kwargs):
        super(AdsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'), Field('file'),
            Field('type'), Field('is_active'),
            ButtonHolder(
                Submit('submit', 'Save changes')
            )
        )
