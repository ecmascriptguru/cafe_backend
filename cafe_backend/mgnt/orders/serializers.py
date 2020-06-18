from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from cafe_backend.apps.dishes.serializers import DishSerializer
from cafe_backend.apps.dishes.models import Dish, DISH_POSITION
from ...apps.users.models import TABLE_STATE
from .models import Order, OrderItem
from .tasks import print_order, print_order_item, bulk_print_order_items


class OrderItemSerializer(CafeModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                 source='dish',
                                                 queryset=Dish.objects.all())
    dish = DishSerializer(read_only=True)
    to_table_name = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = (
            'id', 'order', 'dish_id', 'dish', 'amount', 'to_table',
            'to_table_name', 'is_canceled', 'is_delivered', )
        extra_kwargs = {
            'to_table': {'required': False},
            'order': {'required': False},
            'dish_object': {'read_only': True, 'required': False},
        }

    def validate(self, validated_data):
        if not validated_data.get('to_table') and hasattr(self, 'table'):
            validated_data['to_table'] = self.table
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

    def check_table_state(self, state=TABLE_STATE.using, **kwargs):
        if not hasattr(self, 'table'):
            return False
        if self.table.state != state:
            self.table.state = state
            self.table.save()

    def create(self, validated_data):
        if hasattr(self, 'table'):
            validated_data['table'] = self.table

        items = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)

        item_pks = list()
        for item in items:
            order_item = order.order_items.create(**item)
            if order_item.dish.position == DISH_POSITION.kitchen:
                item_pks.append(order_item.pk)
        print_order.delay(order.pk, item_pks)
        for pk in item_pks:
            print_order_item.delay(pk)
        # bulk_print_order_items.delay(item_pks)

        # Check table state and change when a new order was made.
        self.check_table_state(TABLE_STATE.using)
        return order

    def update(self, instance, validated_data):
        items = validated_data.pop('order_items', [])
        added_items = list()
        for item in items:
            if item.get('order'):
                order = item.pop('order')
            dish = item.pop('dish')
            if not item.get('to_table'):
                to_table = self.table
            else:
                to_table = item.pop('to_table')
            order_item = instance.order_items.create(
                dish=dish, to_table=to_table, **item)
            added_items.append(order_item)
        if len(added_items) > 0:
            order_pk = added_items[0].order.pk
            print_order.delay(order_pk, [item.pk for item in added_items])
            # bulk_print_order_items.delay([
            #     item.pk for item in added_items
            #     if item.dish.position == DISH_POSITION.kitchen])
            for item in added_items:
                if item.dish.position == DISH_POSITION.kitchen:
                    print_order_item.delay(item.pk)

            # Check table state and change when a new additional order item
            # was made.
            self.check_table_state(TABLE_STATE.using)
        return instance


class OrderCheckoutSerializer(CafeModelSerializer):
    class Meta:
        model = Order
        fields = ('payment_method', )
