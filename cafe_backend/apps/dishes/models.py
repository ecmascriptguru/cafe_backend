from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from image_cropping import ImageRatioField, ImageCropField


class Category(TimeStampedModel):
    slug = models.SlugField(
        max_length=40, verbose_name=_('Slug'), null=True, default=None)
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
        null=True, verbose_name=_('Category'))
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
    rate = models.FloatField()

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish')
        verbose_name_plural = _('Dishes')

    def __str__(self):
        return "<%s(%d): %s>" % (_('Dish'), self.pk, self.name)

    @property
    def avg_rate(self):
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

    @property
    def img(self):
        if len(self.images.all()) > 0:
            return self.images.first()
        else:
            return None

    @property
    def default_image(self):
        return self.img and self.img.file.url or None


class DishImage(TimeStampedModel):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='images',
        verbose_name=_('Dish'))
    file = models.ImageField(
        upload_to='dishes/%Y/%m/%d', verbose_name=_('Image File'))
    small = ImageRatioField('file', '256x192')
    medium = ImageRatioField('file', '512x384')
    large = ImageRatioField('file', '1024x768')

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish Image')
        verbose_name_plural = _('Dish Images')

    def __str__(self):
        return self.file.url


class DishReview(TimeStampedModel):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))
    table = models.ForeignKey(
        'users.Table', on_delete=models.CASCADE,
        verbose_name=_('Table'))
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='reviews',
        verbose_name=_('Dish'))
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
        Dish, on_delete=models.CASCADE, related_name='prices',
        verbose_name=_('Dish'))
    price = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name=_('Price'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
