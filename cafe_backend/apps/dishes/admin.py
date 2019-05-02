from django.contrib import admin
from django.contrib.admin import ModelAdmin, AdminSite
from django.utils.translation import ugettext_lazy as _
from .models import Category, Dish, DishImage as Image, DishReview as Review


class CafeAdminSite(AdminSite):
    site_header = _("Cafe Administration")
    site_title = _("Cafe Admin")
    index_title = _("Cafe Admin")


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_en', 'name_ko', 'is_active', )

    class Meta:
        model = Category


class ImageInline(admin.TabularInline):
    model = Image


class ReviewInline(admin.TabularInline):
    model = Review


class DishAdmin(ModelAdmin):
    list_display = (
        'name', 'name_en', 'name_ko',
        'description', 'description_en', 'description_ko',
        'price', 'rate', 'is_active', )
    readonly_fields = ('rate', )
    inlines = (ImageInline, ReviewInline)

    class Meta:
        model = Dish


admin_site = CafeAdminSite()
admin_site.register(Category, CategoryAdmin)
admin_site.register(Dish, DishAdmin)