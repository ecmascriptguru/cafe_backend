from django.contrib import admin
from .models import Advertisement
from sorl.thumbnail.admin import AdminImageMixin


class AdsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'is_active', )

    class Meta:
        model = Advertisement


admin.site.register(Advertisement, AdsAdmin)
