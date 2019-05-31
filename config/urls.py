"""cafe_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url, static
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from cafe_backend.apps.users.views import TablesListView
from cafe_backend.core.apis.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token)

urlpatterns = [
    url(r'^$', TablesListView.as_view(), name='root_url'),
    url(r'^api/', include('cafe_backend.api_urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('versions/', include((
        'cafe_backend.apps.versions.urls', 'cafe_backend.apps.versions'),
        namespace='versions')),
]

urlpatterns += i18n_patterns(
    url(r'^$', TablesListView.as_view(), name='root_url'),
    url(r'^mgnt/', include('cafe_backend.mgnt_urls')),
    url(r'^settings/', include('cafe_backend.settings_urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
