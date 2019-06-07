from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, ButtonHolder
from .models import Video
from .tasks import send_video_notification_to_tables


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('created', 'updated', )

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'), Field('file'),
            ButtonHolder(
                Submit('submit', _('Save Changes'), css_class='pull-right'),
                Submit(
                    'submit', _('Show Customers'),
                    css_class='pull-left btn-secondary')),
        )

    def save(self, commit=True):
        self.instance = super(VideoForm, self).save(commit=commit)
        print(self.data['submit'])
        if self.data['submit'].lower() == _('show customers'):
            # logic to show customers
            print("SLDKFJLSKDJFLSDKJF")
            send_video_notification_to_tables.delay(self.instance.pk)
        return self.instance
