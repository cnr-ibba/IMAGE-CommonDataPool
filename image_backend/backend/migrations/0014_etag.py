# Generated by Django 2.2.13 on 2020-07-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20200707_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_source_id', models.CharField(max_length=1000)),
                ('etag', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'backend_etag',
                'managed': False,
            },
        ),
    ]
