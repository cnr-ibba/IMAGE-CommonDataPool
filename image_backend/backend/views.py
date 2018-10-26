from rest_framework import generics

from .models import SampleInfo, AnimalInfo, SampleDataInfo
from .serializers import SampleInfoSerializer, AnimalInfoSerializer, SampleDataInfoSerializer


# class ListExperimentsView(generics.ListAPIView):
#     queryset = ExperimentInfo.objects.all()
#     serializer_class = ExperimentInfoSerializer

class ListSamplesView(generics.ListAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = SampleInfoSerializer


class ListAnimalsView(generics.ListAPIView):
    queryset = AnimalInfo.objects.all()
    serializer_class = AnimalInfoSerializer()


class ListSamplesDataView(generics.ListAPIView):
    queryset = SampleDataInfo.objects.all()
    serializer_class = SampleDataInfoSerializer
