from django.contrib import admin
from .models import Music, Playlist


class MusicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'state', 'external_id', )

    class Meta:
        model = Music


admin.site.register(Music, MusicAdmin)
admin.site.register(Playlist)
