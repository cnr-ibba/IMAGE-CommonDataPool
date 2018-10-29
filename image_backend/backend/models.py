from django.db import models

PROJECT_TYPES = (
    ('IMAGE', 'IMAGE'),
)

MATERIAL = (
    ('Organism', 'Organism'),
    ('Specimen from organism', 'Specimen from organism'),
)

COUNTRIES = (
    ('AFG', 'Afghanistan'), ('ALA', 'Aland Islands'), ('ALB', 'Albania'), ('DZA', 'Algeria'), ('ASM', 'American Samoa'),
    ('AND', 'Andorra'), ('AGO', 'Angola'), ('AIA', 'Anguilla'), ('ATA', 'Antarctica'), ('ATG', 'Antigua and Barbuda'),
    ('ARG', 'Argentina'), ('ARM', 'Armenia'), ('ABW', 'Aruba'), ('AUS', 'Australia'), ('AUT', 'Austria'),
    ('AZE', 'Azerbaijan'), ('BHS', 'Bahamas'), ('BHR', 'Bahrain'), ('BGD', 'Bangladesh'), ('BRB', 'Barbados'),
    ('BLR', 'Belarus'), ('BEL', 'Belgium'), ('BLZ', 'Belize'), ('BEN', 'Benin'), ('BMU', 'Bermuda'), ('BTN', 'Bhutan'),
    ('BOL', 'Bolivia (Plurinational State of)'), ('BES', 'Bonaire, Sint Eustatius and Saba'),
    ('BIH', 'Bosnia and Herzegovina'), ('BWA', 'Botswana'), ('BVT', 'Bouvet Island'), ('BRA', 'Brazil'),
    ('IOT', 'British Indian Ocean Territory'), ('VGB', 'British Virgin Islands'), ('BRN', 'Brunei Darussalam'),
    ('BGR', 'Bulgaria'), ('BFA', 'Burkina Faso'), ('BDI', 'Burundi'), ('CPV', 'Cabo Verde'), ('KHM', 'Cambodia'),
    ('CMR', 'Cameroon'), ('CAN', 'Canada'), ('CYM', 'Cayman Islands'), ('CAF', 'Central African Republic'),
    ('TCD', 'Chad'), ('CHL', 'Chile'), ('CHN', 'China'), ('HKG', 'China, Hong Kong Special Administrative Region'),
    ('MAC', 'China, Macao Special Administrative Region'), ('CXR', 'Christmas Island'),
    ('CCK', 'Cocos (Keeling) Islands'), ('COL', 'Colombia'), ('COM', 'Comoros'), ('COG', 'Congo'),
    ('COK', 'Cook Islands'), ('CRI', 'Costa Rica'), ('CIV', "Cote d'ivoire"), ('HRV', 'Croatia'), ('CUB', 'Cuba'),
    ('CUW', 'Curacao'), ('CYP', 'Cyprus'), ('CZE', 'Czechia'), ('PRK', "Democratic People's Republic of Korea"),
    ('COD', 'Democratic Republic of the Congo'), ('DNK', 'Denmark'), ('DJI', 'Djibouti'), ('DMA', 'Dominica'),
    ('DOM', 'Dominican Republic'), ('ECU', 'Ecuador'), ('EGY', 'Egypt'), ('SLV', 'El Salvador'),
    ('GNQ', 'Equatorial Guinea'), ('ERI', 'Eritrea'), ('EST', 'Estonia'), ('SWZ', 'Eswatini'), ('ETH', 'Ethiopia'),
    ('FLK', 'Falkland Islands (Malvinas)'), ('FRO', 'Faroe Islands'), ('FJI', 'Fiji'), ('FIN', 'Finland'),
    ('FRA', 'France'), ('GUF', 'French Guiana'), ('PYF', 'French Polynesia'), ('ATF', 'French Southern Territories'),
    ('GAB', 'Gabon'), ('GMB', 'Gambia'), ('GEO', 'Georgia'), ('DEU', 'Germany'), ('GHA', 'Ghana'), ('GIB', 'Gibraltar'),
    ('GRC', 'Greece'), ('GRL', 'Greenland'), ('GRD', 'Grenada'), ('GLP', 'Guadeloupe'), ('GUM', 'Guam'),
    ('GTM', 'Guatemala'), ('GGY', 'Guernsey'), ('GIN', 'Guinea'), ('GNB', 'Guinea-Bissau'), ('GUY', 'Guyana'),
    ('HTI', 'Haiti'), ('HMD', 'Heard Island and McDonald Islands'), ('VAT', 'Holy See'), ('HND', 'Honduras'),
    ('HUN', 'Hungary'), ('ISL', 'Iceland'), ('IND', 'India'), ('IDN', 'Indonesia'),
    ('IRN', 'Iran (Islamic Republic of)'), ('IRQ', 'Iraq'), ('IRL', 'Ireland'), ('IMN', 'Isle of Man'),
    ('ISR', 'Israel'), ('ITA', 'Italy'), ('JAM', 'Jamaica'), ('JPN', 'Japan'), ('JEY', 'Jersey'), ('JOR', 'Jordan'),
    ('KAZ', 'Kazakhstan'), ('KEN', 'Kenya'), ('KIR', 'Kiribati'), ('KWT', 'Kuwait'), ('KGZ', 'Kyrgyzstan'),
    ('LAO', "Lao People's Democratic Republic"), ('LVA', 'Latvia'), ('LBN', 'Lebanon'), ('LSO', 'Lesotho'),
    ('LBR', 'Liberia'), ('LBY', 'Libya'), ('LIE', 'Liechtenstein'), ('LTU', 'Lithuania'), ('LUX', 'Luxembourg'),
    ('MDG', 'Madagascar'), ('MWI', 'Malawi'), ('MYS', 'Malaysia'), ('MDV', 'Maldives'), ('MLI', 'Mali'),
    ('MLT', 'Malta'), ('MHL', 'Marshall Islands'), ('MTQ', 'Martinique'), ('MRT', 'Mauritania'), ('MUS', 'Mauritius'),
    ('MYT', 'Mayotte'), ('MEX', 'Mexico'), ('FSM', 'Micronesia (Federated States of)'), ('MCO', 'Monaco'),
    ('MNG', 'Mongolia'), ('MNE', 'Montenegro'), ('MSR', 'Montserrat'), ('MAR', 'Morocco'), ('MOZ', 'Mozambique'),
    ('MMR', 'Myanmar'), ('NAM', 'Namibia'), ('NRU', 'Nauru'), ('NPL', 'Nepal'), ('NLD', 'Netherlands'),
    ('NCL', 'New Caledonia'), ('NZL', 'New Zealand'), ('NIC', 'Nicaragua'), ('NER', 'Niger'), ('NGA', 'Nigeria'),
    ('NIU', 'Niue'), ('NFK', 'Norfolk Island'), ('MNP', 'Northern Mariana Islands'), ('NOR', 'Norway'), ('OMN', 'Oman'),
    ('PAK', 'Pakistan'), ('PLW', 'Palau'), ('PAN', 'Panama'), ('PNG', 'Papua New Guinea'), ('PRY', 'Paraguay'),
    ('PER', 'Peru'), ('PHL', 'Philippines'), ('PCN', 'Pitcairn'), ('POL', 'Poland'), ('PRT', 'Portugal'),
    ('PRI', 'Puerto Rico'), ('QAT', 'Qatar'), ('KOR', 'Republic of Korea'), ('MDA', 'Republic of Moldova'),
    ('REU', 'Reunion'), ('ROU', 'Romania'), ('RUS', 'Russian Federation'), ('RWA', 'Rwanda'),
    ('BLM', 'Saint Barthelemy'), ('SHN', 'Saint Helena'), ('KNA', 'Saint Kitts and Nevis'), ('LCA', 'Saint Lucia'),
    ('MAF', 'Saint Martin (French Part)'), ('SPM', 'Saint Pierre and Miquelon'),
    ('VCT', 'Saint Vincent and the Grenadines'), ('WSM', 'Samoa'), ('SMR', 'San Marino'),
    ('STP', 'Sao Tome and Principe'), ('Sark', 'Sark'), ('SAU', 'Saudi Arabia'), ('SEN', 'Senegal'), ('SRB', 'Serbia'),
    ('SYC', 'Seychelles'), ('SLE', 'Sierra Leone'), ('SGP', 'Singapore'), ('SXM', 'Sint Maarten (Dutch part)'),
    ('SVK', 'Slovakia'), ('SVN', 'Slovenia'), ('SLB', 'Solomon Islands'), ('SOM', 'Somalia'), ('ZAF', 'South Africa'),
    ('SGS', 'South Georgia and the South Sandwich Islands'), ('SSD', 'South Sudan'), ('ESP', 'Spain'),
    ('LKA', 'Sri Lanka'), ('PSE', 'State of Palestine'), ('SDN', 'Sudan'), ('SUR', 'Suriname'),
    ('SJM', 'Svalbard and Jan Mayen Islands'), ('SWE', 'Sweden'), ('CHE', 'Switzerland'),
    ('SYR', 'Syrian Arab Republic'), ('TJK', 'Tajikistan'), ('THA', 'Thailand'),
    ('MKD', 'The former Yugoslav Republic of Macedonia'), ('TLS', 'Timor-Leste'), ('TGO', 'Togo'), ('TKL', 'Tokelau'),
    ('TON', 'Tonga'), ('TTO', 'Trinidad and Tobago'), ('TUN', 'Tunisia'), ('TUR', 'Turkey'), ('TKM', 'Turkmenistan'),
    ('TCA', 'Turks and Caicos Islands'), ('TUV', 'Tuvalu'), ('UGA', 'Uganda'), ('UKR', 'Ukraine'),
    ('ARE', 'United Arab Emirates'), ('GBR', 'United Kingdom of Great Britain and Northern Ireland'),
    ('TZA', 'United Republic of Tanzania'), ('UMI', 'United States Minor Outlying Islands'),
    ('USA', 'United States of America'), ('VIR', 'United States Virgin Islands'), ('URY', 'Uruguay'),
    ('UZB', 'Uzbekistan'), ('VUT', 'Vanuatu'), ('VEN', 'Venezuela (Bolivarian Republic of)'), ('VNM', 'Viet Nam'),
    ('WLF', 'Wallis and Futuna Islands'), ('ESH', 'Western Sahara'), ('YEM', 'Yemen'), ('ZMB', 'Zambia'),
    ('ZWE', 'Zimbabwe'))

