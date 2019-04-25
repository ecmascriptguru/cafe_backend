from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Table, User


class TableForm(forms.ModelForm):
    imei = forms.CharField(max_length=16, min_length=14, strip=True, )
    class Meta:
        model = Table
        fields = ('imei', 'size', 'male', 'female', 'is_vip', )
    
    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)

        self.fields['imei'].label = _('IMEI Code')
        if self.instance.pk:
            self.fields['imei'].initial = self.instance.user.username

    def clean_male(self):
        male = self.cleaned_data['male']
        if male > self.cleaned_data['size']:
            self.add_error('male', _("Male can't be greater than size!"))
        return male

    def clean_female(self):
        male = self.cleaned_data['male']
        female = self.cleaned_data['female']
        if male + female > self.cleaned_data['size']:
            self.add_error('female', _('Male + Femail should not be greater than size!'))
        return female
    
    def save(self, commit=True):
        if self.instance.pk is None:
            user = User.objects.create_user(
                self.cleaned_data['imei'], email=None,
                password=self.cleaned_data['imei'], is_table=True)
            self.instance.user = user
        return super(TableForm, self).save(commit)
