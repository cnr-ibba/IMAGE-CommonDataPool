
# it seems that SimpleListFilter isn't provided by django.contrib.gis.admin
from django.contrib.admin import SimpleListFilter
from django.contrib.gis import admin

from .models import (
    Organism, Specimen, Species2CommonName, DADISLink)


# Adapted from
# https://bradmontgomery.net/blog/django-admin-filters-arrayfields/
# get all values from array fields and then use them with django admin filters
class PersonEmailListFilter(SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """

    title = 'Email'
    parameter_name = 'person_email'

    def lookups(self, request, model_admin):
        # query and sort all email belonging to model (access to it through
        # model property)
        person_email = model_admin.model.objects.values_list(
            "person_email", flat=True)

        # Flatten the nested list of results, and eliminate any empty lists
        person_email = [
            (kw, kw) for sublist in person_email for kw in sublist if kw]

        # Get rid of duplicates and sort them (in alphabetical order)
        person_email = sorted(set(person_email))

        return person_email

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of models, so we need to
        # filter that based on the clicked person_email.
        lookup_value = self.value()

        # The clicked person_email. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(person_email__contains=[lookup_value])
        return queryset


class OrganismAdmin(admin.OSMGeoAdmin):
    list_display = (
        'data_source_id', 'gene_bank_country', 'species', 'person_email',
        'supplied_breed')
    # Using custom filter in order to filter using ArrayField
    list_filter = [PersonEmailListFilter, 'species', 'gene_bank_country']
    search_fields = ['data_source_id', 'supplied_breed']
    list_per_page = 25


class SpecimenAdmin(admin.OSMGeoAdmin):
    list_display = (
        'data_source_id', 'gene_bank_country', 'species', 'person_email',
        'organism_part', 'derived_from')
    # Using custom filter in order to filter using ArrayField
    list_filter = [PersonEmailListFilter, 'species', 'gene_bank_country']
    search_fields = ['data_source_id', 'derived_from']
    list_per_page = 25


class Species2CommonNameAdmin(admin.ModelAdmin):
    list_display = ('scientific_name', 'common_name')
    list_per_page = 25


class DADISLinkAdmin(admin.ModelAdmin):
    list_display = (
        'species', 'supplied_breed', 'efabis_breed_country', 'dadis_url'
    )
    list_per_page = 25


admin.site.register(Organism, OrganismAdmin)
admin.site.register(Specimen, SpecimenAdmin)
admin.site.register(Species2CommonName, Species2CommonNameAdmin)
admin.site.register(DADISLink, DADISLinkAdmin)
