# Generated by Django 2.0.9 on 2019-07-03 08:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0013_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('employee', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='users.Employee', verbose_name='Employee')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='users.Table', verbose_name='Table')),
            ],
            options={
                'verbose_name': 'Call',
                'verbose_name_plural': 'Calls',
                'ordering': ('-created',),
            },
        ),
    ]
