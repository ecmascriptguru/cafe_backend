# Generated by Django 2.0.9 on 2019-05-02 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0003_change_review_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterModelOptions(
            name='dishimage',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterModelOptions(
            name='dishreview',
            options={'ordering': ('-modified',)},
        ),
    ]