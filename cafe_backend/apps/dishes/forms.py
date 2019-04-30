from django import forms
from .models import Category, Dish, DishImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'name_en', 'name_ko', 'is_active', )
