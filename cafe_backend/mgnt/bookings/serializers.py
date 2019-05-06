from rest_framework import serializers
from cafe_backend.core.apis.serializers import CafeModelSerializer, serializers
from .models import Booking, BookingMessage


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
    class Meta:
        model = Booking
        fields = ('id', 'requester', 'receiver', 'dishes',)


class SeatBookingSerializer(CafeModelSerializer):
    pass
