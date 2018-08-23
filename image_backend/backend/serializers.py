from rest_framework import serializers

from .models import SampleInfo, ExperimentInfo


class SampleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleInfo
        fields = "__all__"


class ExperimentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentInfo
        fields = "__all__"
