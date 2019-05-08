from django.contrib import admin
from django.contrib.admin import ModelAdmin
from cafe_backend.apps.dishes.admin import admin_site
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price', )


class OrderAdmin(ModelAdmin):
    class Meta:
        model = Order

    list_display = ('table', 'total_sum', )
    inlines = (OrderItemInline, )


admin_site.register(Order, OrderAdmin)