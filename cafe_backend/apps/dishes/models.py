from django.db import models
from model_utils.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator


def dish_images_directory_path(instance, filename):
    return 'dishes/%d/%s' % (instance.dish.id, filename)


class Category(TimeStampedModel):
    name = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    name_ko = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Dish(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='dishes',
        null=True)
    name = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    name_ko = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    description_en = models.TextField(max_length=1024)
    description_ko = models.TextField(max_length=1024)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return "<dish(%d): %s>" % (self.pk, self.name)

    @property
    def rate(self):
        return "%.2f" % self.reviews.values('rate')\
            .aggregate(models.Avg('rate')).get('rate__avg', 0.0)


class DishImage(TimeStampedModel):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='dishes/%Y/%m/%d')

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return self.file.url


class DishReview(TimeStampedModel):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))
    table = models.ForeignKey('users.Table', on_delete=models.CASCADE)
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
        default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(max_length=1024)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return "%d (%s)" % (self.rate, self.comment)
