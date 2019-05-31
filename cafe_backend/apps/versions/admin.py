from django.contrib import admin
from .models import Version
from .forms import VersionForm


class VersionAdmin(admin.ModelAdmin):
    form = VersionForm
    list_display = ('name', 'release_note', 'url')

    class Meta:
        model = Version


admin.site.register(Version, VersionAdmin)
