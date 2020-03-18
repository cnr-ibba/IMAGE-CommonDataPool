# Generated by Django 2.2.10 on 2020-03-16 17:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalinfo',
            name='specimens',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, default=list, size=None),
        ),
    ]
