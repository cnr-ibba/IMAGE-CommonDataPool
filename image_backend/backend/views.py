from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer


class ListSpecimensView(generics.ListAPIView):
    serializer_class = SpecimensSerializer

    def get_queryset(self):
        return SampleInfo.objects.filter(specimens__isnull=False)


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
                    "message": "Organism with id: {} does not exist".format(kw['specimen_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListOrganismsView(generics.ListAPIView):
    serializer_class = OrganismsSerializer

    def get_queryset(self):
        return SampleInfo.objects.filter(organisms__isnull=False)


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
                    "message": "Organism with id: {} does not exist".format(kw['organism_id'])
                },
                status=status.HTTP_404_NOT_FOUND
            )
