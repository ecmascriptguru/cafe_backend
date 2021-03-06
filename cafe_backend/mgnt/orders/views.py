import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from cafe_backend.core.apis.viewsets import CafeModelViewSet
from cafe_backend.apps.users.models import Table, TABLE_STATE
from ...apps.dishes.models import Category
from .models import Order, OrderItem, ORDER_STATE, DISH_POSITION
from . import serializers
from . import forms
from .tasks import (
    print_order_item_cancel, send_changed_order_item,
    print_order, print_order_item, bulk_print_order_items)


class TableGridView(LoginRequiredMixin, generic.ListView):
    model = Table
    template_name = 'orders/table_gridview.html'
    queryset = Table.objects.filter(state__in=[
        TABLE_STATE.using, TABLE_STATE.reserved])


class OrderDetailView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    template_name = 'orders/order_detailview.html'
    form_class = forms.OrderCheckoutForm

    def get_context_data(self, *args, **kwargs):
        params = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        params['categories'] = Category.objects.all()
        return params


class OrderFullPrintView(generic.DetailView):
    model = Order
    template_name = 'orders/order_full_printview.html'


class OrderPrintView(generic.DetailView):
    model = Order
    template_name = 'orders/order_printview.html'

    def get_context_data(self, *args, **kwargs):
        item_ids = self.request.GET.get('items', '').split(' ')
        item_ids = [id for id in item_ids if id != '']
        params = super(OrderPrintView, self).get_context_data(*args, **kwargs)
        order = self.get_object()
        items = order.items.filter(pk__in=item_ids)
        total_count = 0
        free_count = 0
        total_sum = 0.0
        free_sum = 0.0
        for item in items:
            total_count += item.amount
            total_sum += item.subtotal
            if item.is_free:
                free_count += 1
                free_sum += item.subtotal
        billing_amount = total_sum - free_sum
        params['items'] = items
        params['total_count'] = total_count
        params['total_sum'] = total_sum
        params['free_count'] = free_count
        params['free_sum'] = free_sum
        params['wipe_zeor'] = order.wipe_zero
        params['billing_price'] = billing_amount
        return params


class OrdersPrintView(generic.TemplateView):
    template_name = 'orders/orders_report_printview.html'

    def get_context_data(self, *args, **kwargs):
        params = super().get_context_data(*args, **kwargs)
        order_ids = [
            pk for pk in self.request.GET.get('orders', '').split(' ')
            if pk != '']
        print(order_ids)
        params['orders'] = Order.objects.filter(pk__in=order_ids)
        return params


class OrderPrintCallbackView(generic.DetailView):
    model = OrderItem
    template_name = 'orders/order_print_callbackview.html'

    def get_context_data(self, *args, **kwargs):
        param = super(OrderPrintCallbackView, self).get_context_data(
            *args, **kwargs)
        order = self.get_object()
        order.print_items.update(is_printed=True)
        return param


class FreeItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderItem
    form_class = forms.FreeOrderItemForm
    # success_url = None
    template_name = 'orders/free_order_item_createview.html'

    def get_form_kwargs(self, *args, **kwargs):
        params = super(FreeItemCreateView, self).get_form_kwargs(
            *args, **kwargs)
        order = self.get_order_object()
        params['order'] = order
        params['to_table'] = order.table
        return params

    def get_order_object(self):
        return Order.objects.get(pk=self.kwargs.get('order_pk'))

    def get_context_data(self, *args, **kwargs):
        params = super().get_context_data(*args, **kwargs)
        params['order'] = self.get_order_object()
        print(params['order'])
        return params

    def get_success_url(self, *args, **kwargs):
        order_pk = self.kwargs.get('order_pk')
        return reverse_lazy('orders:order_detailview', kwargs={'pk': order_pk})


class OrderItemPrintView(generic.DetailView):
    model = OrderItem
    template_name = 'orders/order_item_printview.html'


class OrderItemsBulkPrintView(generic.TemplateView):
    model = OrderItem
    template_name = 'orders/order_item_bulk_printview.html'

    def get_context_data(self, **kwargs):
        params = super().get_context_data(**kwargs)
        ids = self.request.GET.get('ids', '').split(' ')
        params['order_items'] = OrderItem.objects.filter(pk__in=ids)
        return params


class OrderItemCancelPrintView(generic.DetailView):
    model = OrderItem
    template_name = 'orders/order_item_cancel_printview.html'


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = forms.OrderForm
    template_name = 'orders/order_updateview.html'

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            self.object = form.save(commit=False)
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        return super(OrderUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'orders:order_detailview', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            data['order_items'] = forms.OrderItemFormSet(
                self.request.POST, instance=self.object)
        else:
            data['order_items'] = forms.OrderItemFormSet(instance=self.object)
        return data


class OrderViewSet(CafeModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = Order.all()

    @action(detail=False, methods=['get'])
    def current(self, request, *args, **kwargs):
        table = self.request.user.table
        current = table.order
        current_serializer = self.serializer_class(instance=current)
        return Response(current_serializer.data)

    @action(
        detail=True, methods=['get', 'post'], url_name='order_checkout_view')
    def checkout(self, request, *args, **kwargs):
        self.serializer_class = serializers.OrderCheckoutSerializer
        return super(OrderViewSet, self).update(request)

    @action(
        detail=True, methods=['post'], url_name='order_item_update')
    def update_items(self, request, *args, **kwargs):
        item_ids = request.data.get('item_ids')
        state = request.data.get('state')
        items = self.get_object().order_items.filter(
            pk__in=item_ids).exclude(state=state)
        if state == ORDER_STATE.canceled:
            for item in items:
                print_order_item_cancel.delay(item.pk)
        for item in items:
            send_changed_order_item.delay(item.pk, False)
        return Response({'status': items.update(state=state)})

    @action(
        detail=True, methods=['get'], url_name='order_item_update')
    def print(self, request, *args, **kwargs):
        from .tasks import print_order
        task = print_order.delay(self.get_object().pk, [], None, True)
        return Response({
            'status': task.id})

    @action(
        detail=True, methods=['post'], url_name='order_items_additions')
    def add_items(self, request, *args, **kwargs):
        items = request.data.get('items')
        order = self.get_object()
        order_items = list()
        try:
            for item in items:
                order_item = order.order_items.create(
                    order=order, dish_id=item['id'], is_free=item['free'],
                    amount=item['amount'], to_table=order.table,
                    price=item['price'])
                order_items.append(order_item)
            print_order.delay(order.pk, [item.pk for item in order_items])
            # bulk_print_order_items.delay([
            #     item.pk for item in order_items
            #     if item.dish.position == DISH_POSITION.kitchen])
            for order_item in order_items:
                if order_item.dish.position == DISH_POSITION.kitchen:
                    print_order_item.delay(order_item.pk)

            # Change table state
            if order.table.state != TABLE_STATE.using:
                order.table.state = TABLE_STATE.using
                order.table.save()
            return Response({'status': True})
        except Exception as e:
            return Response({'status': True, 'msg': str(e)})


class OrderItemViewSet(CafeModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self, **kwargs):
        if self.kwargs.get('order_pk'):
            return self.queryset.filter(
                order_id=self.kwargs.get('order_pk'))
        else:
            return self.queryset

    @action(detail=True, methods=['post'], url_name='order_item_set_amount')
    def set_amount(self, request, *args, **kwargs):
        item = self.get_object()
        item.amount = request.data.get('amount')
        try:
            item.save()
            return Response({'status': True})
        except Exception as e:
            return Response({'status': False, 'msg': str(e)})
