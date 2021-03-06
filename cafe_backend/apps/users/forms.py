from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from django.urls import reverse_lazy
from crispy_forms.layout import Layout, Submit, ButtonHolder, HTML, Div
from crispy_forms.helper import FormHelper
from ...core.constants.types import MONITOR_MESSAGE_TYPE
from .models import Table, User, TABLE_STATE, Employee
from .tasks import send_command


class TableAdminForm(forms.ModelForm):
    imei = forms.CharField(
        max_length=16, min_length=14, strip=True, label=_('imei'))
    name = forms.CharField(max_length=12, label=_('name'))

    class Meta:
        model = Table
        fields = (
            'name', 'imei', 'size', 'female',
            'male', 'state', 'is_online', 'is_vip', 'deposit',)

    def __init__(self, *args, **kwargs):
        super(TableAdminForm, self).__init__(*args, **kwargs)

        self.fields['imei'].label = _('IMEI Code')
        if self.instance.pk:
            self.fields['name'].initial = self.instance.name
            self.fields['imei'].initial = self.instance.imei
        else:
            self.fields['size'].initial = 4

    def clean_size(self):
        if self.cleaned_data.get('size', 0) < 1:
            self.add_error('size', _('Size can not be 0.'))
        return self.cleaned_data.get('size', 0)

    def clean(self):
        super(TableAdminForm, self).clean()
        male = self.cleaned_data.get('male', 0)
        female = self.cleaned_data.get('female', 0)
        state = self.cleaned_data.get('state')

        if male > self.cleaned_data.get('size', 0):
            self.add_error('male', _("Male can't be greater than size!"))

        if male + female > self.cleaned_data.get('size', 0):
            self.add_error('female', _('Male + Femail should not be greater\
                than size!'))

        if state == TABLE_STATE.using:
            if male + female < 1:
                self.add_error('female', _('Using without any customers?'))
        return self.cleaned_data

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
        fields = (
            'size', 'male', 'female', 'is_vip', 'state', 'deposit', )

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.state == TABLE_STATE.blank:
            self.helper.layout = Layout(
                'size', 'female', 'male', 'deposit', 'state', 'is_vip',
                ButtonHolder(
                    Submit(
                        'submit', _('Save Changes'),
                        css_class='btn btn-primary pull-right'),
                ),
            )
        else:
            if self.instance.state == TABLE_STATE.using and\
                    self.instance.order and\
                    len(self.instance.order.items.all()) > 0:
                self.fields['state'].widget = forms.HiddenInput()
            self.helper.layout = Layout(
                'size', 'female', 'male', 'deposit', 'state', 'is_vip',
                ButtonHolder(
                    Submit(
                        'submit', _('Save Changes'),
                        css_class='btn btn-primary pull-right'),
                    Submit(
                        'submit', _('Clear'),
                        css_class='btn btn-danger pull-left'),
                    wrapper_class='form-group',
                ),
            )

    def clean(self):
        super(TableForm, self).clean()
        male = self.cleaned_data.get('male', 0)
        female = self.cleaned_data.get('female', 0)
        state = self.cleaned_data.get('state')

        if male > self.cleaned_data.get('size', 0):
            self.add_error('male', _("Male can't be greater than size!"))

        if male + female > self.cleaned_data.get('size', 0):
            self.add_error('female', _('Male + Femail should not be greater\
                than size!'))

        if state == TABLE_STATE.using:
            if male + female < 1:
                self.add_error('female', _('Using without any customers?'))

        if self.cleaned_data.get('deposit', 0) < 0:
            self.add_error('deposit', _("Deposit can't be less than 0."))

        # data = super(TableForm, self).clean()
        # if self.data['submit'].lower() == _('clear') and\
        #         not self.instance.can_clear():
        #     self.add_error(None, _('Order is not complete yet.'))
        return self.cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.data['submit'].lower() == _('clear'):
            instance.clear()
        instance.save()
        return instance


class TableControlForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ()

    def __init__(self, *args, **kwargs):
        super(TableControlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.is_online:
            self.helper.layout = Layout(
                Div(
                    HTML('<h3>%s</h3>' % _('This table is online now.')),
                    css_class='form-group'
                ),
                ButtonHolder(
                    Submit(
                        'submit', _('Reboot'),
                        css_class='btn-warning pull-left'),
                    Submit(
                        'submit', _('Stop'),
                        css_class='btn-danger pull-right'),
                )
            )
        else:
            self.helper.layout = Layout(
                Div(
                    HTML('<h3>%s</h3>' % _('This table is offline now.')),
                    css_class='form-group'
                ),
                ButtonHolder(
                    Submit(
                        'submit', _('Start'),
                        css_class='btn-primary pull-right'),
                )
            )

    def clean(self):
        super(TableControlForm, self).clean()
        submit = self.data['submit']
        if submit not in [_('Start'), _('Stop'), _('Reboot')]:
            self.add_error(None, _('Unknown command %s' % submit))

    def save(self, commit=True):
        if self.data['submit'] == _('Start'):
            command = MONITOR_MESSAGE_TYPE.start
        elif self.data['submit'] == _('Stop'):
            command = MONITOR_MESSAGE_TYPE.stop
        elif self.data['submit'] == _('Reboot'):
            command = MONITOR_MESSAGE_TYPE.reboot
        send_command.delay(self.instance.pk, command)
        return self.instance


class EmployeeAdminForm(forms.ModelForm):
    imei = forms.CharField(
        max_length=16, min_length=14, strip=True, label=_('imei'))
    name = forms.CharField(max_length=12, label=_('name'))

    class Meta:
        model = Employee
        fields = ('name', 'imei',)

    def __init__(self, *args, **kwargs):
        super(EmployeeAdminForm, self).__init__(*args, **kwargs)

        self.fields['imei'].label = _('IMEI Code')
        if self.instance.pk:
            self.fields['name'].initial = self.instance.name
            self.fields['imei'].initial = self.instance.imei

    def save(self, commit=True):
        if self.instance.pk is None:
            user = User.objects.create_user(
                self.cleaned_data['imei'], email=None,
                password=self.cleaned_data['imei'], is_table=True)
            self.instance.user = user
        self.instance.imei = self.cleaned_data['imei']
        self.instance.name = self.cleaned_data['name']
        return super(EmployeeAdminForm, self).save(commit)
