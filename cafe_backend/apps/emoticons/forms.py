from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, ButtonHolder
from .models import Emoticon


class EmoticonForm(forms.ModelForm):
    class Meta:
        model = Emoticon
        exclude = ('created', 'updated', )

    def __init__(self, *args, **kwargs):
        super(EmoticonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'), Field('file'),
            ButtonHolder(
                Submit('save', _('Save Changes'), css_class='pull-right'))
        )
