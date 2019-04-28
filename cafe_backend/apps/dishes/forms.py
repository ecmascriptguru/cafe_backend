from django import forms
from .models import Category, Dish, DishImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'is_active', )
