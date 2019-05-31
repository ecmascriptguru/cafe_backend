from django.contrib import admin
from .models import Booking, BookingMessage as Message


class MessageInlineAdmin(admin.TabularInline):
    model = Message


class BookingAdmin(admin.ModelAdmin):
    class Meta:
        model = Booking

    inlines = (MessageInlineAdmin, )

admin.site.register(Booking, BookingAdmin)
