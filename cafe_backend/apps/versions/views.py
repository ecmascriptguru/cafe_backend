from django.views import generic
from ...core.apis.viewsets import viewsets, CafeModelViewSet
from .models import Version
from .serializers import serializers, VersionSerializer


class AppDownloadView(generic.RedirectView):
    permanent = True

    def get_redirect_url(self):
        version = Version.get_version(self.kwargs.get('version'))
        return version.url


class AppVersionViewSet(CafeModelViewSet):
    serializer_class = VersionSerializer
    queryset = Version.objects.all()
