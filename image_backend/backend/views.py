import json
import math

from django.http import JsonResponse, HttpResponse
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer, \
    OrganismsSerializerShort, SpecimensSerializerShort


def get_organisms_summary(request):
    species = dict()
    breed = dict()
    sex = dict()
    species_filter = request.GET.get('species', False)
    breed_filter = request.GET.get('organisms__supplied_breed', False)
    sex_filter = request.GET.get('organisms__sex', False)
    results = SampleInfo.objects.filter(organisms__isnull=False)
    if species_filter:
        results = results.filter(species=species_filter)
    if breed_filter:
        results = results.filter(organisms__supplied_breed=breed_filter)
    if sex_filter:
        results = results.filter(organisms__sex=sex_filter)
    species_names = results.order_by().values_list(
        'species', flat=True).distinct()
    breed_names = results.order_by().values_list('organisms__supplied_breed',
                                                 flat=True).distinct()
    sex_names = results.order_by().values_list('organisms__sex',
                                               flat=True).distinct()
    for name in species_names:
        species[name] = results.filter(species=name).count()
    for name in breed_names:
        breed[name] = results.filter(organisms__supplied_breed=name).count()
    for name in sex_names:
        sex[name] = results.filter(organisms__sex=name).count()
    return JsonResponse(
        {
            'species': species,
            'breed': breed,
            'sex': sex
        }
    )


def get_organisms_graphical_summary(request):
    breeds = dict()
    species = dict()
    countries = dict()
    coordinates = list()
    results = SampleInfo.objects.filter(organisms__isnull=False)
    species_names = results.order_by().values_list('species',
                                                   flat=True).distinct()
    country_names = results.order_by().values_list(
        'organisms__efabis_breed_country', flat=True).distinct()
    organisms = results.exclude(organisms__birth_location_longitude='',
                                organisms__birth_location_latitude='')
    for name in species_names:
        species[name] = results.filter(species=name).count()
        breeds.setdefault(name, dict())
        tmp = results.filter(species=name)
        breeds_names = tmp.order_by().values_list('organisms__supplied_breed',
                                                  flat=True).distinct()
        for breed_name in breeds_names:
            breeds[name][breed_name] = tmp.filter(
                organisms__supplied_breed=breed_name).count()
    for name in country_names:
        countries[name] = results.filter(
            organisms__efabis_breed_country=name).count()
    for record in organisms:
        organism = record.organisms.get()
        coordinates.append((organism.birth_location_longitude,
                            organism.birth_location_latitude))
    return JsonResponse(

        {
            'species': species,
            'breeds': breeds,
            'countries': countries,
            'coordinates': coordinates
        }
    )


def convert_to_radians(degrees):
    return float(degrees) * 3.14 / 180


def organisms_gis_search(request):
    filter_results = dict()
    filter_results['results'] = list()
    latitude = convert_to_radians(request.GET.get('latitude', False))
    longitude = convert_to_radians(request.GET.get('longitude', False))
    radius = float(request.GET.get('radius', False))
    results = SampleInfo.objects.filter(organisms__isnull=False)
    organisms = results.exclude(organisms__birth_location_longitude='',
                                organisms__birth_location_latitude='')
    for record in organisms:
        organism = record.organisms.get()
        organism_latitude = convert_to_radians(organism.birth_location_latitude)
        organism_longitude = convert_to_radians(
            organism.birth_location_longitude)
        if math.acos(math.sin(latitude) * math.sin(organism_latitude) +
                     math.cos(latitude) * math.cos(organism_latitude) *
                     math.cos(organism_longitude - longitude)) * 6371 < radius:
            organism_results = {
                'data_source_id': record.data_source_id,
                'species': record.species,
                'supplied_breed': organism.supplied_breed,
                'sex': organism.sex
            }
            filter_results['results'].append(organism_results)
    return JsonResponse(filter_results)


