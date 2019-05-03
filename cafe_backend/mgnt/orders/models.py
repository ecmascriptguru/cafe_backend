from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='orders', null=True)
    is_complete = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    @property
    def items(self):
        return self.order_items.filter(is_canceled=False)

    @property
    def completed(self):
        return self.items.filter(is_complete=True)

    @property
    def progress(self):
        if len(self.items) > 0:
            return "%d/%d" % (len(self.completed), len(self.items))
        else:
            return "N/A"

    @property
    def total_sum(self):
        if len(self.order_items.all()) > 0:
            return self.order_items.filter(
                is_canceled=False).values('price', 'amount').aggregate(
                    total_price=models.Sum(
                        F('price') * F("amount"),
                        output_field=models.FloatField()
                    )
                ).get('total_price', 0.0)
        else:
            return 0.0


class OrderItem(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(
        'dishes.Dish', on_delete=models.CASCADE, related_name='order_items')
    to_table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='received_order_items', null=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])
    discount_rate = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_canceled = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.price = self.dish.price
        return super(OrderItem, self).save(**kwargs)
