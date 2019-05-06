from .models import Category, Dish, DishReview
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishReview
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)
    price = serializers.ReadOnlyField()

    class Meta:
        model = Dish
        fields = '__all__'

    def get_extra_kwargs(self):
        extra_kwargs = super(DishSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        if action == 'create':
            kwargs = extra_kwargs.get('ro_on_create_field', {})
            kwargs['read_only'] = True
            extra_kwargs['ro_on_create_field'] = kwargs

        return extra_kwargs


class CategorySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(source='dish_set', many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
