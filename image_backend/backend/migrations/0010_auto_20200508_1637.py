# Generated by Django 2.2.10 on 2020-05-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20200508_1557'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='animalinfo',
            index=models.Index(fields=['birth_location_latitude', 'birth_location_longitude'], name='backend_ani_birth_l_811d8f_idx'),
        ),
        migrations.AddIndex(
            model_name='sampledatainfo',
            index=models.Index(fields=['collection_place_latitude', 'collection_place_longitude'], name='backend_sam_collect_82b97c_idx'),
        ),
    ]