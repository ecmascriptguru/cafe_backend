from cafe_backend.core.apis.serializers import serializers, CafeModelSerializer
from .models import Category, Dish, DishReview


class ReviewSerializer(CafeModelSerializer):
    class Meta:
        model = DishReview
        exclude = ('table', )
        extra_kwargs = {
            'dish': {'read_only': True}
        }

    def create(self, validated_data):
        if hasattr(self, 'table'):
            validated_data['table'] = self.table
        return super(ReviewSerializer, self).create(validated_data)


class DishSerializer(CafeModelSerializer):
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


class CategorySerializer(CafeModelSerializer):
    dishes = DishSerializer(source='dish_set', many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
