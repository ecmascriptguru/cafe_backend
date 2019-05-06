from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class CafeModelViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_context(self):
        context = super(CafeModelViewSet, self).get_serializer_context()

        if not self.request.user.table:
            raise PermissionDenied()

        context['table'] = self.request.user.table
        return context
