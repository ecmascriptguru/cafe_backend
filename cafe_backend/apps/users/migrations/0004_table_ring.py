# Generated by Django 2.0.9 on 2019-05-22 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_table_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='ring',
            field=models.FileField(default=None, null=True, upload_to='rings/%Y/%m/%d'),
        ),
    ]