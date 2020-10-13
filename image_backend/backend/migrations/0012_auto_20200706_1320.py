# Generated by Django 2.2.13 on 2020-07-06 13:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20200703_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('data_source_id', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('alternative_id', models.CharField(max_length=1000)),
                ('project', models.CharField(max_length=1000)),
                ('submission_title', models.TextField()),
                ('material', models.CharField(max_length=1000)),
                ('material_ontology', models.CharField(max_length=1000)),
                ('person_last_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_email', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_affiliation', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_role', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_role_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_role', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_role_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('gene_bank_name', models.CharField(max_length=1000)),
                ('gene_bank_country', models.CharField(max_length=1000)),
                ('gene_bank_country_ontology', models.CharField(max_length=1000)),
                ('data_source_type', models.CharField(max_length=1000)),
                ('data_source_version', models.CharField(max_length=1000)),
                ('species', models.CharField(db_index=True, max_length=1000)),
                ('species_ontology', models.CharField(max_length=1000)),
                ('etag', models.CharField(max_length=1000)),
                ('submission_description', models.TextField(blank=True)),
                ('person_first_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_address', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, size=None)),
                ('organization_country', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_country_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('description', models.TextField(blank=True)),
                ('person_initial', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_uri', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, size=None)),
                ('publication_doi', models.CharField(blank=True, max_length=1000)),
                ('supplied_breed', models.CharField(max_length=1000)),
                ('efabis_breed_country', models.CharField(max_length=1000)),
                ('sex', models.CharField(max_length=1000)),
                ('sex_ontology', models.CharField(max_length=1000)),
                ('birth_location_accuracy', models.CharField(max_length=1000)),
                ('mapped_breed', models.CharField(blank=True, max_length=1000)),
                ('mapped_breed_ontology', models.CharField(blank=True, max_length=1000)),
                ('birth_date', models.CharField(blank=True, max_length=1000)),
                ('birth_date_unit', models.CharField(blank=True, max_length=1000)),
                ('birth_location', models.CharField(blank=True, max_length=1000)),
                ('birth_location_longitude', models.CharField(blank=True, max_length=1000)),
                ('birth_location_longitude_unit', models.CharField(blank=True, max_length=1000)),
                ('birth_location_latitude', models.CharField(blank=True, max_length=1000)),
                ('birth_location_latitude_unit', models.CharField(blank=True, max_length=1000)),
                ('child_of', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=2)),
                ('specimens', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, default=list, size=None)),
            ],
            options={
                'ordering': ['-data_source_id'],
            },
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('data_source_id', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('alternative_id', models.CharField(max_length=1000)),
                ('project', models.CharField(max_length=1000)),
                ('submission_title', models.TextField()),
                ('material', models.CharField(max_length=1000)),
                ('material_ontology', models.CharField(max_length=1000)),
                ('person_last_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_email', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_affiliation', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_role', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('person_role_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_role', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('organization_role_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('gene_bank_name', models.CharField(max_length=1000)),
                ('gene_bank_country', models.CharField(max_length=1000)),
                ('gene_bank_country_ontology', models.CharField(max_length=1000)),
                ('data_source_type', models.CharField(max_length=1000)),
                ('data_source_version', models.CharField(max_length=1000)),
                ('species', models.CharField(db_index=True, max_length=1000)),
                ('species_ontology', models.CharField(max_length=1000)),
                ('etag', models.CharField(max_length=1000)),
                ('submission_description', models.TextField(blank=True)),
                ('person_first_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_address', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, size=None)),
                ('organization_country', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_country_ontology', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('description', models.TextField(blank=True)),
                ('person_initial', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, size=None)),
                ('organization_uri', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, size=None)),
                ('publication_doi', models.CharField(blank=True, max_length=1000)),
                ('derived_from', models.CharField(max_length=1000)),
                ('collection_place_accuracy', models.CharField(max_length=1000)),
                ('organism_part', models.CharField(max_length=1000)),
                ('organism_part_ontology', models.CharField(db_index=True, max_length=1000)),
                ('specimen_collection_protocol', models.CharField(blank=True, max_length=1000)),
                ('collection_date', models.CharField(blank=True, max_length=1000)),
                ('collection_date_unit', models.CharField(blank=True, max_length=1000)),
                ('collection_place_latitude', models.CharField(blank=True, max_length=1000)),
                ('collection_place_latitude_unit', models.CharField(blank=True, max_length=1000)),
                ('collection_place_longitude', models.CharField(blank=True, max_length=1000)),
                ('collection_place_longitude_unit', models.CharField(blank=True, max_length=1000)),
                ('collection_place', models.CharField(blank=True, max_length=1000)),
                ('developmental_stage', models.CharField(blank=True, max_length=1000)),
                ('developmental_stage_ontology', models.CharField(blank=True, max_length=1000)),
                ('physiological_stage', models.CharField(blank=True, max_length=1000)),
                ('physiological_stage_ontology', models.CharField(blank=True, max_length=1000)),
                ('availability', models.CharField(blank=True, max_length=1000)),
                ('sample_storage', models.CharField(blank=True, max_length=1000)),
                ('sample_storage_processing', models.CharField(blank=True, max_length=1000)),
                ('animal_age_at_collection', models.CharField(blank=True, max_length=1000)),
                ('animal_age_at_collection_unit', models.CharField(blank=True, max_length=1000)),
                ('sampling_to_preparation_interval', models.CharField(blank=True, max_length=1000)),
                ('sampling_to_preparation_interval_unit', models.CharField(blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['-data_source_id'],
            },
        ),
        migrations.RemoveField(
            model_name='sampledatainfo',
            name='sample',
        ),
        migrations.DeleteModel(
            name='AnimalInfo',
        ),
        migrations.DeleteModel(
            name='SampleDataInfo',
        ),
        migrations.DeleteModel(
            name='SampleInfo',
        ),
        migrations.AddIndex(
            model_name='specimen',
            index=models.Index(fields=['collection_place_latitude', 'collection_place_longitude'], name='backend_spe_collect_a0a983_idx'),
        ),
        migrations.AddField(
            model_name='organism',
            name='dadis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organisms', to='backend.DADISLink'),
        ),
        migrations.AddIndex(
            model_name='organism',
            index=models.Index(fields=['supplied_breed', 'efabis_breed_country'], name='backend_org_supplie_11b7e8_idx'),
        ),
        migrations.AddIndex(
            model_name='organism',
            index=models.Index(fields=['efabis_breed_country'], name='backend_org_efabis__7eea6d_idx'),
        ),
        migrations.AddIndex(
            model_name='organism',
            index=models.Index(fields=['birth_location_latitude', 'birth_location_longitude'], name='backend_org_birth_l_d60b7e_idx'),
        ),
    ]