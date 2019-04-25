from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .forms import TableForm
from .models import User, Table


class RestaurantUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_table', )


class TableAdmin(ModelAdmin):
    form = TableForm

admin.site.register(User, RestaurantUserAdmin)
admin.site.register(Table, TableAdmin)