DATA_SOURCE_TYPE = (
    ('CyroWeb', 'CyroWeb'),
    ('CRB-Anim', 'CRB-Anim'),
    ('Template', 'Template')
)

LOCATION_ACCURACY = (
    ('missing geographic information', 'missing geographic information'),
    ('country level', 'country level'),
    ('region level', 'region level'),
    ('subregion level', 'subregion level'),
    ('precise coordinates', 'precise coordinates'),
)

SAMPLE_STORAGE = (
    ('ambient temperature', 'ambient temperature'),
    ('cut slide', 'cut slide'),
    ('frozen, -80 degrees Celsius freezer', 'frozen, -80 degrees Celsius freezer'),
    ('frozen, -20 degrees Celsius freezer', 'frozen, -20 degrees Celsius freezer'),
    ('frozen, liquid nitrogen', 'frozen, liquid nitrogen'),
    ('frozen, vapor phase', 'frozen, vapor phase'),
    ('paraffin block', 'paraffin block'),
    ('RNAlater, frozen -20 degrees Celsius', 'RNAlater, frozen -20 degrees Celsius'),
    ('TRIzol, frozen', 'TRIzol, frozen'),
    ('paraffin block at ambient temperatures (+15 to +30 degrees Celsius)',
     'paraffin block at ambient temperatures (+15 to +30 degrees Celsius)'),
    ('freeze dried', 'freeze dried'),
)

