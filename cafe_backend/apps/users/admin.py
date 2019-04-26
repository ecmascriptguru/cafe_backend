from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .forms import TableAdminForm
from .models import User, Table


class RestaurantUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_table', )

    def get_queryset(self, *args, **kwargs):
        qs = super(RestaurantUserAdmin, self).get_queryset(*args, **kwargs)
        return qs.filter(is_table=False)


class TableAdmin(ModelAdmin):
    list_display = ('name', 'imei', 'size', 'is_vip', )
    form = TableAdminForm

admin.site.register(User, RestaurantUserAdmin)
admin.site.register(Table, TableAdmin)
