from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Order, OrderItem


class OrderItemSerializer(CafeModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'dish', 'amount', 'to_table', )
        extra_kwargs = {
            'to_table': {'required': False},
            'order': {'required': False},
        }


class OrderSerializer(CafeModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        depth = 1
        fields = (
            'id', 'is_complete', 'is_archived', 'total_sum',
            'order_items', 'created', 'modified', )
        extra_kwargs = {
            'is_complete': {
                'read_only': True,
            },
            'is_archived': {
                'read_only': True,
            },
        }

    def validate(self, data):
        if len(data.get('order_items', [])) == 0:
            raise serializers.ValidationError('Blank order was not permitted.')

        return data

    def create(self, validated_data):
        if hasattr(self, 'table'):
            validated_data['table'] = self.table

        items = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)

        for item in items:
            order.order_items.create(**item)
        return order
