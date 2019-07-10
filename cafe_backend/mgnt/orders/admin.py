from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Order, OrderItem
from .forms import OrderForm


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price', 'discount_rate', )


class OrderAdmin(ModelAdmin):
    class Meta:
        model = Order

    list_display = (
        'table', 'sum', 'free_sum', 'canceled_sum', 'wipe_zero',
        'total_billing_price', 'state', 'created', 'checkout_at')
    inlines = (OrderItemInline, )
    # exclude = ('details', )
    # form = OrderForm


admin.site.register(Order, OrderAdmin)
