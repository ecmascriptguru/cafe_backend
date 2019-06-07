from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers


class CafeModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CafeModelSerializer, self).__init__(*args, **kwargs)
        if kwargs.get('context'):
            if not kwargs['context'].get('table'):
                self.table = None
                # raise FieldDoesNotExist()
            self.table = kwargs['context']['table']
