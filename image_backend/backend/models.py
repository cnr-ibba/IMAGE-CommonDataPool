from django.db import models


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

DATE_FORMATS = (
    '%Y-%m-%d',
    '%Y-%m',
    '%Y'
)


class SampleInfo(models.Model):
    # mandatory
    biosample_id = models.CharField(max_length=100, primary_key=True)
    experiment_type = models.CharField(max_length=100, choices=EXPERIMENT_TYPE_ONTOLOGY_ID)
    experiment_target = models.CharField(max_length=100, choices=EXPERIMENT_TARGET_ONTOLOGY_ID)

    # optional
    extraction_protocol = models.CharField(max_length=100, blank=True)
    library_preparation_location = models.TextField(blank=True)
    library_preparation_location_longitude = models.DecimalField(null=True)
    library_preparation_location_latitude = models.DecimalField(null=True)
    library_preparation_date = models.DateField(input_formats=DATE_FORMATS, null=True)
    sequencing_location = models.TextField(blank=True)
    sequencing_date = models.DateField(input_formats=DATE_FORMATS, null=True)
    experimental_protocol = models.CharField(max_length=100, blank=True)
    sequencing_location_longitude = models.DecimalField(null=True)
    sequencing_location_latitude = models.DecimalField(null=True)


class AtacSeqInfo(models.Model):
    # optional
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    transposase_protocol = models.CharField(max_length=100, blank=True)


class BisulfiteSequencingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    library_selection = models.CharField(max_length=100, choices=BS_LIBRARY_SELECTION)
    bisulfite_conversion_protocol = models.CharField(max_length=100)
    pcr_product_isolation_protocol = models.CharField(max_length=100)
    bisulfite_conversion_percentage = models.IntegerField()

    # optional
    restriction_enzyme = models.CharField(max_length=100, blank=True)
    maximum_fragment_size_selection_range = models.IntegerField(null=True)
    minimum_fragment_size_selection_range = models.IntegerField(null=True)


class ChipSeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    chip_protocol = models.CharField(max_length=100)
    library_generation_maximum_fragment_size_range = models.IntegerField()
    library_generation_minimum_fragment_size_range = models.IntegerField()


class ChipSeqHistoneModificationInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    chip_antibody_provider = models.TextField()
    chip_antibody_catalog = models.TextField()
    chip_antibody_lot = models.TextField()


class DnaseHypersensitivitySeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    dnase_protocol = models.CharField(max_length=100)


class HiCInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    restriction_enzyme = models.CharField(max_length=100)
    restriction_site = models.TextField()


class RnaSeqInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(SampleInfo, on_delete=models.CASCADE)
    rna_preparation_3_adapter_ligation_protocol = models.CharField(max_length=100)
    rna_preparation_5_adapter_ligation_protocol = models.CharField(max_length=100)
    library_generation_pcr_product_isolation_protocol = models.CharField(max_length=100)
    preparation_reverse_transcription_protocol = models.CharField(max_length=100)
    library_generation_protocol = models.CharField(max_length=100)
    read_strand = models.CharField(max_length=100, choices=READ_STRAND)

    # optional
    rna_purity_260_280_ratio = models.IntegerField(null=True)
    rna_purity_260_230_ratio = models.IntegerField(null=True)
    rna_integrity_number = models.IntegerField(null=True)


