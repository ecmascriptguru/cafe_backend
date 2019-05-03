from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Field, Fieldset, Div, HTML)
from cafe_backend.core.layouts.formsets import Formset
from .models import Category, Dish, DishImage


class DishImageForm(forms.ModelForm):
    class Meta:
        model = DishImage
        exclude = ()


DishImageFormSet = inlineformset_factory(
    Dish, DishImage, form=DishImageForm,
    fields=['file'], extra=2, can_delete=True)


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        exclude = ('created', 'modified', )
        widgets = {
          'description': forms.Textarea(attrs={'rows': 3}),
          'description_en': forms.Textarea(attrs={'rows': 3}),
          'description_ko': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.instance = kwargs.pop('instance')
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.is_multipart = True
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(Field('category'),
                Field('name'), Field('description'),
                Field('name_en'), Field('description_en'),
                Field('name_ko'), Field('description_ko'),
                Field('price'), Field('is_active'),
                Fieldset(
                    'Add images', Formset('images'), css_class='form-group'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )


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
