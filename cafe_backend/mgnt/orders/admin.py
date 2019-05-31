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

    list_display = ('table', 'total_sum', )
    inlines = (OrderItemInline, )
    exclude = ('details', )
    # form = OrderForm


admin.site.register(Order, OrderAdmin)
