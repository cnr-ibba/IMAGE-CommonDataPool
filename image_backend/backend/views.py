from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer, \
    OrganismsSerializerShort, SpecimensSerializerShort


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
