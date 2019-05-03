from django.contrib import admin
from cafe_backend.apps.dishes.admin import admin_site
from .models import Booking, BookingMessage as Message


class MessageInlineAdmin(admin.TabularInline):
    model = Message


class BookingAdmin(admin.ModelAdmin):
    class Meta:
        model = Booking

    inlines = (MessageInlineAdmin, )

admin_site.register(Booking, BookingAdmin)
