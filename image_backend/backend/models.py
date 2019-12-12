from django.db import models
from django_postgres_extensions.models.fields import ArrayField

PROJECT_TYPES = (
    ('IMAGE', 'IMAGE'),
)

MATERIAL = (
    ('organism', 'organism'),
    ('specimen from organism', 'specimen from organism'),
)

MATERIAL_ONTOLOGY = (
    ('OBI_010002', 'OBI_010002'),
    ('OBI_0001479', 'OBI_0001479')
)

COUNTRIES = (
    ('France', 'France'),
    ('Egypt', 'Egypt'),
    ('Colombia', 'Colombia'),
    ('Switzerland', 'Switzerland'),
    ('Netherlands', 'Netherlands'),
    ('Germany', 'Germany'),
    ('Italy', 'Italy'),
    ('Hungary', 'Hungary'),
    ('Morocco', 'Morocco'),
    ('Spain', 'Spain'),
    ('Argentina', 'Argentina'),
    ('Sweden', 'Sweden'),
    ('United Kingdom', 'United Kingdom'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Austria', 'Austria')
)

COUNTRIES_ONTOLOGY = (
    ('NCIT_C16592', 'NCIT_C16592'),
    ('NCIT_C16530', 'NCIT_C16530'),
    ('NCIT_C16449', 'NCIT_C16449'),
    ('NCIT_C17181', 'NCIT_C17181'),
    ('NCIT_C16903', 'NCIT_C16903'),
    ('NCIT_C16636', 'NCIT_C16636'),
    ('NCIT_C16761', 'NCIT_C16761'),
    ('NCIT_C16699', 'NCIT_C16699'),
    ('NCIT_C16878', 'NCIT_C16878'),
    ('NCIT_C17152', 'NCIT_C17152'),
    ('NCIT_C16305', 'NCIT_C16305'),
    ('NCIT_C17180', 'NCIT_C17180'),
    ('NCIT_C17233', 'NCIT_C17233'),
    ('NCIT_C17002', 'NCIT_C17002'),
    ('NCIT_C17006', 'NCIT_C17006'),
    ('NCIT_C16312', 'NCIT_C16312')
)

DATA_SOURCE_TYPE = (
    ('CyroWeb', 'CyroWeb'),
    ('CRB-Anim', 'CRB-Anim'),
    ('Template', 'Template')
)

DATE_UNITS = (
    ('YYYY-MM-DD', 'YYYY-MM-DD'),
    ('YYYY-MM', 'YYYY-MM'),
    ('YYYY', 'YYYY')
)

LOCATION_UNITS = (
    ('decimal degrees', 'decimal degrees'),
)

LOCATION_ACCURACY = (
    ('missing geographic information', 'missing geographic information'),
    ('country level', 'country level'),
    ('region level', 'region level'),
    ('precise coordinates', 'precise coordinates'),
    ('unknown accuracy level', 'unknown accuracy level')
)

AGE_UNITS = (
    ('minutes', 'minutes'),
    ('hours', 'hours'),
    ('month', 'month'),
    ('year', 'year'),
    ('days', 'days'),
    ('weeks', 'weeks'),
    ('months', 'months'),
    ('years', 'years'),
    ('minute', 'minute'),
    ('hour', 'hour'),
    ('day', 'day'),
    ('week', 'week')
)

SAMPLE_STORAGE = (
    ('ambient temperature', 'ambient temperature'),
    ('cut slide', 'cut slide'),
    ('frozen, -80 degrees Celsius freezer',
     'frozen, -80 degrees Celsius freezer'),
    ('frozen, -40 degrees Celsius freezer',
     'frozen, -40 degrees Celsius freezer'),
    ('frozen, -20 degrees Celsius freezer',
     'frozen, -20 degrees Celsius freezer'),
    ('frozen, liquid nitrogen', 'frozen, liquid nitrogen'),
    ('frozen, vapor phase', 'frozen, vapor phase'),
    ('paraffin block', 'paraffin block'),
    ('RNAlater, frozen -20 degrees Celsius',
     'RNAlater, frozen -20 degrees Celsius'),
    ('TRIzol, frozen', 'TRIzol, frozen'),
    ('paraffin block at ambient temperatures (+15 to +30 degrees Celsius)',
     'paraffin block at ambient temperatures (+15 to +30 degrees Celsius)'),
    ('freeze dried', 'freeze dried'),
)

SAMPLE_STORAGE_PROCESSING = (
    ('cryopreservation in liquid nitrogen (dead tissue)',
     'cryopreservation in liquid nitrogen (dead tissue)'),
    ('cryopreservation in dry ice (dead tissue)',
     'cryopreservation in dry ice (dead tissue)'),
    ('cryopreservation of live cells in liquid nitrogen',
     'cryopreservation of live cells in liquid nitrogen'),
    ('cryopreservation, other', 'cryopreservation, other'),
    ('formalin fixed, unbuffered', 'formalin fixed, unbuffered'),
    ('formalin fixed, buffered', 'formalin fixed, buffered'),
    ('formalin fixed and paraffin embedded',
     'formalin fixed and paraffin embedded'),
    ('freeze dried (vaiable for reproduction)',
     'freeze dried (vaiable for reproduction)'),
    ('freeze dried', 'freeze dried')
)

EXPERIMENT_TYPE_ONTOLOGY_ID = (
    ('EFO_0007045', 'ATAC-seq'),
    ('EFO_0002692', 'ChIP-seq'),
    ('EFO_0003752', 'DNase-Hypersensitivity seq'),
    ('EFO_0007693', 'Hi-C'),
    ('OBI_0000748', 'bisulfite sequencing'),
    ('EFO_0002896', 'microRNA profiling by high throughput sequencing'),
    ('EFO_0002770', 'transcription profiling by high throughput sequencing'),
    ('EFO_0003738', 'RNA-seq of coding RNA'),
    ('EFO_0003737', 'RNA-seq of non coding RNA'),
    ('OBI_0002117', 'whole genome sequencing'),
    ('', 'genotyping SNP'),
    ('', 'genotyping SSR'),
    ('', 'genotyping other markers')
)

EXPERIMENT_TARGET_ONTOLOGY_ID = (
    ('SO_0001747', 'open_chromatin_region'),
    ('GO_0006306', 'DNA methylation'),
    ('EFO_0005031', 'input DNA'),
    ('SO_0001700', 'histone_modification'),
    ('GO_0000785', 'chromatin'),
    ('CHEBI_33697', 'RNA'),
    ('CHEBI_16991', 'deoxyribonucleic acid'),
)

BS_LIBRARY_SELECTION = (
    ('OBI_0001863', 'whole genome bisulfite sequencing'),
    ('OBI_0001862', 'reduced representation bisulfite-seq'),
    ('OBI_0002086', 'Tet-assisted bisulfite sequencing assay'),
    ('OBI_0002094', 'MethylC-Capture sequencing assay')
)

READ_STRAND = (
    ('Not applicable', 'Not applicable'),
    ('Sense', 'Sense'),
    ('Antisense', 'Antisense'),
    ('Mate 1 sense', 'Mate 1 sense'),
    ('Mate 2 sense', 'Mate 2 sense'),
    ('Non-stranded', 'Non-stranded'),
)

WGC_LIBRARY_SELCTION = (
    ('Reduced representation', 'Reduced representation'),
    ('None', 'None'),
)


class SampleInfo(models.Model):
    # mandatory
    data_source_id = models.CharField(max_length=100, primary_key=True)
    alternative_id = models.CharField(max_length=100)
    project = models.CharField(max_length=100, choices=PROJECT_TYPES)
    submission_title = models.TextField()
    material = models.CharField(max_length=100, choices=MATERIAL)
    material_ontology = models.CharField(max_length=100,
                                         choices=MATERIAL_ONTOLOGY)
    person_lat_name = ArrayField(models.CharField(max_length=100))
    person_email = ArrayField(models.EmailField())
    person_affiliation = ArrayField(models.CharField(max_length=100))
    person_role = ArrayField(models.CharField(max_length=100))
    person_role_ontology = ArrayField(models.CharField(max_length=100))
    organization_name = ArrayField(models.CharField(max_length=100))
    organization_role = ArrayField(models.CharField(max_length=100))
    organization_role_ontology = ArrayField(models.CharField(max_length=100))
    gene_bank_name = models.CharField(max_length=100)
    gene_bank_country = models.CharField(max_length=100, choices=COUNTRIES)
    gene_bank_country_ontology = models.CharField(max_length=100,
                                                  choices=COUNTRIES_ONTOLOGY)
    data_source_type = models.CharField(max_length=100,
                                        choices=DATA_SOURCE_TYPE)
    data_source_version = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    species_ontology = models.CharField(max_length=100)

    # recommended
    submission_description = models.TextField(blank=True)
    person_first_name = ArrayField(models.CharField(max_length=100, blank=True))
    organization_address = ArrayField(models.TextField(blank=True))
    organization_country = ArrayField(models.CharField(max_length=100,
                                                       choices=COUNTRIES,
                                                       blank=True))
    organization_country_ontology = ArrayField(
        models.CharField(max_length=100, choices=COUNTRIES_ONTOLOGY,
                         blank=True))

    # optional
    description = models.TextField(blank=True)
    person_initial = ArrayField(models.CharField(max_length=100, blank=True))
    organization_uri = ArrayField(models.TextField(blank=True))
    publication_doi = models.CharField(max_length=100, blank=True)


class AnimalInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="organisms",
                               on_delete=models.CASCADE)
    supplied_breed = models.CharField(max_length=100)
    efabis_breed_country = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    sex_ontology = models.CharField(max_length=100)
    birth_location_accuracy = models.CharField(max_length=100,
                                               choices=LOCATION_ACCURACY)

    # recommended
    mapped_breed = models.CharField(max_length=100, blank=True)
    mapped_breed_ontology = models.CharField(max_length=100, blank=True)
    birth_date = models.CharField(max_length=100, blank=True)
    birth_date_unit = models.CharField(max_length=100, blank=True,
                                       choices=DATE_UNITS)
    birth_location = models.CharField(max_length=100, blank=True)
    birth_location_longitude = models.DecimalField(decimal_places=10,
                                                   max_digits=20, blank=True,
                                                   null=True)
    birth_location_longitude_unit = models.CharField(max_length=100,
                                                     blank=True,
                                                     choices=LOCATION_UNITS)
    birth_location_latitude = models.DecimalField(decimal_places=10,
                                                  max_digits=20, blank=True,
                                                  null=True)
    birth_location_latitude_unit = models.CharField(max_length=100,
                                                    blank=True,
                                                    choices=LOCATION_UNITS)

    # optional
    child_of = ArrayField(models.CharField(max_length=100, blank=True), size=2)


class SampleDataInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="specimens",
                               on_delete=models.CASCADE)
    derived_from = models.CharField(max_length=100)
    collection_place_accuracy = models.CharField(max_length=100,
                                                 choices=LOCATION_ACCURACY)
    organism_part = models.CharField(max_length=100)
    organism_part_ontology = models.CharField(max_length=100)

    # recommended
    specimen_collection_protocol = models.CharField(max_length=100, blank=True)
    collection_date = models.DateField(blank=True)
    collection_date_unit = models.CharField(max_length=100, blank=True,
                                            choices=DATE_UNITS)
    collection_place_latitude = models.DecimalField(decimal_places=10,
                                                    max_digits=20, blank=True,
                                                    null=True)
    collection_place_latitude_unit = models.CharField(max_length=100,
                                                      blank=True,
                                                      choices=LOCATION_UNITS)
    collection_place_longitude = models.DecimalField(decimal_places=10,
                                                     max_digits=20, blank=True,
                                                     null=True)
    collection_place_longitude_unit = models.CharField(max_length=100,
                                                       blank=True,
                                                       choices=LOCATION_UNITS)
    collection_place = models.CharField(max_length=100, blank=True)
    developmental_stage = models.CharField(max_length=100, blank=True)
    developmental_stage_ontology = models.CharField(max_length=100, blank=True)
    physiological_stage = models.CharField(max_length=100, blank=True)
    physiological_stage_ontology = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    sample_storage = models.CharField(max_length=100, choices=SAMPLE_STORAGE,
                                      blank=True)
    sample_storage_processing = models.CharField(
        max_length=100,
        choices=SAMPLE_STORAGE_PROCESSING,
        blank=True)

    # optional
    animal_age_at_collection = models.IntegerField(blank=True, null=True)
    animal_age_at_collection_unit = models.CharField(max_length=100,
                                                     blank=True,
                                                     choices=AGE_UNITS)
    sampling_to_preparation_interval = models.IntegerField(blank=True,
                                                           null=True)
    sampling_to_preparation_interval_unit = models.CharField(max_length=100,
                                                             blank=True,
                                                             choices=AGE_UNITS)


