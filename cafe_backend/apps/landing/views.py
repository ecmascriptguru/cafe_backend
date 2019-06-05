from datetime import timedelta, datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .forms import DashboardQueryForm
from ...apps.users.models import Table
from ...mgnt.orders.models import Order


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'landing/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        end_date = self.request.GET.get(
            'end_date',
            timezone.now().date().strftime('%Y-%m-%d'))
        start_date = self.request.GET.get(
            'start_date',
            (timezone.now() - timedelta(days=29)).date().strftime('%Y-%m-%d'))
        range_option = self.request.GET.get('range_option', _('Last 30 Days'))
        tables = self.request.GET.get('tables', '')
        params = super(DashboardView, self).get_context_data(*args, **kwargs)
        params['filter_form'] = DashboardQueryForm(
            start_date=start_date, end_date=end_date,
            range_option=range_option, tables=tables)
        params['table_choices'] = Table.get_choices()
        params['table_ids'] = [
            int(item) for item in tables.split(',') if item != '']
        params['report'] = Order.get_report(
            start_date, end_date, tables=[
                int(item) for item in tables.split(',') if item != ''])
        return params