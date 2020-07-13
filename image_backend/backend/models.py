from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.http import urlquote

from django_db_views.db_view import DBView


class BioSampleAbstract(models.Model):
    # mandatory
    data_source_id = models.CharField(max_length=1000, primary_key=True)
    alternative_id = models.CharField(max_length=1000)
    project = models.CharField(max_length=1000)
    submission_title = models.TextField()
    material = models.CharField(max_length=1000)
    material_ontology = models.CharField(max_length=1000)
    person_last_name = ArrayField(models.CharField(max_length=1000))
    person_email = ArrayField(models.CharField(max_length=1000))
    person_affiliation = ArrayField(models.CharField(max_length=1000))
    person_role = ArrayField(models.CharField(max_length=1000))
    person_role_ontology = ArrayField(models.CharField(max_length=1000))
    organization_name = ArrayField(models.CharField(max_length=1000))
    organization_role = ArrayField(models.CharField(max_length=1000))
    organization_role_ontology = ArrayField(models.CharField(max_length=1000))
    gene_bank_name = models.CharField(max_length=1000)
    gene_bank_country = models.CharField(max_length=1000)
    gene_bank_country_ontology = models.CharField(max_length=1000)
    data_source_type = models.CharField(max_length=1000)
    data_source_version = models.CharField(max_length=1000)

    species = models.CharField(
        max_length=1000,
        db_index=True)

    species_ontology = models.CharField(max_length=1000)
    etag = models.CharField(max_length=1000)

    # recommended
    submission_description = models.TextField(blank=True)
    person_first_name = ArrayField(models.CharField(max_length=1000,
                                                    blank=True), blank=True)
    organization_address = ArrayField(models.TextField(blank=True), blank=True)
    organization_country = ArrayField(models.CharField(max_length=1000,
                                                       blank=True), blank=True)
    organization_country_ontology = ArrayField(
        models.CharField(max_length=1000, blank=True), blank=True)

    # optional
    description = models.TextField(blank=True)
    person_initial = ArrayField(models.CharField(max_length=1000, blank=True),
                                blank=True)
    organization_uri = ArrayField(models.TextField(blank=True), blank=True)
    publication_doi = models.CharField(max_length=1000, blank=True)

    class Meta:
        abstract = True


class Files(models.Model):
    # Specimen BioSample id
    # HINT: should be a foreign key to Specimen?
    data_source_id = models.CharField(max_length=1000, primary_key=True)

    file_name = ArrayField(models.CharField(max_length=1000))
    file_url = ArrayField(models.CharField(max_length=1000))
    file_size = ArrayField(models.CharField(max_length=1000))
    file_checksum = ArrayField(models.CharField(max_length=1000))
    file_checksum_method = ArrayField(models.CharField(max_length=1000))

    class Meta:
        ordering = ['-data_source_id']


class Specimen(BioSampleAbstract):
    # mandatory
    derived_from = models.CharField(max_length=1000)
    collection_place_accuracy = models.CharField(max_length=1000)
    organism_part = models.CharField(max_length=1000)
    organism_part_ontology = models.CharField(
        max_length=1000,
        db_index=True)

    # recommended
    specimen_collection_protocol = models.CharField(
        max_length=1000, blank=True)
    collection_date = models.CharField(max_length=1000, blank=True)
    collection_date_unit = models.CharField(max_length=1000, blank=True)
    collection_place_latitude = models.CharField(max_length=1000, blank=True)
    collection_place_latitude_unit = models.CharField(max_length=1000,
                                                      blank=True)
    collection_place_longitude = models.CharField(max_length=1000, blank=True)
    collection_place_longitude_unit = models.CharField(max_length=1000,
                                                       blank=True)
    collection_place = models.CharField(max_length=1000, blank=True)
    developmental_stage = models.CharField(max_length=1000, blank=True)
    developmental_stage_ontology = models.CharField(
        max_length=1000, blank=True)
    physiological_stage = models.CharField(max_length=1000, blank=True)
    physiological_stage_ontology = models.CharField(
        max_length=1000, blank=True)
    availability = models.CharField(max_length=1000, blank=True)
    sample_storage = models.CharField(max_length=1000, blank=True)
    sample_storage_processing = models.CharField(max_length=1000, blank=True)

    # optional
    animal_age_at_collection = models.CharField(max_length=1000, blank=True)
    animal_age_at_collection_unit = models.CharField(max_length=1000,
                                                     blank=True)
    sampling_to_preparation_interval = models.CharField(max_length=1000,
                                                        blank=True)
    sampling_to_preparation_interval_unit = models.CharField(max_length=1000,
                                                             blank=True)

    class Meta:
        ordering = ['-data_source_id']
        indexes = [
            models.Index(fields=[
                'collection_place_latitude', 'collection_place_longitude']),
        ]