class ExperimentInfo(models.Model):
    # mandatory
    data_source_id = models.ForeignKey(SampleInfo, on_delete=models.CASCADE)
    experiment_type = models.CharField(max_length=100,
                                       choices=EXPERIMENT_TYPE_ONTOLOGY_ID)
    experiment_target = models.CharField(max_length=100,
                                         choices=EXPERIMENT_TARGET_ONTOLOGY_ID)

    # optional
    extraction_protocol = models.CharField(max_length=100, blank=True)
    library_preparation_location = models.TextField(blank=True)
    library_preparation_location_longitude = models.DecimalField(
        decimal_places=10, max_digits=20, null=True)
    library_preparation_location_latitude = models.DecimalField(
        decimal_places=10, max_digits=20, null=True)
    library_preparation_date = models.DateField(null=True)
    sequencing_location = models.TextField(blank=True)
    sequencing_date = models.DateField(null=True)
    experimental_protocol = models.CharField(max_length=100, blank=True)
    sequencing_location_longitude = models.DecimalField(
        decimal_places=10, max_digits=20, null=True)
    sequencing_location_latitude = models.DecimalField(
        decimal_places=10, max_digits=20, null=True)


class AtacSeqInfo(models.Model):
    # optional
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    transposase_protocol = models.CharField(max_length=100, blank=True)


class BisulfiteSequencingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    library_selection = models.CharField(max_length=100,
                                         choices=BS_LIBRARY_SELECTION)
    bisulfite_conversion_protocol = models.CharField(max_length=100)
    pcr_product_isolation_protocol = models.CharField(max_length=100)
    bisulfite_conversion_percentage = models.IntegerField()

    # optional
    restriction_enzyme = models.CharField(max_length=100, blank=True)
    maximum_fragment_size_selection_range = models.IntegerField(null=True)
    minimum_fragment_size_selection_range = models.IntegerField(null=True)


class ChipSeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    chip_protocol = models.CharField(max_length=100)
    library_generation_maximum_fragment_size_range = models.IntegerField()
    library_generation_minimum_fragment_size_range = models.IntegerField()


class ChipSeqHistoneModificationInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    chip_antibody_provider = models.TextField()
    chip_antibody_catalog = models.TextField()
    chip_antibody_lot = models.TextField()


class DnaseHypersensitivitySeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    dnase_protocol = models.CharField(max_length=100)


class HiCInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    restriction_enzyme = models.CharField(max_length=100)
    restriction_site = models.TextField()


class RnaSeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    rna_preparation_3_adapter_ligation_protocol = models.CharField(
        max_length=100)
    rna_preparation_5_adapter_ligation_protocol = models.CharField(
        max_length=100)
    library_generation_pcr_product_isolation_protocol = models.CharField(
        max_length=100)
    preparation_reverse_transcription_protocol = models.CharField(
        max_length=100)
    library_generation_protocol = models.CharField(max_length=100)
    read_strand = models.CharField(max_length=100, choices=READ_STRAND)

    # optional
    rna_purity_260_280_ratio = models.DecimalField(decimal_places=2,
                                                   max_digits=10, null=True)
    rna_purity_260_230_ratio = models.DecimalField(decimal_places=2,
                                                   max_digits=10, null=True)
    rna_integrity_number = models.DecimalField(decimal_places=2,
                                               max_digits=10, null=True)


class WholeGenomeSequencingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    library_generation_pcr_product_isolation_protocol = models.CharField(
        max_length=100)
    library_generation_protocol = models.CharField(max_length=100)

    # optional
    library_selection = models.CharField(max_length=100,
                                         choices=WGC_LIBRARY_SELCTION)


class GenotypingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    genotyping_protocol = models.CharField(max_length=100)

