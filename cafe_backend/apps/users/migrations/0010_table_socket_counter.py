# Generated by Django 2.0.9 on 2019-06-18 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_waiting_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='socket_counter',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
