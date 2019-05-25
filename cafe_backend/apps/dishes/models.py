from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


def dish_images_directory_path(instance, filename):
    return 'dishes/%d/%s' % (instance.dish.id, filename)


class Category(TimeStampedModel):
    name = models.CharField(
        max_length=128, verbose_name=_('name'))
    name_en = models.CharField(
        max_length=128, verbose_name=_('english name'))
    name_ko = models.CharField(
        max_length=128, verbose_name=_('korean name'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('active?'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Dish(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='dishes',
        null=True)
    name = models.CharField(
        max_length=128, verbose_name=_('name'))
    name_en = models.CharField(
        max_length=128, verbose_name=_('english name'))
    name_ko = models.CharField(
        max_length=128, verbose_name=_('korean name'))
    description = models.TextField(
        max_length=1024, verbose_name=_('description'))
    description_en = models.TextField(
        max_length=1024, verbose_name=_('english description'))
    description_ko = models.TextField(
        max_length=1024, verbose_name=_('korean description'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('active?'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('dish')
        verbose_name_plural = _('dishes')

    def __str__(self):
        return "<%s(%d): %s>" % (_('dish'), self.pk, self.name)

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
    file = models.ImageField(upload_to='dishes/%Y/%m/%d')

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('dish image')
        verbose_name_plural = _('dish images')

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
        verbose_name=_('rate'))
    comment = models.TextField(
        max_length=1024, verbose_name=_('comment'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('dish review')
        verbose_name_plural = _('dish reviews')

    def __str__(self):
        return "%d (%s)" % (self.rate, self.comment)


class Price(TimeStampedModel):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='prices')
    price = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name=_('price'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('price')
        verbose_name_plural = _('prices')
