from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Field, Fieldset, Div, HTML)
from cafe_backend.core.layouts.formsets import Formset
from .models import Order, OrderItem
from ...apps.users.models import Table


class OrderItemForm(forms.ModelForm):
    dish_name = forms.CharField()

    class Meta:
        model = OrderItem
        fields = ('dish_name', 'to_table', 'amount', 'state', )

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['dish_name'].initial = self.instance.dish.name
            self.fields['dish_name'].widget.attrs['readonly'] = True


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    # exclude=('price', 'discount_rate', 'to_table', ),
    extra=0, can_delete=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('table', 'created', 'modified', 'details', 'state', )

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
                    _('Order Items'), Formset('order_items'),
                    css_class='form-group'),
                Field('payment_method'),
                Field('state'),
                HTML("<br>"),
                ButtonHolder(
                    HTML('<a href="%s" class="btn btn-default">%s</a>' % (
                        reverse_lazy(
                            'orders:order_detailview',
                            kwargs={'pk': self.instance.pk}),
                        _('Back'))),
                    Submit(
                        'submit', _('Save Changes'), css_class='pull-right')),
                )
            )


class FreeOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('dish', 'amount',)

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        self.to_table = kwargs.pop('to_table')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('dish'), Field('amount'),
            ButtonHolder(Submit('commit', _('Send Free Item')))
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.order = self.order
        instance.to_table = self.to_table
        instance.is_free = True
        instance.save()
        return instance
