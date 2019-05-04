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
