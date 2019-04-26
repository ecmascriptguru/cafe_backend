from django.utils.translation import ugettext_lazy as _
from django import forms
from crispy_forms.layout import Layout, Submit, ButtonHolder
from crispy_forms.helper import FormHelper
from .models import Table, User


class TableAdminForm(forms.ModelForm):
    imei = forms.CharField(max_length=16, min_length=14, strip=True, )
    name = forms.CharField(max_length=12, )

    class Meta:
        model = Table
        fields = ('name', 'imei', 'size', 'male', 'female', 'is_vip', )

    def __init__(self, *args, **kwargs):
        super(TableAdminForm, self).__init__(*args, **kwargs)

        self.fields['imei'].label = _('IMEI Code')
        if self.instance.pk:
            self.fields['name'].initial = self.instance.name
            self.fields['imei'].initial = self.instance.imei

    def clean_male(self):
        male = self.cleaned_data['male']
        if male > self.cleaned_data['size']:
            self.add_error('male', _("Male can't be greater than size!"))
        return male

    def clean_female(self):
        male = self.cleaned_data['male']
        female = self.cleaned_data['female']
        if male + female > self.cleaned_data['size']:
            self.add_error('female', _('Male + Femail should not be greater\
                than size!'))
        return female

    def save(self, commit=True):
        if self.instance.pk is None:
            user = User.objects.create_user(
                self.cleaned_data['imei'], email=None,
                password=self.cleaned_data['imei'], is_table=True)
            self.instance.user = user
        self.instance.imei = self.cleaned_data['imei']
        self.instance.name = self.cleaned_data['name']
        return super(TableAdminForm, self).save(commit)


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('male', 'female', 'is_vip', )

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'male', 'female', 'is_vip',
            ButtonHolder(
                Submit(
                    'submit', 'Submit',
                    css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )
