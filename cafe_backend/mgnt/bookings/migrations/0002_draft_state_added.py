# Generated by Django 2.0.9 on 2019-05-08 02:07

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=django_fsm.FSMField(choices=[('d', 'Requested'), ('a', 'Approved'), ('r', 'Rejected'), ('c', 'Canceled')], default='d', max_length=50),
        ),
    ]
