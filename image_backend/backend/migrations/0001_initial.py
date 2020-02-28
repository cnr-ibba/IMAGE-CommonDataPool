# Generated by Django 2.2.10 on 2020-02-27 13:56

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_type', models.CharField(choices=[('EFO_0007045', 'ATAC-seq'), ('EFO_0002692', 'ChIP-seq'), ('EFO_0003752', 'DNase-Hypersensitivity seq'), ('EFO_0007693', 'Hi-C'), ('OBI_0000748', 'bisulfite sequencing'), ('EFO_0002896', 'microRNA profiling by high throughput sequencing'), ('EFO_0002770', 'transcription profiling by high throughput sequencing'), ('EFO_0003738', 'RNA-seq of coding RNA'), ('EFO_0003737', 'RNA-seq of non coding RNA'), ('OBI_0002117', 'whole genome sequencing'), ('', 'genotyping SNP'), ('', 'genotyping SSR'), ('', 'genotyping other markers')], max_length=1000)),
                ('experiment_target', models.CharField(choices=[('SO_0001747', 'open_chromatin_region'), ('GO_0006306', 'DNA methylation'), ('EFO_0005031', 'input DNA'), ('SO_0001700', 'histone_modification'), ('GO_0000785', 'chromatin'), ('CHEBI_33697', 'RNA'), ('CHEBI_16991', 'deoxyribonucleic acid')], max_length=1000)),
                ('extraction_protocol', models.CharField(blank=True, max_length=1000)),
                ('library_preparation_location', models.TextField(blank=True)),
                ('library_preparation_location_longitude', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
                ('library_preparation_location_latitude', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
                ('library_preparation_date', models.DateField(null=True)),
                ('sequencing_location', models.TextField(blank=True)),
                ('sequencing_date', models.DateField(null=True)),
                ('experimental_protocol', models.CharField(blank=True, max_length=1000)),
                ('sequencing_location_longitude', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
                ('sequencing_location_latitude', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('data_source_id', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('file_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('file_url', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('file_size', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('file_checksum', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('file_checksum_method', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='SampleInfo',
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
                ('species', models.CharField(max_length=1000)),
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
            ],
        ),
        migrations.CreateModel(
            name='WholeGenomeSequencingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_generation_pcr_product_isolation_protocol', models.CharField(max_length=1000)),
                ('library_generation_protocol', models.CharField(max_length=1000)),
                ('library_selection', models.CharField(choices=[('Reduced representation', 'Reduced representation'), ('None', 'None')], max_length=1000)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='SampleDataInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('derived_from', models.CharField(max_length=1000)),
                ('collection_place_accuracy', models.CharField(max_length=1000)),
                ('organism_part', models.CharField(max_length=1000)),
                ('organism_part_ontology', models.CharField(max_length=1000)),
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
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specimens', to='backend.SampleInfo')),
            ],
        ),
        migrations.CreateModel(
            name='RnaSeqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rna_preparation_3_adapter_ligation_protocol', models.CharField(max_length=1000)),
                ('rna_preparation_5_adapter_ligation_protocol', models.CharField(max_length=1000)),
                ('library_generation_pcr_product_isolation_protocol', models.CharField(max_length=1000)),
                ('preparation_reverse_transcription_protocol', models.CharField(max_length=1000)),
                ('library_generation_protocol', models.CharField(max_length=1000)),
                ('read_strand', models.CharField(choices=[('Not applicable', 'Not applicable'), ('Sense', 'Sense'), ('Antisense', 'Antisense'), ('Mate 1 sense', 'Mate 1 sense'), ('Mate 2 sense', 'Mate 2 sense'), ('Non-stranded', 'Non-stranded')], max_length=1000)),
                ('rna_purity_260_280_ratio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('rna_purity_260_230_ratio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('rna_integrity_number', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='HiCInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restriction_enzyme', models.CharField(max_length=1000)),
                ('restriction_site', models.TextField()),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='GenotypingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotyping_protocol', models.CharField(max_length=1000)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.AddField(
            model_name='experimentinfo',
            name='data_source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.SampleInfo'),
        ),
        migrations.CreateModel(
            name='DnaseHypersensitivitySeqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dnase_protocol', models.CharField(max_length=1000)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ChipSeqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chip_protocol', models.CharField(max_length=1000)),
                ('library_generation_maximum_fragment_size_range', models.IntegerField()),
                ('library_generation_minimum_fragment_size_range', models.IntegerField()),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ChipSeqHistoneModificationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chip_antibody_provider', models.TextField()),
                ('chip_antibody_catalog', models.TextField()),
                ('chip_antibody_lot', models.TextField()),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='BisulfiteSequencingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_selection', models.CharField(choices=[('OBI_0001863', 'whole genome bisulfite sequencing'), ('OBI_0001862', 'reduced representation bisulfite-seq'), ('OBI_0002086', 'Tet-assisted bisulfite sequencing assay'), ('OBI_0002094', 'MethylC-Capture sequencing assay')], max_length=1000)),
                ('bisulfite_conversion_protocol', models.CharField(max_length=1000)),
                ('pcr_product_isolation_protocol', models.CharField(max_length=1000)),
                ('bisulfite_conversion_percentage', models.IntegerField()),
                ('restriction_enzyme', models.CharField(blank=True, max_length=1000)),
                ('maximum_fragment_size_selection_range', models.IntegerField(null=True)),
                ('minimum_fragment_size_selection_range', models.IntegerField(null=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='AtacSeqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transposase_protocol', models.CharField(blank=True, max_length=1000)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.ExperimentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='AnimalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('specimens', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, default=[], size=None)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisms', to='backend.SampleInfo')),
            ],
        ),
    ]
