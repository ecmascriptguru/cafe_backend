# Generated by Django 2.0.9 on 2019-05-29 03:49

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0012_update_translation'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishimage',
            name='large',
            field=image_cropping.fields.ImageRatioField('file', '1024x768', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='large'),
        ),
        migrations.AddField(
            model_name='dishimage',
            name='medium',
            field=image_cropping.fields.ImageRatioField('file', '512x384', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='medium'),
        ),
        migrations.AddField(
            model_name='dishimage',
            name='small',
            field=image_cropping.fields.ImageRatioField('file', '256x192', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='small'),
        ),
    ]
