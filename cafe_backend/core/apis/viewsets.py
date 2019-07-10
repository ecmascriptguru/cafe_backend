from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework import viewsets


class CafeModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = (None)

    def get_serializer_context(self):
        context = super(CafeModelViewSet, self).get_serializer_context()

        if self.request.user.is_superuser:
            context['table'] = None
        elif not hasattr(self.request.user, 'table'):
            raise PermissionDenied()
        else:
            context['table'] = self.request.user.table
        return context
