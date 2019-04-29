from .models import Category, Dish
from rest_framework import serializers


class DishSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dish
        fields = ('name', 'description', 'images', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'is_active', 'dishes', )
