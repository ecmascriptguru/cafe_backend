# Generated by Django 2.0.9 on 2019-05-23 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_table_ring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ('pk',)},
        ),
        migrations.RemoveField(
            model_name='table',
            name='ring',
        ),
    ]
