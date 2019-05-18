from django.contrib import admin
from cafe_backend.apps.users.admin import admin_site
from .models import Music, Playlist


class MusicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'state', 'external_id', )

    class Meta:
        model = Music


admin_site.register(Music, MusicAdmin)
admin_site.register(Playlist)
