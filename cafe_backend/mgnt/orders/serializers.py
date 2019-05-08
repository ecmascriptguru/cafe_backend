from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Order, OrderItem


class OrderItemSerializer(CafeModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id', 'order', 'dish', 'amount', 'to_table',
            'is_canceled', 'is_delivered', )
        extra_kwargs = {
            'to_table': {'required': False},
            'order': {'required': False},
        }

    def validate(self, validated_data):
        if not validated_data.get('to_table'):
            validated_data['to_table'] = validated_data['order'].table
        return validated_data


class OrderSerializer(CafeModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        depth = 1
        fields = (
            'id', 'state', 'total_sum',
            'order_items', 'created', 'modified', )
        extra_kwargs = {
            'id': {'read_only': True},
            'state': {'read_only': True},
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

    def update(self, instance, validated_data):
        super().update
        items = validated_data.pop('order_items', [])
        for item in items:
            if item.get('order'):
                order = item.pop('order')
            dish = item.pop('dish')
            if not item.get('to_table'):
                to_table = self.table
            else:
                to_table = item.pop('to_table')
            order_item, created = instance.order_items.update_or_create(
                dish=dish, to_table=to_table, defaults=item)
        return instance
