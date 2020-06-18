from django.views import generic
from ...core.apis.viewsets import viewsets, CafeModelViewSet
from .models import Version
from .serializers import serializers, VersionSerializer


class AppDownloadView(generic.TemplateView):
    template_name = 'versions/download.html'

    def get_context_data(self, **kwargs):
        params = super(AppDownloadView, self).get_context_data(**kwargs)
        version = Version.get_version(self.kwargs.get('version'))
        params['download_url'] = version.url
        return params


# class AppDownloadView(generic.RedirectView):
#     permanent = True

#     def get_redirect_url(self):
#         version = Version.get_version(self.kwargs.get('version'))
#         return version.url


class AppVersionViewSet(CafeModelViewSet):
    serializer_class = VersionSerializer
    queryset = Version.objects.all()
