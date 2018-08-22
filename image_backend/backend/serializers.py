from rest_framework import serializers

from .models import SampleInfo


class SampleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleInfo
        fields = ('biosample_id')
