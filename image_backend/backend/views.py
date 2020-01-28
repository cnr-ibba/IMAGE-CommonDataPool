from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.pagination import PageNumberPagination

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer, \
    OrganismsSerializerShort, SpecimensSerializerShort


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class ListCreateSpecimensView(generics.ListCreateAPIView):
    serializer_class = SpecimensSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