def download_organism_data(request):
    data_to_download = 'Data source ID\tSpecies\tSupplied breed\tSex\n'
    species_filter = request.GET.get('species', False)
    breed_filter = request.GET.get('organisms__supplied_breed', False)
    sex_filter = request.GET.get('organisms__sex', False)
    results = SampleInfo.objects.filter(organisms__isnull=False)
    if species_filter:
        results = results.filter(species=species_filter)
    if breed_filter:
        results = results.filter(organisms__supplied_breed=breed_filter)
    if sex_filter:
        results = results.filter(organisms__sex=sex_filter)
    for record in results:
        organism = record.organisms.get()
        data_to_download += f'{record.data_source_id}\t{record.species}\t' \
                            f'{organism.supplied_breed}\t{organism.sex}\n'
    response = HttpResponse(data_to_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="IMAGE_organisms' \
                                      '.txt"'
    return response


def get_specimens_summary(request):
    species = dict()
    organism_part = dict()
    species_filter = request.GET.get('species', False)
    organism_part_filter = request.GET.get('specimens__organism_part', False)
    results = SampleInfo.objects.filter(specimens__isnull=False)
    if species_filter:
        results = results.filter(species=species_filter)
    if organism_part_filter:
        results = results.filter(specimens__organism_part=organism_part_filter)
    species_names = results.order_by().values_list('species',
                                                   flat=True).distinct()
    organism_part_names = results.order_by().values_list(
        'specimens__organism_part', flat=True).distinct()
    for name in species_names:
        species[name] = results.filter(species=name).count()
    for name in organism_part_names:
        organism_part[name] = results.filter(
            specimens__organism_part=name).count()
    return JsonResponse(
        {
            'species': species,
            'organism_part': organism_part
        }
    )


def get_specimens_graphical_summary(request):
    coordinates = list()
    organism_part = dict()
    results = SampleInfo.objects.filter(specimens__isnull=False)
    organism_part_names = results.order_by().values_list(
        'specimens__organism_part', flat=True).distinct()
    specimens = results.exclude(specimens__collection_place_latitude='',
                                specimens__collection_place_longitude='')
    for name in organism_part_names:
        organism_part[name] = results.filter(
            specimens__organism_part=name).count()
    for record in specimens:
        specimen = record.specimens.get()
        coordinates.append((specimen.collection_place_longitude,
                            specimen.collection_place_latitude))
    return JsonResponse(
        {
            'organism_part': organism_part,
            'coordinates': coordinates
        }
    )


def specimens_gis_search(request):
    filter_results = dict()
    filter_results['results'] = list()
    latitude = convert_to_radians(request.GET.get('latitude', False))
    longitude = convert_to_radians(request.GET.get('longitude', False))
    radius = int(request.GET.get('radius', False))
    results = SampleInfo.objects.filter(specimens__isnull=False)
    specimens = results.exclude(specimens__collection_place_latitude='',
                                specimens__collection_place_longitude='')
    for record in specimens:
        specimen = record.specimens.get()
        specimen_latitude = convert_to_radians(
            specimen.collection_place_latitude)
        specimen_longitude = convert_to_radians(
            specimen.collection_place_longitude)
        if math.acos(math.sin(latitude) * math.sin(specimen_latitude) +
                     math.cos(latitude) * math.cos(specimen_latitude) *
                     math.cos(specimen_longitude - longitude)) * 6371 < radius:
            specimen_results = {
                'data_source_id': record.data_source_id,
                'species': record.species,
                'derived_from': specimen.derived_from,
                'organism_part': specimen.organism_part
            }
            filter_results['results'].append(specimen_results)
    return JsonResponse(filter_results)


def download_specimen_data(request):
    data_to_download = 'Data source ID\tSpecies\tDerived from\tOrganism part\n'
    species_filter = request.GET.get('species', False)
    organism_part_filter = request.GET.get('specimens__organism_part', False)
    results = SampleInfo.objects.filter(specimens__isnull=False)
    if species_filter:
        results = results.filter(species=species_filter)
    if organism_part_filter:
        results = results.filter(specimens__organism_part=organism_part_filter)
    for record in results:
        specimen = record.specimens.get()
        data_to_download += f'{record.data_source_id}\t{record.species}\t' \
                            f'{specimen.derived_from}\t' \
                            f'{specimen.organism_part}\n'
    response = HttpResponse(data_to_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="IMAGE_specimens' \
                                      '.txt"'
    return response


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class ListCreateSpecimensView(generics.ListCreateAPIView):
    serializer_class = SpecimensSerializer
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['data_source_id', 'alternative_id', 'project',
                     'submission_title', 'material', 'material_ontology',
                     'person_last_name', 'person_email', 'person_affiliation',
                     'person_role', 'person_role_ontology', 'organization_name',
                     'organization_role', 'organization_role_ontology',
                     'gene_bank_name', 'gene_bank_country',
                     'gene_bank_country_ontology', 'data_source_type',
                     'data_source_version', 'species', 'species_ontology',
                     'etag', 'submission_description', 'person_first_name',
                     'organization_address', 'organization_country',
                     'organization_country_ontology', 'description',
                     'person_initial', 'organization_uri', 'publication_doi',
                     'specimens__derived_from',
                     'specimens__collection_place_accuracy',
                     'specimens__organism_part',
                     'specimens__organism_part_ontology',
                     'specimens__specimen_collection_protocol',
                     'specimens__collection_date',
                     'specimens__collection_date_unit',
                     'specimens__collection_place_latitude',
                     'specimens__collection_place_latitude_unit',
                     'specimens__collection_place_longitude',
                     'specimens__collection_place_longitude_unit',
                     'specimens__collection_place',
                     'specimens__developmental_stage',
                     'specimens__developmental_stage_ontology',
                     'specimens__physiological_stage',
                     'specimens__physiological_stage_ontology',
                     'specimens__availability', 'specimens__sample_storage',
                     'specimens__sample_storage_processing',
                     'specimens__animal_age_at_collection',
                     'specimens__animal_age_at_collection_unit',
                     'specimens__sampling_to_preparation_interval',
                     'specimens__sampling_to_preparation_interval_unit']

    def get_queryset(self):
        return SampleInfo.objects.filter(specimens__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = SpecimensSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListCreateSpecimensViewShort(generics.ListCreateAPIView):
    serializer_class = SpecimensSerializerShort
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['species', 'specimens__organism_part']
    search_fields = ['species', 'specimens__organism_part']
    ordering_fields = ['data_source_id', 'species', 'specimens__derived_from',
                       'specimens__organism_part']

    def get_queryset(self):
        return SampleInfo.objects.filter(specimens__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = SpecimensSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SpecimensDetailsView(generics.RetrieveAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = SpecimensSerializer

    def get(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['specimen_id'])
            return Response(SpecimensSerializer(organism).data)
        except:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['specimen_id'])
            organism.delete()
            return Response(
                data={
                    "message": "Specimen with id: {} was deleted".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_202_ACCEPTED
            )
        except:
            return Response(
                data={
                    "message": "Specimen with id: {} does not exist".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListCreateOrganismsView(generics.ListCreateAPIView):
    serializer_class = OrganismsSerializer
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['data_source_id', 'alternative_id', 'project',
                     'submission_title', 'material', 'material_ontology',
                     'person_last_name', 'person_email', 'person_affiliation',
                     'person_role', 'person_role_ontology', 'organization_name',
                     'organization_role', 'organization_role_ontology',
                     'gene_bank_name', 'gene_bank_country',
                     'gene_bank_country_ontology', 'data_source_type',
                     'data_source_version', 'species', 'species_ontology',
                     'etag', 'submission_description', 'person_first_name',
                     'organization_address', 'organization_country',
                     'organization_country_ontology', 'description',
                     'person_initial', 'organization_uri', 'publication_doi',
                     'organisms__supplied_breed',
                     'organisms__efabis_breed_country', 'organisms__sex',
                     'organisms__sex_ontology',
                     'organisms__birth_location_accuracy',
                     'organisms__mapped_breed',
                     'organisms__mapped_breed_ontology',
                     'organisms__birth_date', 'organisms__birth_date_unit',
                     'organisms__birth_location',
                     'organisms__birth_location_longitude',
                     'organisms__birth_location_longitude_unit',
                     'organisms__birth_location_latitude',
                     'organisms__birth_location_latitude_unit',
                     'organisms__child_of']

    def get_queryset(self):
        return SampleInfo.objects.filter(organisms__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = OrganismsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListCreateOrganismsViewShort(generics.ListCreateAPIView):
    serializer_class = OrganismsSerializerShort
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['species', 'organisms__supplied_breed',
                        'organisms__sex']
    search_fields = ['species', 'organisms__supplied_breed', 'organisms__sex']
    ordering_fields = ['data_source_id', 'species', 'organisms__supplied_breed',
                       'organisms__sex']

    def get_queryset(self):
        return SampleInfo.objects.filter(organisms__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = OrganismsSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class OrganismsDetailsView(generics.RetrieveAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = OrganismsSerializer

    def get(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['organism_id'])
            return Response(OrganismsSerializer(organism).data)
        except:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kw['organism_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['organism_id'])
            organism.delete()
            return Response(
                data={
                    "message": "Organism with id: {} was deleted".format(
                        kw['organism_id'])
                },
                status=status.HTTP_202_ACCEPTED
            )
        except:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kw['organism_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )
