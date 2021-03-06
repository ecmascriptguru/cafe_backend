# Generated by Django 2.0.9 on 2019-05-27 15:44

from django.db import migrations
from ....core.constants.categories import DEFAULT_CATEGORIES


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('dishes', 'Category')

    count, _ = Category.objects.all().delete()
    print("%d objects deleted from database" % count)

    count = 0
    for (cn, en, ko, slug) in DEFAULT_CATEGORIES:
        category = Category(
            slug=slug, name=cn, name_ko=ko, name_en=en)
        try:
            category.save()
            count += 1
        except Exception as e:
            print(str(e))

    print("%d categories created successfully." % count)


def reverse_func(apps, schema_editor):
    print("Do nothing...")


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0010_category_slug'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_func)
    ]
