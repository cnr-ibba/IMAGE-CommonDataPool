
from django.contrib.gis import admin

from .models import (
    Organism, Specimen, Species2CommonName, DADISLink)


class OrganismAdmin(admin.OSMGeoAdmin):
    list_display = (
        'data_source_id', 'gene_bank_country', 'species', 'person_email',
        'supplied_breed')
    list_filter = ['person_email', 'species', 'gene_bank_country']
    search_fields = ['data_source_id', 'supplied_breed']


class SpecimenAdmin(admin.OSMGeoAdmin):
    list_display = (
        'data_source_id', 'gene_bank_country', 'species', 'person_email',
        'organism_part', 'derived_from')
    list_filter = ['person_email', 'species', 'gene_bank_country']
    search_fields = ['data_source_id', 'derived_from']


class Species2CommonNameAdmin(admin.ModelAdmin):
    list_display = ('scientific_name', 'common_name')


class DADISLinkAdmin(admin.ModelAdmin):
    list_display = (
        'species', 'supplied_breed', 'efabis_breed_country', 'dadis_url'
    )


admin.site.register(Organism, OrganismAdmin)
admin.site.register(Specimen, SpecimenAdmin)
admin.site.register(Species2CommonName, Species2CommonNameAdmin)
admin.site.register(DADISLink, DADISLinkAdmin)
