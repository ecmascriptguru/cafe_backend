# Generated by Django 2.0.9 on 2019-05-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]
