# Generated by Django 2.0.9 on 2019-05-02 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_table'),
        ('dishes', '0004_add_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishreview',
            name='table',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.Table'),
            preserve_default=False,
        ),
    ]
