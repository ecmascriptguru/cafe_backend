from .models import Category, Dish, DishReview
from rest_framework import serializers


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishReview
        fields = ('id', 'rate', 'comment', )


class DishSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.StringRelatedField(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Dish
        fields = (
            'id', 'name', 'name_en', 'name_ko',
            'description', 'description_en', 'description_ko',
            'rate', 'images', 'reviews', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'name_en', 'name_ko', 'is_active', 'dishes', )
