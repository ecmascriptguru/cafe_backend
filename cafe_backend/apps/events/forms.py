from django import forms
from django.core.exceptions import ValidationError
from .models import Event, EVENT_REPEAT_TYPE


WEEK_DAYS = (
    ('mon', 1), ('tue', 2), ('wed', 3), ('thu', 4),
    ('fri', 5), ('sat', 6), ('sun', 7))


class EventForm(forms.ModelForm):
    mon = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='MON', required=False)
    tue = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='TUE', required=False)
    wed = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='WED', required=False)
    thu = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='THU', required=False)
    fri = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='FRI', required=False)
    sat = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='SAT', required=False)
    sun = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'checked': False, 'class': 'weekday-checkbox',
                'disabled': True}), label='SUN', required=False)

    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for week_day, value in WEEK_DAYS:
            self.fields[week_day].widget.attrs['disabled'] =\
                (self.instance.repeat != EVENT_REPEAT_TYPE.every_week)
            self.fields[week_day].widget.attrs['checked'] =\
                self.instance.details.get('weekdays', {}).get(week_day, False)

    def save(self, commit=True):
        if self.cleaned_data['repeat'] == EVENT_REPEAT_TYPE.every_week:
            buffer = dict()
            for week_day, value in WEEK_DAYS:
                buffer[week_day] = self.cleaned_data[week_day]
            self.instance.details['weekdays'] = buffer
        else:
            self.instance.details['weekdays'] = {}
        return super(EventForm, self).save(commit)
