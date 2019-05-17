from django.contrib import admin
from cafe_backend.apps.users.admin import admin_site
from .models import Music, Playlist


admin_site.register(Music)
admin_site.register(Playlist)
