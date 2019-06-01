from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from sorl.thumbnail.admin.current import AdminImageWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Field, Fieldset, Div, HTML)
from cafe_backend.core.layouts.formsets import Formset
from .models import Category, Dish, DishImage


class DishImageForm(forms.ModelForm):

    class Meta:
        model = DishImage
        fields = ('file', )

    def __init__(self, *args, **kwargs):
        super(DishImageForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['file'].widget = AdminImageWidget()


DishImageFormSet = inlineformset_factory(
    Dish, DishImage, form=DishImageForm,
    fields=['file'], extra=2, can_delete=True)


class DishForm(forms.ModelForm):
    price = forms.FloatField(min_value=0, required=False)

    class Meta:
        model = Dish
        fields = (
            'category', 'name', 'description', 'price', 'is_active',
            'name_en', 'description_en',
            'name_ko', 'description_ko', )
        widgets = {
          'description': forms.Textarea(attrs={'rows': 3}),
          'description_en': forms.Textarea(attrs={'rows': 3}),
          'description_ko': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['price'].initial = self.instance.price
        else:
            self.fields['price'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.is_multipart = True
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(Field('category'),
                Field('name'), Field('description'), Field('price'),
                Field('name_en'), Field('description_en'),
                Field('name_ko'), Field('description_ko'),
                Field('is_active'),
                Fieldset(
                    'Add images', Formset('images'), css_class='form-group'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', _('save'))),
                )
            )

    @transaction.atomic()
    def save(self, commit=True):
        if self.instance.pk:
            self.instance.price = self.cleaned_data['price']
        return super(DishForm, self).save(commit=commit)


class DishAdminForm(forms.ModelForm):
    price = forms.FloatField(required=False)

    class Meta:
        model = Dish
        fields = (
            'category', 'name', 'description', 'price', 'is_active',
            'name_en', 'description_en',
            'name_ko', 'description_ko', )

    def __init__(self, *args, **kwargs):
        super(DishAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['price'].initial = self.instance.price
        else:
            self.fields['price'].widget.attrs['disabled'] = True

    @transaction.atomic()
    def save(self, commit=True):
        price = self.cleaned_data['price']
        instance = super(DishAdminForm, self).save(commit=commit)
        if self.instance.pk:
            instance.price = price
        return instance


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
                    'submit', _('Submit'),
                    css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )


class DishFilterForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        max_length=32, widget=forms.widgets.TextInput(
            attrs={
                'placeholder': _('Dish Name or Description'),
                'required': False}))

    def __init__(self, *args, **kwargs):
        keyword = kwargs.pop('keyword')
        super(DishFilterForm, self).__init__(*args, **kwargs)
        self.fields['keyword'].initial = keyword
