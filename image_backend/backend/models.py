from django.db import models
from django.contrib.postgres.fields import ArrayField


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
    project = models.CharField(max_length=100)
    submission_title = models.TextField()
    material = models.CharField(max_length=100)
    material_ontology = models.CharField(max_length=100,)
    person_last_name = ArrayField(models.CharField(max_length=100))
    person_email = ArrayField(models.EmailField())
    person_affiliation = ArrayField(models.CharField(max_length=100))
    person_role = ArrayField(models.CharField(max_length=100))
    person_role_ontology = ArrayField(models.CharField(max_length=100))
    organization_name = ArrayField(models.CharField(max_length=100))
    organization_role = ArrayField(models.CharField(max_length=100))
    organization_role_ontology = ArrayField(models.CharField(max_length=100))
    gene_bank_name = models.CharField(max_length=100)
    gene_bank_country = models.CharField(max_length=100)
    gene_bank_country_ontology = models.CharField(max_length=100,)
    data_source_type = models.CharField(max_length=100)
    data_source_version = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    species_ontology = models.CharField(max_length=100)

    # recommended
    submission_description = models.TextField(blank=True)
    person_first_name = ArrayField(models.CharField(max_length=100,
                                                    blank=True), blank=True)
    organization_address = ArrayField(models.TextField(blank=True), blank=True)
    organization_country = ArrayField(models.CharField(max_length=100,
                                                       blank=True), blank=True)
    organization_country_ontology = ArrayField(
        models.CharField(max_length=100, blank=True), blank=True)

    # optional
    description = models.TextField(blank=True)
    person_initial = ArrayField(models.CharField(max_length=100, blank=True),
                                blank=True)
    organization_uri = ArrayField(models.TextField(blank=True), blank=True)
    publication_doi = models.CharField(max_length=100, blank=True)


class AnimalInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="organisms",
                               on_delete=models.CASCADE)
    supplied_breed = models.CharField(max_length=100)
    efabis_breed_country = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    sex_ontology = models.CharField(max_length=100)
    birth_location_accuracy = models.CharField(max_length=100)

    # recommended
    mapped_breed = models.CharField(max_length=100, blank=True)
    mapped_breed_ontology = models.CharField(max_length=100, blank=True)
    birth_date = models.CharField(max_length=100, blank=True)
    birth_date_unit = models.CharField(max_length=100, blank=True)
    birth_location = models.CharField(max_length=100, blank=True)
    birth_location_longitude = models.DecimalField(decimal_places=10,
                                                   max_digits=20, blank=True,
                                                   null=True)
    birth_location_longitude_unit = models.CharField(max_length=100,
                                                     blank=True)
    birth_location_latitude = models.DecimalField(decimal_places=10,
                                                  max_digits=20, blank=True,
                                                  null=True)
    birth_location_latitude_unit = models.CharField(max_length=100,
                                                    blank=True)

    # optional
    child_of = ArrayField(models.CharField(max_length=100, blank=True),
                          size=2, blank=True)


class SampleDataInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="specimens",
                               on_delete=models.CASCADE)
    derived_from = models.CharField(max_length=100)
    collection_place_accuracy = models.CharField(max_length=100)
    organism_part = models.CharField(max_length=100)
    organism_part_ontology = models.CharField(max_length=100)

    # recommended
    specimen_collection_protocol = models.CharField(max_length=100, blank=True)
    collection_date = models.DateField(blank=True, null=True)
    collection_date_unit = models.CharField(max_length=100, blank=True)
    collection_place_latitude = models.DecimalField(decimal_places=10,
                                                    max_digits=20, blank=True,
                                                    null=True)
    collection_place_latitude_unit = models.CharField(max_length=100,
                                                      blank=True)
    collection_place_longitude = models.DecimalField(decimal_places=10,
                                                     max_digits=20, blank=True,
                                                     null=True)
    collection_place_longitude_unit = models.CharField(max_length=100,
                                                       blank=True)
    collection_place = models.CharField(max_length=100, blank=True)
    developmental_stage = models.CharField(max_length=100, blank=True)
    developmental_stage_ontology = models.CharField(max_length=100, blank=True)
    physiological_stage = models.CharField(max_length=100, blank=True)
    physiological_stage_ontology = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    sample_storage = models.CharField(max_length=100, blank=True)
    sample_storage_processing = models.CharField(max_length=100, blank=True)

    # optional
    animal_age_at_collection = models.IntegerField(blank=True, null=True)
    animal_age_at_collection_unit = models.CharField(max_length=100,
                                                     blank=True)
    sampling_to_preparation_interval = models.IntegerField(blank=True,
                                                           null=True)
    sampling_to_preparation_interval_unit = models.CharField(max_length=100,
                                                             blank=True)


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