class Species2CommonName(models.Model):
    # in theory the scientific name is unique. However, what if a species
    # has more than one common name?
    scientific_name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Species to common name"
        ordering = ['-id']

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"


class DADISLink(models.Model):
    species = models.ForeignKey(
        Species2CommonName,
        on_delete=models.CASCADE)
    supplied_breed = models.CharField(max_length=255)
    efabis_breed_country = models.CharField(max_length=255)
    dadis_url = models.URLField(
        max_length=255,
        null=True,
        blank=True)

    class Meta:
        unique_together = (
            "species", "supplied_breed", "efabis_breed_country")
        ordering = ['-id']

    @classmethod
    def get_instance_from_dict(cls, adict):
        qs = cls.objects.filter(
            species__scientific_name=adict['species']['scientific_name'],
            species__common_name=adict['species']['common_name'],
            supplied_breed=adict['supplied_breed'],
            efabis_breed_country=adict['efabis_breed_country'],
            )

        # should be one or None
        return qs.first()

    def __str__(self):
        return "%s,%s,%s" % (
            self.species.common_name,
            self.supplied_breed,
            self.efabis_breed_country)

    def save(self, *args, **kwargs):
        if self.dadis_url is None or self.dadis_url == '':
            self.dadis_url = (
                "https://dadis-breed-4eff5.firebaseapp.com/?country="
                "{country}&specie={specie}&breed={breed}"
                "&callback=allbreeds"
            ).format(
                country=self.efabis_breed_country,
                specie=urlquote(self.species.common_name),
                breed=urlquote(self.supplied_breed)
            )

        # call the base method
        super().save(*args, **kwargs)


class Organism(BioSampleAbstract):
    # mandatory
    supplied_breed = models.CharField(max_length=1000)
    efabis_breed_country = models.CharField(max_length=1000)
    sex = models.CharField(max_length=1000)
    sex_ontology = models.CharField(max_length=1000)
    birth_location_accuracy = models.CharField(max_length=1000)

    # recommended
    mapped_breed = models.CharField(max_length=1000, blank=True)
    mapped_breed_ontology = models.CharField(max_length=1000, blank=True)
    birth_date = models.CharField(max_length=1000, blank=True)
    birth_date_unit = models.CharField(max_length=1000, blank=True)
    birth_location = models.CharField(max_length=1000, blank=True)
    birth_location_longitude = models.CharField(max_length=1000, blank=True)
    birth_location_longitude_unit = models.CharField(max_length=1000,
                                                     blank=True)
    birth_location_latitude = models.CharField(max_length=1000, blank=True)
    birth_location_latitude_unit = models.CharField(max_length=1000,
                                                    blank=True)

    # optional
    child_of = ArrayField(models.CharField(max_length=1000, blank=True),
                          size=2, blank=True)
    specimens = ArrayField(models.CharField(max_length=1000, blank=True),
                           blank=True, default=list)

    # custom
    dadis = models.ForeignKey(
        DADISLink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organisms")

    class Meta:
        ordering = ['-data_source_id']
        indexes = [
            models.Index(fields=['supplied_breed', 'efabis_breed_country']),
            models.Index(fields=['efabis_breed_country']),
            models.Index(fields=[
                'birth_location_latitude', 'birth_location_longitude']),
        ]


# using database views for etag models
# https://github.com/BezBartek/django-db-views/blob/master/README.md
class Etag(DBView):
    data_source_id = models.CharField(max_length=1000)
    etag = models.CharField(max_length=1000)

    # Django requires column called id
    view_definition = """
        SELECT row_number() over () AS id,
               t1.* FROM (
                   SELECT data_source_id,
                          etag
                     FROM backend_organism UNION
                   SELECT data_source_id,
                          etag
                     FROM backend_specimen) AS t1
    """

    class Meta:
        managed = False
        db_table = 'backend_etag'
