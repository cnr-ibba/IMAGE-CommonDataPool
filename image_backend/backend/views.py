from rest_framework import generics

from .models import SampleInfo
from .serializers import SampleInfoSerializer


class ListSamplesView(generics.ListAPIView):
    queryset = SampleInfo.objects.all()
    serializer_class = SampleInfoSerializer
