from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer


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
