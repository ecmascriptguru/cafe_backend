from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


def dish_images_directory_path(instance, filename):
    return 'dishes/%d/%s' % (instance.dish.id, filename)


class Category(TimeStampedModel):
    name = models.CharField(
        max_length=128, verbose_name=_('Name'))
    name_en = models.CharField(
        max_length=128, verbose_name=_('English name'))
    name_ko = models.CharField(
        max_length=128, verbose_name=_('Korean name'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Active?'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Dish(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='dishes',
        null=True)
    name = models.CharField(
        max_length=128, verbose_name=_('Name'))
    name_en = models.CharField(
        max_length=128, verbose_name=_('English name'))
    name_ko = models.CharField(
        max_length=128, verbose_name=_('Korean name'))
    description = models.TextField(
        max_length=1024, verbose_name=_('Description'))
    description_en = models.TextField(
        max_length=1024, verbose_name=_('English Description'))
    description_ko = models.TextField(
        max_length=1024, verbose_name=_('Korean Description'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Active?'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish')
        verbose_name_plural = _('Dishes')

    def __str__(self):
        return "<%s(%d): %s>" % (_('Dish'), self.pk, self.name)

    @property
    def rate(self):
        if len(self.reviews.all()) > 0:
            return "%.2f" % self.reviews.values('rate')\
                .aggregate(models.Avg('rate')).get('rate__avg', 0.0)
        else:
            return 0.0

    @property
    def price(self):
        if len(self.prices.all()) > 0:
            return self.prices.first().price
        else:
            return 0.0

    @price.setter
    def price(self, value):
        if self.price != value:
            self.prices.create(price=value)


class DishImage(TimeStampedModel):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(
        upload_to='dishes/%Y/%m/%d', verbose_name=_('Image File'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish Image')
        verbose_name_plural = _('Dish Images')

    def __str__(self):
        return self.file.url


class DishReview(TimeStampedModel):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))
    table = models.ForeignKey('users.Table', on_delete=models.CASCADE)
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
        default=5, validators=[MaxValueValidator(5), MinValueValidator(1)],
        verbose_name=_('Rate'))
    comment = models.TextField(
        max_length=1024, verbose_name=_('Comment'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish Review')
        verbose_name_plural = _('Dish Reviews')

    def __str__(self):
        return "%d (%s)" % (self.rate, self.comment)


class Price(TimeStampedModel):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='prices')
    price = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name=_('Price'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
