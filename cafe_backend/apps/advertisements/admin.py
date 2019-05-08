from django.contrib import admin
from cafe_backend.apps.users.admin import admin_site
from .models import Advertisement


admin_site.register(Advertisement)