SAMPLE_STORAGE_PROCESSING = (
    ('cryopreservation in liquid nitrogen (dead tissue)', 'cryopreservation in liquid nitrogen (dead tissue)'),
    ('cryopreservation in dry ice (dead tissue)', 'cryopreservation in dry ice (dead tissue)'),
    ('cryopreservation of live cells in liquid nitrogen', 'cryopreservation of live cells in liquid nitrogen'),
    ('cryopreservation, other', 'cryopreservation, other'),
    ('formalin fixed, unbuffered', 'formalin fixed, unbuffered'),
    ('formalin fixed, buffered', 'formalin fixed, buffered'),
    ('formalin fixed and paraffin embedded', 'formalin fixed and paraffin embedded'),
    ('freeze dried (vaiable for reproduction)', 'freeze dried (vaiable for reproduction)'),
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
    submission_title = models.CharField(max_length=100)
    material = models.CharField(max_length=100, choices=MATERIAL)
    person_last_name = models.CharField(max_length=100)
    person_email = models.EmailField()  # todo check that it is mandatory
    person_affiliation = models.CharField(max_length=100)
    person_role = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)
    organization_role = models.CharField(max_length=100)
    gene_bank_name = models.CharField(max_length=100)
    gene_bank_country = models.CharField(max_length=100, choices=COUNTRIES)
    data_source_type = models.CharField(max_length=100, choices=DATA_SOURCE_TYPE)
    data_source_version = models.CharField(max_length=100)  # todo check that it is mandatory
    species = models.CharField(max_length=100)

    # optional
    submission_description = models.CharField(max_length=100, blank=True)
    person_first_name = models.CharField(max_length=100, blank=True)
    organization_address = models.TextField(blank=True)
    organization_country = models.CharField(max_length=100, choices=COUNTRIES, blank=True)
    description = models.TextField(blank=True)
    person_initial = models.TextField(blank=True)
    organization_uri = models.TextField(blank=True)
    publication_doi = models.CharField(max_length=100, blank=True)


class AnimalInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="organisms", on_delete=models.CASCADE)
    supplied_breed = models.CharField(max_length=100)
    efabis_breed_country = models.CharField(max_length=100, choices=COUNTRIES)
    sex = models.CharField(max_length=100)
    birth_location_accuracy = models.CharField(max_length=100, choices=LOCATION_ACCURACY)  # todo check that it is mandatory

    # optional
    mapped_breed = models.CharField(max_length=100, blank=True)
    birth_location = models.TextField(blank=True)
    birth_location_longitude = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    birth_location_latitude = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    child_of = models.CharField(max_length=100, blank=True)


class SampleDataInfo(models.Model):
    # mandatory
    sample = models.ForeignKey(SampleInfo, related_name="specimens", on_delete=models.CASCADE)
    derived_from = models.CharField(max_length=100)
    collection_date = models.DateField()
    collection_place = models.CharField(max_length=100)  # todo check that it is mandatory
    collection_place_accuracy = models.CharField(max_length=100, choices=LOCATION_ACCURACY)  # todo check that it is mandatory
    organism_part = models.CharField(max_length=100)

    # optional
    specimen_collection_protocol = models.CharField(max_length=100, blank=True)
    collection_place_latitude = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    collection_place_longitude = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    developmental_stage = models.CharField(max_length=100, blank=True)
    physiological_stage = models.CharField(max_length=100, blank=True)
    availability = models.TextField(blank=True)
    sample_storage = models.CharField(max_length=100, choices=SAMPLE_STORAGE, blank=True)
    sample_storage_processing = models.CharField(max_length=100, choices=SAMPLE_STORAGE_PROCESSING, blank=True)
    animal_age_at_collection = models.IntegerField(blank=True)
    sampling_to_preparation_interval = models.IntegerField(blank=True)


class ExperimentInfo(models.Model):
    # mandatory
    data_source_id = models.ForeignKey(SampleInfo, on_delete=models.CASCADE)
    experiment_type = models.CharField(max_length=100, choices=EXPERIMENT_TYPE_ONTOLOGY_ID)
    experiment_target = models.CharField(max_length=100, choices=EXPERIMENT_TARGET_ONTOLOGY_ID)

    # optional
    extraction_protocol = models.CharField(max_length=100, blank=True)
    library_preparation_location = models.TextField(blank=True)
    library_preparation_location_longitude = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    library_preparation_location_latitude = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    library_preparation_date = models.DateField(null=True)
    sequencing_location = models.TextField(blank=True)
    sequencing_date = models.DateField(null=True)
    experimental_protocol = models.CharField(max_length=100, blank=True)
    sequencing_location_longitude = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    sequencing_location_latitude = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class AtacSeqInfo(models.Model):
    # optional
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    transposase_protocol = models.CharField(max_length=100, blank=True)


class BisulfiteSequencingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
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
    rna_preparation_3_adapter_ligation_protocol = models.CharField(max_length=100)
    rna_preparation_5_adapter_ligation_protocol = models.CharField(max_length=100)
    library_generation_pcr_product_isolation_protocol = models.CharField(max_length=100)
    preparation_reverse_transcription_protocol = models.CharField(max_length=100)
    library_generation_protocol = models.CharField(max_length=100)
    read_strand = models.CharField(max_length=100, choices=READ_STRAND)

    # optional
    rna_purity_260_280_ratio = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    rna_purity_260_230_ratio = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    rna_integrity_number = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class WholeGenomeSequencingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    library_generation_pcr_product_isolation_protocol = models.CharField(max_length=100)
    library_generation_protocol = models.CharField(max_length=100)

    # optional
    library_selection = models.CharField(max_length=100, choices=WGC_LIBRARY_SELCTION)


class GenotypingInfo(models.Model):
    # mandatory
    sample = models.OneToOneField(ExperimentInfo, on_delete=models.CASCADE)
    genotyping_protocol = models.CharField(max_length=100)

