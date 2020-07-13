
import math

from django.http import HttpResponse
from django.db.models import Count

from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Specimen, Organism, Files, Species2CommonName, DADISLink, Etag)
from .serializers import (
    SpecimenSerializer, OrganismSerializer, OrganismSerializerShort,
    SpecimenSerializerShort, FilesSerializer, Species2CommonNameSerializer,
    DADISLinkSerializer, EtagSerializer)


@api_view(['GET'])
def backend_root(request, format=None):

    def construct_reponse(params):
        """
        Define a dictionary of response from a dictionary of parameters,
        where keys are locations and values are names (as defined in
        backend.urls)
        """

        result = dict()
        base_url = "/data_portal/backend/"
        app_name = "backend"

        for path, name in params.items():
            result[base_url+path] = reverse(
                ":".join([app_name, name]),
                request=request,
                format=format)

        return result

    # this is my parameters dictionary. The detail pages are not displayed
    data = {
        "organism/": "organismindex",
        "organism_short/": "organismindex_short",
        "organism/summary/": "organism_summary",
        "organism/graphical_summary/": "organism_graphical_summary",
        "organism/gis_search/": "organism_gis_search",
        "organism/download/": "organism_download",
        'specimen/': 'specimenindex',
        'specimen_short/': 'specimenindex_short',
        'specimen/summary/': 'specimen_summary',
        'specimen/graphical_summary/': 'specimens_graphical_summary',
        'specimen/gis_search/': 'specimen_gis_search',
        'specimen/download/': 'specimen_download',
        'file/': 'fileindex',
        'file/download/': 'file_download',
        'species/': 'species',
        'dadis_link/': 'dadis_link',
        'etag/': 'etag-list',
    }

    # info for debug toolbar
    print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])

    # combine data in order to have a correct response
    return Response(construct_reponse(data))


@api_view(['GET'])
def get_organisms_summary(request, format=None):
    # get filters from get request
    species_filter = request.GET.get('species', False)
    breed_filter = request.GET.get('supplied_breed', False)
    sex_filter = request.GET.get('sex', False)
    country_filter = request.GET.get('efabis_breed_country', False)

    # gett all my organisms (amimal) in a queryset
    results = Organism.objects.all()

    # update queryset with filter submitted by GET
    if species_filter:
        results = results.filter(species=species_filter)

    if breed_filter:
        results = results.filter(supplied_breed=breed_filter)

    if sex_filter:
        results = results.filter(sex=sex_filter)

    if country_filter:
        results = results.filter(
            efabis_breed_country=country_filter)

    def count_items(field, results=results):
        qs = results.values(field).annotate(
            total=Count(field)).order_by('total')

        count = dict()

        # update species result
        for item in qs:
            key = item[field]
            total = item['total']
            count[key] = total

        return count

    # count my items
    species_count = count_items('species')
    breeds_count = count_items('supplied_breed')
    sex_count = count_items('sex')
    country_count = count_items('efabis_breed_country')

    return Response({
        'species': species_count,
        'breed': breeds_count,
        'sex': sex_count,
        'country': country_count
    })


@api_view(['GET'])
def get_organisms_graphical_summary(request, format=None):
    """Return statistics for IMAGE-Portal summary page"""

    # start queryset
    results = Organism.objects.all()

    def count_items(field, results=results):
        qs = results.values(field).annotate(
            total=Count(field)).order_by('total')

        count = dict()

        # update species result
        for item in qs:
            key = item[field]
            total = item['total']
            count[key] = total

        return count

    def count_breeds(results=results):
        qs = results.values(
            'species',
            'supplied_breed').annotate(
                total=Count('species')).order_by('-total')

        count = dict()

        # read count items
        for item in qs:
            species = item['species']
            breed = item['supplied_breed']
            total = item['total']

            if species not in count:
                count.setdefault(species, dict())

            count[species][breed] = total

        return count

    country_count = count_items('efabis_breed_country')
    species_count = count_items('species')
    breeds_count = count_breeds()

    coordinates = list()

    organisms = results.exclude(
        birth_location_longitude='',
        birth_location_latitude='')

    for organism in organisms:
        coordinates.append(
            (organism.birth_location_longitude,
             organism.birth_location_latitude)
        )

    return Response({
        'species': species_count,
        'breeds': breeds_count,
        'countries': country_count,
        'coordinates': coordinates
    })


