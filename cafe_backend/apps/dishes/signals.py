from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import DishImage, DishReview


@receiver(post_delete, sender=DishImage)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)


@receiver(post_save, sender=DishReview)
def calculate_dish_review(sender, instance, created, **kwargs):
    dish = instance.dish
    dish.rate = dish.avg_rate
    dish.save()
