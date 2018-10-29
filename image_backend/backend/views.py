from rest_framework import generics

from .models import SampleInfo
from .serializers import SpecimensSerializer, OrganismsSerializer


class ListSpecimensView(generics.ListAPIView):
    serializer_class = SpecimensSerializer

    def get_queryset(self):
        return SampleInfo.objects.filter(specimens__isnull=False)


class ListOrganismsView(generics.ListAPIView):
    serializer_class = OrganismsSerializer

    def get_queryset(self):
        return SampleInfo.objects.filter(organisms__isnull=False)
