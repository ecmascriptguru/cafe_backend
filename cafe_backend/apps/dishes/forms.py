from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from .models import Category, Dish, DishImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'name_en', 'name_ko', 'is_active', )

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name', 'name_en', 'name_ko', 'is_active',
            ButtonHolder(
                Submit(
                    'submit', 'Submit',
                    css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )
