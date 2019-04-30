from .models import Category, Dish
from rest_framework import serializers


class DishSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dish
        fields = (
            'name', 'name_en', 'name_ko',
            'description', 'description_en', 'description_ko', 'images', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'name_en', 'name_ko', 'is_active', 'dishes', )
