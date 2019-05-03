# Generated by Django 2.0.9 on 2019-05-03 12:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
