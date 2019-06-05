# Generated by Django 2.0.9 on 2019-06-05 16:19

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_state_choices_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=django_fsm.FSMField(choices=[('c', 'Cash'), ('w', 'WeChat'), ('a', 'AliPay')], default='w', max_length=50, verbose_name='Payment Method'),
        ),
    ]
