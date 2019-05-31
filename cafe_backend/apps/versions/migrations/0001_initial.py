# Generated by Django 2.0.9 on 2019-05-31 01:44

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Name')),
                ('release_note', models.TextField(verbose_name='Release Note')),
                ('file', models.FileField(upload_to='versions/%Y/%m/%d', verbose_name='File')),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versions',
                'ordering': ('-created',),
            },
        ),
    ]