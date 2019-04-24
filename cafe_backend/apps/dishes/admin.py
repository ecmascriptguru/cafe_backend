from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_ko', 'is_active', )
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
