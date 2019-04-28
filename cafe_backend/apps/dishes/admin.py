from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Dish, DishImage as Image


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_ko', 'is_active', )

    class Meta:
        model = Category


class DishAdmin(ModelAdmin):
    list_display = ('name', 'description', 'price', 'is_active', )

    class Meta:
        model = Dish

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
