# Generated by Django 2.0.9 on 2019-06-15 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_printed',
            field=models.BooleanField(default=False, verbose_name='Printed?'),
        ),
    ]