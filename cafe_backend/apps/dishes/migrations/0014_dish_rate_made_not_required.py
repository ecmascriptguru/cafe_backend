# Generated by Django 2.0.9 on 2019-06-01 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0013_enable_solr_in_dish_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='rate',
            field=models.FloatField(default=0.0),
        ),
    ]
