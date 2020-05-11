
import math

from django.http import HttpResponse
from django.http.response import Http404
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
    SampleInfo, AnimalInfo, SampleDataInfo, Files, Species2CommonName,
    DADISLink)
from .serializers import (
    SpecimensSerializer, OrganismsSerializer, OrganismsSerializerShort,
    SpecimensSerializerShort, FilesSerializer, Species2CommonNameSerializer,
    DADISLinkSerializer)


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
        'dadis_link': 'dadis_link'
    }

    # info for debug toolbar
    print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])

    # combine data in order to have a correct response
    return Response(construct_reponse(data))


@api_view(['GET'])
def get_organisms_summary(request, format=None):
    # get filters from get request
    species_filter = request.GET.get('species', False)
    breed_filter = request.GET.get('organisms__supplied_breed', False)
    sex_filter = request.GET.get('organisms__sex', False)
    country_filter = request.GET.get('organisms__efabis_breed_country', False)

    results = SampleInfo.objects.prefetch_related(
        'organisms').filter(organisms__isnull=False)

    # update queryset with filter submitted by GET
    if species_filter:
        results = results.filter(species=species_filter)

    if breed_filter:
        results = results.filter(organisms__supplied_breed=breed_filter)

    if sex_filter:
        results = results.filter(organisms__sex=sex_filter)

    if country_filter:
        results = results.filter(
            organisms__efabis_breed_country=country_filter)

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
    breeds_count = count_items('organisms__supplied_breed')
    sex_count = count_items('organisms__sex')
    country_count = count_items('organisms__efabis_breed_country')

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
    results = AnimalInfo.objects.select_related("sample")

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
            'sample__species',
            'supplied_breed').annotate(
                total=Count('sample__species')).order_by('-total')

        count = dict()

        # read count items
        for item in qs:
            species = item['sample__species']
            breed = item['supplied_breed']
            total = item['total']

            if species not in count:
                count.setdefault(species, dict())

            count[species][breed] = total

        return count

    country_count = count_items('efabis_breed_country')
    species_count = count_items('sample__species')
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
    results = SampleInfo.objects.filter(organisms__isnull=False)
    organisms = results.exclude(organisms__birth_location_longitude='',
                                organisms__birth_location_latitude='')
    for record in organisms:
        organism = record.organisms.get()
        organism_latitude = convert_to_radians(
            organism.birth_location_latitude)
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
    return Response(filter_results)


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


@api_view(['GET'])
def get_specimens_summary(request, format=None):
    # get filters from get request
    species_filter = request.GET.get('species', False)
    organism_part_filter = request.GET.get('specimens__organism_part', False)

    results = SampleInfo.objects.prefetch_related(
        'specimens').filter(specimens__isnull=False)

    # update queryset with filter submitted by GET
    if species_filter:
        results = results.filter(species=species_filter)

    if organism_part_filter:
        results = results.filter(specimens__organism_part=organism_part_filter)

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
    organism_count = count_items('specimens__organism_part')

    return Response({
        'species': species_count,
        'organism_part': organism_count
    })


@api_view(['GET'])
def get_specimens_graphical_summary(request, format=None):
    """Return statistics for IMAGE-Portal summary page"""

    # start queryset
    results = SampleDataInfo.objects.select_related("sample")

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
    return Response(filter_results)


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


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class ListSpecimensView(generics.ListCreateAPIView):
    serializer_class = SpecimensSerializer
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
    ordering_fields = ['data_source_id']

    def get_queryset(self):
        return SampleInfo.objects.prefetch_related(
            'specimens').filter(specimens__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = SpecimensSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListSpecimensViewShort(generics.ListCreateAPIView):
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
        return SampleInfo.objects.prefetch_related(
            'specimens').filter(specimens__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = SpecimensSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SpecimensDetailsView(generics.RetrieveDestroyAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = SpecimensSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['data_source_id'])
            return Response(SpecimensSerializer(
                organism, context={'request': request}).data)

        except SampleInfo.DoesNotExist:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kw['data_source_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *a, **kw):
        try:
            organism = self.queryset.get(data_source_id=kw['data_source_id'])
            organism.delete()
            return Response(
                data={
                    "message": "Specimen with id: {} was deleted".format(
                        kw['data_source_id'])
                },
                status=status.HTTP_202_ACCEPTED
            )
        except SampleInfo.DoesNotExist:
            return Response(
                data={
                    "message": "Specimen with id: {} does not exist".format(
                        kw['data_source_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListOrganismsView(generics.ListCreateAPIView):
    serializer_class = OrganismsSerializer
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'species', 'organisms__supplied_breed',
        'organisms__efabis_breed_country', 'organisms__sex']
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
    ordering_fields = ['data_source_id']

    def get_queryset(self):
        return SampleInfo.objects.prefetch_related(
            'organisms',
            "organisms__dadis",
            "organisms__dadis__species").filter(
                organisms__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = OrganismsSerializer(
            data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ListOrganismsViewShort(generics.ListCreateAPIView):
    serializer_class = OrganismsSerializerShort
    pagination_class = SmallResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = [
        'species', 'organisms__supplied_breed',
        'organisms__efabis_breed_country', 'organisms__sex']
    search_fields = ['species', 'organisms__supplied_breed', 'organisms__sex']
    ordering_fields = ['data_source_id', 'species',
                       'organisms__supplied_breed', 'organisms__sex']

    def get_queryset(self):
        return SampleInfo.objects.prefetch_related(
            'organisms').filter(organisms__isnull=False)

    def post(self, request, *args, **kwargs):
        serializer = OrganismsSerializerShort(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class OrganismsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SampleInfo.objects.all()
    lookup_field = "data_source_id"
    serializer_class = OrganismsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # TODO: simplify this and text IMAGE-Portal
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

        except Http404:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kwargs[self.lookup_field])
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

        except Http404:
            return Response(
                data={
                    "message": "Organism with id: {} does not exist".format(
                        kwargs[self.lookup_field])
                },
                status=status.HTTP_404_NOT_FOUND
            )

        self.perform_destroy(instance)

        # Set a custom message
        data = {
            "message": "Organism with id: {} was deleted".format(
                kwargs[self.lookup_field])
        }

        return Response(data=data,  status=status.HTTP_202_ACCEPTED)


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
