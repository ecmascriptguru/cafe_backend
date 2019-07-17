from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Div, Field, HTML, ButtonHolder, Submit, Fieldset)
from crispy_forms.bootstrap import InlineField
from sorl.thumbnail.admin.current import AdminImageWidget
from .models import Event, EVENT_REPEAT_TYPE


WEEK_DAYS = (
    ('mon', 1), ('tue', 2), ('wed', 3), ('thu', 4),
    ('fri', 5), ('sat', 6), ('sun', 7))


class EventAdminForm(forms.ModelForm):
    mon = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('MON'), required=False)
    tue = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('TUE'), required=False)
    wed = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('WED'), required=False)
    thu = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('THU'), required=False)
    fri = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('FRI'), required=False)
    sat = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('SAT'), required=False)
    sun = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label=_('SUN'), required=False)

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'file': AdminImageWidget()}

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        for week_day, value in WEEK_DAYS:
            self.fields[week_day].widget.attrs['disabled'] =\
                (self.instance.repeat != EVENT_REPEAT_TYPE.every_week)
            self.fields[week_day].widget.attrs['checked'] =\
                self.instance.details.get('weekdays', {}).get(week_day, False)

    def save(self, commit=True):
        if self.cleaned_data.get('repeat') == EVENT_REPEAT_TYPE.every_week:
            buffer = dict()
            for week_day, value in WEEK_DAYS:
                buffer[week_day] = self.cleaned_data[week_day]
            self.instance.details['weekdays'] = buffer
        else:
            self.instance.details['weekdays'] = {}
        return super(EventAdminForm, self).save(commit)


class WeekDayCheckboxField(Field):
    template = 'layouts/fields/weekdayfield.html'


class EventForm(EventAdminForm):
    class Meta:
        model = Event
        exclude = ('details', )
        kwargs = {
            'mon': {'css_class': 'col-lg-1'}}
        widgets = {
            'file': AdminImageWidget()}

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].widget.attrs['class'] = 'date-picker'
        self.fields['to_date'].widget.attrs['class'] = 'date-picker'
        self.fields['event_date'].widget.attrs['class'] = 'date-picker'
        self.fields['at'].widget.attrs['class'] = 'time-picker'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('name', wrapper_class='col-sm-6 col-xs-12'),
                Field('event_type', wrapper_class='col-sm-6 col-xs-12'),
                css_class='row'),
            Div(
                Field('file', wrapper_class='col-xs-12'),
                css_class='row'),
            Div(
                Field('from_date', wrapper_class='col-sm-6 col-xs-12'),
                Field('to_date', wrapper_class='col-sm-6 col-xs-12'),
                css_class='row'),
            Div(
                Field('event_date', wrapper_class='col-sm-6 col-xs-12'),
                Field('at', wrapper_class='col-sm-6 col-xs-12'),
                css_class='row'),
            Div(
                Field('is_active', wrapper_class='col-sm-12 col-xs-12'),
                css_class='row form-group'),
            Div(
                Field(
                    'repeat',
                    wrapper_class='col-sm-6 col-xs-12',
                    css_class='event-repeat-type'),
                css_class='row'),
            Fieldset(
                _('Select days'),
                WeekDayCheckboxField(
                    'mon', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'tue', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'wed', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'thu', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'fri', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'sat', wrapper_class='col-sm-3 col-xs-4'),
                WeekDayCheckboxField(
                    'sun', wrapper_class='col-sm-3 col-xs-4'),
                css_id='weekday-container'),
            ButtonHolder(
                Submit(
                    'submit', _('Save changes'), css_class='pull-right',
                    wrapper_class='form-group')
            )
        )
