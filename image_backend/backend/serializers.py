from rest_framework import serializers

from .models import SampleInfo, AnimalInfo, SampleDataInfo


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = ('organism_part', 'collection_date')


class SampleInfoSerializer(serializers.ModelSerializer):
    specimens = SampleDataInfoSerializer(many=True, read_only=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'specimens')


class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = "__all__"



# class ExperimentInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExperimentInfo
#         fields = "__all__"
