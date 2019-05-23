from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Table
from .forms import TableForm
from .serializers import TableSerializer
from .tasks import send_ringtone_alarm_to_admin


class TablesListView(LoginRequiredMixin, generic.ListView):
    model = Table
    template_name = 'tables/table_listview.html'


class TableUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Table
    template_name = 'tables/table_updateview.html'
    form_class = TableForm
    success_url = reverse_lazy('tables:table_listview')


class TableViewSet(CafeModelViewSet):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    pagination_class = None
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['post'], url_name='ringtone_view')
    def ring(self, request, *args, **kwargs):
        try:
            send_ringtone_alarm_to_admin.delay(self.request.user.table.pk)
            return Response({"status": True})
        except Exception as e:
            print(str(e))
            return Response({"status": False})
