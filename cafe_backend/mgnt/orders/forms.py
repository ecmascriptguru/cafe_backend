from django import forms
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, ButtonHolder, Submit, Field, Fieldset, Div, HTML)
from cafe_backend.core.layouts.formsets import Formset
from .models import Order, OrderItem, ORDER_STATE
from ...apps.users.models import Table
from .tasks import print_order


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


class OrderCheckoutForm(forms.ModelForm):
    deposit = forms.FloatField(label=_('Deposit'))
    additional_money = forms.FloatField(
        label=_('Additional Money'), min_value=0, required=False)
    total = forms.FloatField(label=_('Total'))
    change = forms.FloatField(label=_('Change Money'))
    earning = forms.FloatField(label=_('Income'))

    class Meta:
        model = Order
        fields = (
            'wipe_zero', 'earning', 'deposit', 'total', 'change',
            'additional_money')

    def __init__(self, *args, **kwargs):
        super(OrderCheckoutForm, self).__init__(*args, **kwargs)
        if self.instance.details.get('additional_money', 0) > 0:
            self.fields['additional_money'].initial =\
                self.instance.details['additional_money']
        else:
            self.fields['additional_money'].initial = 0
        self.fields['deposit'].initial = self.instance.table.deposit
        # self.fields['deposit'].widget.attrs['readonly'] = True
        self.fields['total'].initial = self.instance.total_billing_price
        self.fields['total'].widget.attrs['readonly'] = True
        if self.instance.income > 0:
            self.fields['earning'].initial = self.instance.income
        else:
            self.fields['earning'].initial = self.instance.total_billing_price
        self.fields['earning'].widget.attrs['readonly'] = True

        if self.instance.details.get('change', 0) > 0:
            self.fields['change'].initial = self.instance.details['change']
        else:
            self.fields['change'].initial = self.instance.table.deposit -\
                self.instance.total_billing_price
        self.fields['change'].widget.attrs['readonly'] = True
        self.fields['change'].widget.attrs['min'] = 0
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('deposit', wrapper_class='col-sm-6'),
            Field('additional_money', wrapper_class='col-sm-6'),
            Field('total', wrapper_class='col-sm-6'),
            Field('wipe_zero', wrapper_class='col-sm-6'),
            Field('earning', wrapper_class='col-sm-6'),
            Field('change', wrapper_class='col-sm-6')
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['wipe_zero'] < 0:
            self.add_error('wipe_zero', _('Wipe Zero can not be less than 0.'))
        cleaned_data['income'] = cleaned_data.pop('earning')
        details = self.instance.details
        details.update({
            'deposit': cleaned_data.pop('deposit', 0),
            'additional_money': cleaned_data.pop('additional_money', 0),
            'change': cleaned_data.pop('change', 0),
        })
        cleaned_data['details'] = details
        return cleaned_data

    def save(self, commit=True):
        self.instance.income = self.cleaned_data.pop('income')
        if self.instance.checkout_at is None:
            self.instance.checkout_at = timezone.now()
            print_order.delay(self.instance.pk, [], 'checkout', True)
        else:
            print_order.delay(self.instance.pk, [], 'repeat', True)
        return super(OrderCheckoutForm, self).save(commit)


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
        print_order.delay(instance.order.pk, [instance.pk])
        return instance
