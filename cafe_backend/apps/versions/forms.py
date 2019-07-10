from django import forms
from django.utils.translation import ugettext_lazy as _
from pyaxmlparser import APK
from .models import Version


class VersionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Version
        fields = ('name', 'release_note', 'file', )

    # def __init__(self, *args, **kwargs):
    #     super(VersionForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget = forms.HiddenInput()
    #     self.fields['name'].widget.attrs['required'] = False

    def clean_file(self):
        file = self.files['file']
        try:
            apk = APK(file.file.name)
            version_name = apk.get_androidversion_name()
            if self.Meta.model.objects.filter(name=version_name).exists():
                self.add_error('file', _('This is not a new version!'))
            self.cleaned_data['name'] = version_name
        except Exception as e:
            self.add_error('file', str(e))
        return file
