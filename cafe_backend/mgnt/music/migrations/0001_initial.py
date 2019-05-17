# Generated by Django 2.0.9 on 2019-05-17 03:24

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=64)),
                ('author', models.CharField(max_length=32)),
                ('url', models.URLField(verbose_name='Music URL')),
                ('external_id', models.CharField(max_length=32, unique=True)),
                ('pic_url', models.URLField(verbose_name='Picture URL')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
