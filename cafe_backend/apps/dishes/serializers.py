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

    def get_extra_kwargs(self):
        extra_kwargs = super(DishSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        if action == 'create':
            kwargs = extra_kwargs.get('ro_on_create_field', {})
            kwargs['read_only'] = True
            extra_kwargs['ro_on_create_field'] = kwargs

        return extra_kwargs


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'name_en', 'name_ko', 'is_active', 'dishes', )
