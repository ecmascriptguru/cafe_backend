from io import BytesIO
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files import File
from django.conf import settings
from django_fsm import FSMField
from model_utils.models import TimeStampedModel
from sorl.thumbnail.fields import ImageField
from PIL import Image
from ...core.images.mixins import ImageThumbnailMixin
from ...core.constants.types import DISH_POSITION


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
    DISH_POSITION_CHOICES = (
        (DISH_POSITION.restaurant_counter, _('Rest Counter')),
        (DISH_POSITION.kitchen, _('Kitchen')))

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
        max_length=1024, null=True, blank=True, default=None,
        verbose_name=_('Description'))
    description_en = models.TextField(
        max_length=1024, null=True, blank=True, default=None,
        verbose_name=_('English Description'))
    description_ko = models.TextField(
        max_length=1024, null=True, blank=True, default=None,
        verbose_name=_('Korean Description'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Active?'))
    rate = models.FloatField(default=0.0)
    position = FSMField(
        choices=DISH_POSITION_CHOICES, default=DISH_POSITION.kitchen,
        verbose_name=_('Dish Position'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish')
        verbose_name_plural = _('Dishes')

    def __str__(self):
        if settings.DEBUG:
            return "<%s(%d): %s>" % (_('Dish'), self.pk, self.name)
        else:
            return self.name

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
            return int(self.prices.first().price)
        else:
            return 0

    @price.setter
    def price(self, value):
        if self.price != value and value:
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

    @classmethod
    def search(cls, keyword=None):
        qs = cls.objects.all()
        if keyword:
            qs = qs.filter(
                models.Q(name__icontains=keyword) |
                models.Q(name_en__icontains=keyword) |
                models.Q(name_ko__icontains=keyword) |
                models.Q(description__icontains=keyword) |
                models.Q(description_en__icontains=keyword) |
                models.Q(description_ko__icontains=keyword)
            )
        return qs


class DishImage(ImageThumbnailMixin, TimeStampedModel):
    image_file_field_name = 'file'

    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='images',
        verbose_name=_('Dish'))
    file = ImageField(
        upload_to='dishes/%Y/%m/%d', verbose_name=_('Image File'))

    class Meta:
        ordering = ('-modified', )
        verbose_name = _('Dish Image')
        verbose_name_plural = _('Dish Images')

    def save(self):
        watermark = Image.open(settings.WATERMARK_IMAGE)

        base_image = Image.open(self.file)
        base_image.paste(watermark, (40, 20))
        output = BytesIO()
        base_image.save(output, format='JPEG', quality=75)
        output.seek(0)
        self.file = File(output, self.file.name)
        return super(DishImage, self).save()

    def __str__(self):
        return self.file.url

    def to_json(self):
        return {
            'tiny': self.tiny,
            'small': self.small,
            'normal': self.normal,
            'big': self.big,
        }


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
