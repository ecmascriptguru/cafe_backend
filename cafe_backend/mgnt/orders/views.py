from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions
from cafe_backend.apps.users.models import Table
from .models import Order, OrderItem
from . import serializers
from . import forms


class TableGridView(LoginRequiredMixin, generic.ListView):
    model = Table
    template_name = 'orders/table_gridview.html'


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = forms.OrderForm
    template_name = 'orders/order_updateview.html'


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.filter(is_archived=False)


class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.OrderItemSerializer
    queryset = OrderItem.objects.all()
