from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Field, Fieldset, Div, HTML)
from cafe_backend.core.layouts.formsets import Formset
from .models import Order, OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ('price', 'discount_rate',)


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    # exclude=('price', 'discount_rate', 'to_table', ),
    extra=0, can_delete=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('table', 'created', 'modified', 'state')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 update-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Order Items', Formset('order_items'),
                    css_class='form-group'),
                Field('state'),
                HTML("<br>"),
                ButtonHolder(Submit(
                    'submit', 'Save Changes', css_class='pull-right')),
                )
            )

    def save(self, commit=True):
        return super(OrderForm, self).save(commit)
