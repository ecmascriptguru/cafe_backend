from celery import shared_task
from .models import DishImage
from django.core.files import File
from urllib import urlretrieve


@shared_task
def enable_ratio_to_original_images():
    DishImage.objects.filter(small='').delete()
