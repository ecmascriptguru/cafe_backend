# Generated by Django 2.0.9 on 2019-05-10 20:06

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='state',
            field=django_fsm.FSMField(choices=[('b', 'Blank'), ('u', 'Using'), ('r', 'Reserved'), ('w', 'Waiting')], default='b', max_length=50),
        ),
    ]
