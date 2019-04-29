from django import forms
from modeltranslation.forms import TranslationModelForm
from .models import Category, Dish, DishImage


class CategoryForm(TranslationModelForm):
    class Meta:
        model = Category
        fields = ('name', 'name_zh', 'is_active', )
