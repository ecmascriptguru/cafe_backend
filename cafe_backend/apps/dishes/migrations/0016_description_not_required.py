# Generated by Django 2.0.9 on 2019-07-14 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0015_dish_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description_en',
            field=models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='English Description'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description_ko',
            field=models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='Korean Description'),
        ),
    ]
