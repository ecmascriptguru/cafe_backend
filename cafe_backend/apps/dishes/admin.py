from django.contrib import admin
from django.contrib.admin import ModelAdmin, AdminSite
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from .models import Category, Dish, DishImage as Image, DishReview as Review
from .forms import DishAdminForm

admin.site.site_header = _("Cafe Administration")
admin.site.site_title = _("Cafe Admin")
admin.site.index_title = _("Cafe Admin")


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_en', 'name_ko', 'is_active', 'slug', )

    class Meta:
        model = Category


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image


class ReviewInline(admin.TabularInline):
    model = Review


class DishAdmin(ModelAdmin):
    form = DishAdminForm
    list_display = (
        'name', 'name_en', 'name_ko', 'category',
        'description', 'description_en', 'description_ko',
        'price', 'is_active', )
    # readonly_fields = ('rate', )
    inlines = (ImageInline, ReviewInline)

    class Meta:
        model = Dish


# admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
