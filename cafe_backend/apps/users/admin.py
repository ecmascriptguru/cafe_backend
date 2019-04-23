from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class RestaurantUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_table', )


admin.site.register(User, RestaurantUserAdmin)
