from django.core.exceptions import ValidationError
from rest_framework import serializers
from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from cafe_backend.mgnt.orders.serializers import OrderItemSerializer
from .models import Booking, BookingMessage, BOOKING_TYPE


class BookingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingMessage
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    messages = BookingMessageSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'


class ContactSerializer(CafeModelSerializer):
    qr_code = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        model = Booking
        fields = ('id', 'requester', 'receiver', 'qr_code', 'message', )
        extra_kwargs = {
            'id': {'required': False}
        }

    def create(self, validated_data):
        qr_code = validated_data.pop('qr_code')
        message = validated_data.pop('message')
        validated_data['details'] = {'qr_code': qr_code}

        if hasattr(self, 'table'):
            validated_data['requester'] = self.table

        booking = Booking.objects.create(**validated_data)
        booking.messages.create(
            poster=validated_data['requester'], content=message)
        return booking


class DishBookingSerializer(CafeModelSerializer):
    items = OrderItemSerializer(many=True, source='order_items')
    message = serializers.CharField()

    class Meta:
        model = Booking
        fields = ('id', 'receiver', 'message', 'items',)
        extra_kwargs = {
            'id': {'required': False},
            'requester': {'required': False}
        }

    def get_requester(self, obj):
        return self.table

    def create(self, validated_data):
        if hasattr(self, 'table'):
            validated_data['requester'] = self.table

        validated_data['booking_type'] = BOOKING_TYPE.dish
        message = validated_data.pop('message')
        order_items = validated_data.pop('order_items')
        details = {'order_items': []}
        for item in order_items:
            item['to_table'] = validated_data['receiver']
            order_item = self.table.order.order_items.create(**item)
            details['order_items'].append(order_item.pk)
            # order_item = OrderItemSerializer(data=item)
            # if order_item.is_valid():
            #     details['order_items'].append(order_item.save())
            # else:
            #     raise ValidationError('Invalid order item')

        validated_data['details'] = details
        instance = Booking.objects.create(**validated_data)
        instance.messages.create(
            poster=validated_data['requester'], content=message)
        return instance


class SeatBookingSerializer(CafeModelSerializer):
    pass