def convert_to_radians(degrees):
    return float(degrees) * 3.14 / 180


@api_view(['GET'])
def organisms_gis_search(request, format=None):
    filter_results = dict()
    filter_results['results'] = list()
    latitude = convert_to_radians(request.GET.get('latitude', False))
    longitude = convert_to_radians(request.GET.get('longitude', False))
    radius = float(request.GET.get('radius', False))
    results = Organism.objects.all()
    organisms = results.exclude(birth_location_longitude='',
                                birth_location_latitude='')
    for organism in organisms:
        organism_latitude = convert_to_radians(
            organism.birth_location_latitude)
        organism_longitude = convert_to_radians(
            organism.birth_location_longitude)
        if math.acos(math.sin(latitude) * math.sin(organism_latitude) +
                     math.cos(latitude) * math.cos(organism_latitude) *
                     math.cos(organism_longitude - longitude)) * 6371 < radius:
            organism_results = {
                'data_source_id': organism.data_source_id,
                'species': organism.species,
                'supplied_breed': organism.supplied_breed,
                'sex': organism.sex
            }
            filter_results['results'].append(organism_results)
    return Response(filter_results)


def download_organism_data(request):
    data_to_download = 'Data source ID\tSpecies\tSupplied breed\tSex\n'
    species_filter = request.GET.get('species', False)
    breed_filter = request.GET.get('supplied_breed', False)
    sex_filter = request.GET.get('sex', False)
    results = Organism.objects.all()
    if species_filter:
        results = results.filter(species=species_filter)
    if breed_filter:
        results = results.filter(supplied_breed=breed_filter)
    if sex_filter:
        results = results.filter(sex=sex_filter)
    for record in results:
        data_to_download += f'{record.data_source_id}\t{record.species}\t' \
                            f'{record.supplied_breed}\t{record.sex}\n'
    response = HttpResponse(data_to_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="IMAGE_organisms' \
                                      '.txt"'
    return response


@api_view(['GET'])
def get_specimens_summary(request, format=None):
    # get filters from get request
    species_filter = request.GET.get('species', False)
    organism_part_filter = request.GET.get('organism_part', False)

    results = Specimen.objects.all()

    # update queryset with filter submitted by GET
    if species_filter:
        results = results.filter(species=species_filter)

    if organism_part_filter:
        results = results.filter(organism_part=organism_part_filter)

    def count_items(field, results=results):
        qs = results.values(field).annotate(
            total=Count(field)).order_by('total')

        count = dict()

        # update species result
        for item in qs:
            key = item[field]
            total = item['total']
            count[key] = total

        return count

    species_count = count_items('species')
    organism_count = count_items('organism_part')

    return Response({
        'species': species_count,
        'organism_part': organism_count
    })


@api_view(['GET'])
def get_specimens_graphical_summary(request, format=None):
    """Return statistics for IMAGE-Portal summary page"""

    # start queryset
    results = Specimen.objects.all()

    def count_items(field, results=results):
        qs = results.values(field).annotate(
            total=Count(field)).order_by('total')

        count = dict()

        # update species result
        for item in qs:
            key = item[field]
            total = item['total']
            count[key] = total

        return count

    organism_count = count_items('organism_part')

    coordinates = list()

    specimens = results.exclude(
        collection_place_latitude='',
        collection_place_longitude='')

    for specimen in specimens:
        coordinates.append(
            (specimen.collection_place_longitude,
             specimen.collection_place_latitude)
        )

    return Response({
        'organism_part': organism_count,
        'coordinates': coordinates
    })


@api_view(['GET'])
def specimens_gis_search(request, format=None):
    filter_results = dict()
    filter_results['results'] = list()
    latitude = convert_to_radians(request.GET.get('latitude', False))
    longitude = convert_to_radians(request.GET.get('longitude', False))
    radius = int(request.GET.get('radius', False))
    results = Specimen.objects.all()
    specimens = results.exclude(collection_place_latitude='',
                                collection_place_longitude='')
    for specimen in specimens:
        specimen_latitude = convert_to_radians(
            specimen.collection_place_latitude)
        specimen_longitude = convert_to_radians(
            specimen.collection_place_longitude)
        if math.acos(math.sin(latitude) * math.sin(specimen_latitude) +
                     math.cos(latitude) * math.cos(specimen_latitude) *
                     math.cos(specimen_longitude - longitude)) * 6371 < radius:
            specimen_results = {
                'data_source_id': specimen.data_source_id,
                'species': specimen.species,
                'derived_from': specimen.derived_from,
                'organism_part': specimen.organism_part
            }
            filter_results['results'].append(specimen_results)
    return Response(filter_results)


def download_specimen_data(request):
    data_to_download = 'Data source ID\tSpecies\tDerived from\tOrganism part\n'
    species_filter = request.GET.get('species', False)
    organism_part_filter = request.GET.get('organism_part', False)
    results = Specimen.objects.all()
    if species_filter:
        results = results.filter(species=species_filter)
    if organism_part_filter:
        results = results.filter(organism_part=organism_part_filter)
    for record in results:
        data_to_download += f'{record.data_source_id}\t{record.species}\t' \
                            f'{record.derived_from}\t' \
                            f'{record.organism_part}\n'
    response = HttpResponse(data_to_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="IMAGE_specimens' \
                                      '.txt"'
    return response


# https://www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles
# https://stackoverflow.com/a/40985524
class CustomPaginationMixin():
    """Custom Mixin to add the numer of pages in a response"""

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class SmallResultsSetPagination(CustomPaginationMixin, PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class LargeResultsSetPagination(CustomPaginationMixin, PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class ListSpecimensView(generics.ListCreateAPIView):
    serializer_class = SpecimenSerializer
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['data_source_id', 'alternative_id', 'project',
                     'submission_title', 'material', 'material_ontology',
                     'person_last_name', 'person_email', 'person_affiliation',
                     'person_role', 'person_role_ontology',
                     'organization_name',
                     'organization_role', 'organization_role_ontology',
                     'gene_bank_name', 'gene_bank_country',
                     'gene_bank_country_ontology', 'data_source_type',
                     'data_source_version', 'species', 'species_ontology',
                     'etag', 'submission_description', 'person_first_name',
                     'organization_address', 'organization_country',
                     'organization_country_ontology', 'description',
                     'person_initial', 'organization_uri', 'publication_doi',
                     'derived_from',
                     'collection_place_accuracy',
                     'organism_part',
                     'organism_part_ontology',
                     'specimen_collection_protocol',
                     'collection_date',
                     'collection_date_unit',
                     'collection_place_latitude',
                     'collection_place_latitude_unit',
                     'collection_place_longitude',
                     'collection_place_longitude_unit',
                     'collection_place',
                     'developmental_stage',
                     'developmental_stage_ontology',
                     'physiological_stage',
                     'physiological_stage_ontology',
                     'availability', 'sample_storage',
                     'sample_storage_processing',
                     'animal_age_at_collection',
                     'animal_age_at_collection_unit',
                     'sampling_to_preparation_interval',
                     'sampling_to_preparation_interval_unit']
    ordering_fields = ['data_source_id']

    def get_queryset(self):
        return Specimen.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = SpecimenSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListSpecimensViewShort(generics.ListCreateAPIView):
    serializer_class = SpecimenSerializerShort
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['species', 'organism_part']
    search_fields = ['species', 'organism_part']
    ordering_fields = ['data_source_id', 'species', 'derived_from',
                       'organism_part']

    def get_queryset(self):
        return Specimen.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = SpecimenSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SpecimensDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specimen.objects.all()
    lookup_field = "data_source_id"
    serializer_class = SpecimenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ListOrganismsView(generics.ListCreateAPIView):
    serializer_class = OrganismSerializer
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'species', 'supplied_breed',
        'efabis_breed_country', 'sex']
    search_fields = ['data_source_id', 'alternative_id', 'project',
                     'submission_title', 'material', 'material_ontology',
                     'person_last_name', 'person_email', 'person_affiliation',
                     'person_role', 'person_role_ontology',
                     'organization_name',
                     'organization_role', 'organization_role_ontology',
                     'gene_bank_name', 'gene_bank_country',
                     'gene_bank_country_ontology', 'data_source_type',
                     'data_source_version', 'species', 'species_ontology',
                     'etag', 'submission_description', 'person_first_name',
                     'organization_address', 'organization_country',
                     'organization_country_ontology', 'description',
                     'person_initial', 'organization_uri', 'publication_doi',
                     'supplied_breed',
                     'efabis_breed_country', 'sex',
                     'sex_ontology',
                     'birth_location_accuracy',
                     'mapped_breed',
                     'mapped_breed_ontology',
                     'birth_date', 'birth_date_unit',
                     'birth_location',
                     'birth_location_longitude',
                     'birth_location_longitude_unit',
                     'birth_location_latitude',
                     'birth_location_latitude_unit',
                     'child_of']
    ordering_fields = ['data_source_id']

    def get_queryset(self):
        return Organism.objects.select_related(
            "dadis",
            "dadis__species").all()

    def post(self, request, *args, **kwargs):
        serializer = OrganismSerializer(
            data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListOrganismsViewShort(generics.ListCreateAPIView):
    serializer_class = OrganismSerializerShort
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = [
        'species', 'supplied_breed',
        'efabis_breed_country', 'sex']
    search_fields = ['species', 'supplied_breed', 'sex']
    ordering_fields = ['data_source_id', 'species',
                       'supplied_breed', 'sex']

    def get_queryset(self):
        return Organism.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = OrganismSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class OrganismsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    # since we are searching with sampleinfo, I need to return only entries
    # with a relationship with Organism (organisms)
    queryset = Organism.objects.all()
    lookup_field = "data_source_id"
    serializer_class = OrganismSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ListCreateFilesView(generics.ListCreateAPIView):
    serializer_class = FilesSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_source_id', 'file_name']

    def get_queryset(self):
        return Files.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


def download_file_data(request):
    data_to_download = 'Data source ID\tFile name\tFile size\tFile index\t' \
                       'File index size\n'
    results = Files.objects.all()
    for record in results:
        data_to_download += f'{record.data_source_id}\t{record.file_name}\t' \
                            f'{record.file_size}\t{record.file_index_name}\t' \
                            f'{record.file_index_size}\n'
    response = HttpResponse(data_to_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="IMAGE_files.txt'
    return response


class FilesDetailsView(generics.RetrieveAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    def get(self, request, *a, **kw):
        try:
            file = self.queryset.get(data_source_id=kw['specimen_id'])
            return Response(FilesSerializer(file).data)
        except Files.DoesNotExist:
            return Response(
                data={
                    "message": "File with id: {} does not exist".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *a, **kw):
        try:
            file = self.queryset.get(data_source_id=kw['specimen_id'])
            file.delete()
            return Response(
                data={
                    "message": "File with id: {} was deleted".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Files.DoesNotExist:
            return Response(
                data={
                    "message": "File with id: {} does not exist".format(
                        kw['specimen_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SpeciesToCommonNameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Species2CommonName.objects.all()
    serializer_class = Species2CommonNameSerializer


class DADISLinkViewSet(viewsets.ModelViewSet):
    """
    Update DADIS table
    """

    queryset = DADISLink.objects.select_related('species').all()
    serializer_class = DADISLinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'species__common_name', 'species__scientific_name', 'supplied_breed',
        'efabis_breed_country']


class EtagViewSet(viewsets.ModelViewSet):
    """
    Get Info on Etags
    """

    lookup_field = "data_source_id"
    queryset = Etag.objects.all()
    serializer_class = EtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['data_source_id', 'etag']
    ordering_fields = ['data_source_id']
