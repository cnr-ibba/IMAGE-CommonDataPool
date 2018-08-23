from rest_framework import generics

from .models import SampleInfo, ExperimentInfo
from .serializers import SampleInfoSerializer, ExperimentInfoSerializer


class ListExperimentsView(generics.ListAPIView):
    queryset = ExperimentInfo.objects.all()
    serializer_class = ExperimentInfoSerializer


class ListSamplesView(generics.ListAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = SampleInfoSerializer
