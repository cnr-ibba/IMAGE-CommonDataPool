from rest_framework import serializers

from .models import SampleInfo, AnimalInfo, SampleDataInfo


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = ('derived_from', 'collection_date', 'collection_place', 'collection_place_accuracy', 'organism_part',
                  'specimen_collection_protocol', 'collection_place_latitude', 'collection_place_longitude',
                  'developmental_stage', 'physiological_stage', 'availability', 'sample_storage',
                  'sample_storage_processing', 'animal_age_at_collection', 'sampling_to_preparation_interval')


class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = ('supplied_breed', 'efabis_breed_country', 'sex', 'birth_location_accuracy', 'mapped_breed',
                  'birth_location', 'birth_location_longitude', 'birth_location_latitude', 'child_of')


class SpecimensSerializer(serializers.ModelSerializer):
    specimens = SampleDataInfoSerializer(many=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'project', 'submission_title', 'material', 'person_last_name',
                  'person_email', 'person_affiliation', 'person_role', 'organization_name', 'organization_role',
                  'gene_bank_name', 'gene_bank_country', 'data_source_type', 'data_source_version', 'species',
                  'submission_description', 'person_first_name', 'organization_address', 'organization_country',
                  'description', 'person_initial', 'organization_uri', 'publication_doi', 'specimens')

    def create(self, validated_data):
        specimens_data = validated_data.pop('specimens')
        sample = SampleInfo.objects.create(**validated_data)
        for specimen in specimens_data:
            SampleDataInfo.objects.create(sample=sample, **specimen)
        return sample


class OrganismsSerializer(serializers.ModelSerializer):
    organisms = AnimalInfoSerializer(many=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'project', 'submission_title', 'material', 'person_last_name',
                  'person_email', 'person_affiliation', 'person_role', 'organization_name', 'organization_role',
                  'gene_bank_name', 'gene_bank_country', 'data_source_type', 'data_source_version', 'species',
                  'submission_description', 'person_first_name', 'organization_address', 'organization_country',
                  'description', 'person_initial', 'organization_uri', 'publication_doi', 'organisms')

    def create(self, validated_data):
        organisms_data = validated_data.pop('organisms')
        sample = SampleInfo.objects.create(**validated_data)
        for organism in organisms_data:
            AnimalInfo.objects.create(sample=sample, **organism)
        return sample
