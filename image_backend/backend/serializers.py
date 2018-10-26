from rest_framework import serializers

from .models import SampleInfo, AnimalInfo, SampleDataInfo


class SampleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleInfo
        fields = "__all__"


class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = "__all__"


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = "__all__"



# class ExperimentInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExperimentInfo
#         fields = "__all__"
