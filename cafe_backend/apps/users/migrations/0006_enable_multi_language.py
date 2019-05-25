# Generated by Django 2.0.9 on 2019-05-25 14:03

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190523_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='female',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='female'),
        ),
        migrations.AlterField(
            model_name='table',
            name='is_vip',
            field=models.BooleanField(default=False, verbose_name='vip?'),
        ),
        migrations.AlterField(
            model_name='table',
            name='male',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='male'),
        ),
        migrations.AlterField(
            model_name='table',
            name='size',
            field=models.PositiveSmallIntegerField(verbose_name='size'),
        ),
        migrations.AlterField(
            model_name='table',
            name='state',
            field=django_fsm.FSMField(choices=[('b', 'Blank'), ('u', 'Using'), ('r', 'Reserved'), ('w', 'Waiting')], default='b', max_length=50, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_table',
            field=models.BooleanField(default=False, verbose_name='table?'),
        ),
    ]
