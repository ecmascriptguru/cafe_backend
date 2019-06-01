from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, ButtonHolder, Submit
from ...apps.users.models import Table


class DashboardQueryForm(forms.Form):
    start_date = forms.CharField(widget=forms.widgets.HiddenInput(attrs={
        'id': 'dashboard_start_date'}))
    end_date = forms.CharField(widget=forms.widgets.HiddenInput(attrs={
        'id': 'dashboard_end_date'}))
    range_option = forms.CharField(widget=forms.widgets.HiddenInput(attrs={
        'id': 'dashboard_date_range_option'}))
    tables = forms.CharField(widget=forms.widgets.HiddenInput(attrs={
        'id': 'dashboard_tables'}))

    def __init__(self, *args, **kwargs):
        start_date = kwargs.pop('start_date', None)
        end_date = kwargs.pop('end_date', None)
        range_option = kwargs.pop('range_option', None)
        tables = kwargs.pop('tables', None)
        super(DashboardQueryForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = start_date
        self.fields['end_date'].initial = end_date
        self.fields['range_option'].initial = range_option
        self.fields['tables'].initial = tables
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
