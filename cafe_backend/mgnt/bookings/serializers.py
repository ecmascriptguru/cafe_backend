from rest_framework import serializers
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


class ContactSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        model = Booking
        fields = ('requester', 'receiver', 'qr_code', 'message', )

    def create(self, validated_data):
        qr_code = validated_data.pop('qr_code')
        message = validated_data.pop('message')
        validated_data['details'] = {'qr_code': qr_code}
        booking = Booking.objects.create(**validated_data)
        booking.messages.create(
            poster=validated_data['requester'], content=message)
        return booking
