# Generated by Django 2.0.9 on 2019-05-25 15:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0006_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={'ordering': ('-modified',), 'verbose_name': 'Dish', 'verbose_name_plural': 'Dishes'},
        ),
        migrations.AlterModelOptions(
            name='dishimage',
            options={'ordering': ('-modified',), 'verbose_name': 'Dish Image', 'verbose_name_plural': 'Dish Images'},
        ),
        migrations.AlterModelOptions(
            name='dishreview',
            options={'ordering': ('-modified',), 'verbose_name': 'Dish Review', 'verbose_name_plural': 'Dish Reviews'},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ('-created',), 'verbose_name': 'Price', 'verbose_name_plural': 'Prices'},
        ),
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=128, verbose_name='English name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ko',
            field=models.CharField(max_length=128, verbose_name='Korean name'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(max_length=1024, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description_en',
            field=models.TextField(max_length=1024, verbose_name='English Description'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description_ko',
            field=models.TextField(max_length=1024, verbose_name='Korean Description'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name_en',
            field=models.CharField(max_length=128, verbose_name='English name'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name_ko',
            field=models.CharField(max_length=128, verbose_name='Korean name'),
        ),
        migrations.AlterField(
            model_name='dishimage',
            name='file',
            field=models.ImageField(upload_to='dishes/%Y/%m/%d', verbose_name='Image File'),
        ),
        migrations.AlterField(
            model_name='dishreview',
            name='comment',
            field=models.TextField(max_length=1024, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='dishreview',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Price'),
        ),
    ]