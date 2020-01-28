from rest_framework import serializers

from .models import SampleInfo, AnimalInfo, SampleDataInfo


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = ('derived_from', 'collection_place_accuracy', 'organism_part',
                  'organism_part_ontology', 'specimen_collection_protocol',
                  'collection_date', 'collection_date_unit',
                  'collection_place_latitude', 'collection_place_latitude_unit',
                  'collection_place_longitude',
                  'collection_place_longitude_unit', 'collection_place',
                  'developmental_stage', 'developmental_stage_ontology',
                  'physiological_stage', 'physiological_stage_ontology',
                  'availability', 'sample_storage', 'sample_storage_processing',
                  'animal_age_at_collection', 'animal_age_at_collection_unit',
                  'sampling_to_preparation_interval',
                  'sampling_to_preparation_interval_unit')


class SampleDataInfoSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = ('derived_from', 'organism_part',
                  'collection_place_latitude', 'collection_place_longitude')


class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = ('supplied_breed', 'efabis_breed_country', 'sex',
                  'sex_ontology', 'birth_location_accuracy', 'mapped_breed',
                  'mapped_breed_ontology', 'birth_date', 'birth_date_unit',
                  'birth_location', 'birth_location_longitude',
                  'birth_location_longitude_unit', 'birth_location_latitude',
                  'birth_location_latitude_unit', 'child_of')


class AnimalInfoSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = ('supplied_breed', 'efabis_breed_country', 'sex',
                  'birth_location_longitude', 'birth_location_latitude')


class SpecimensSerializer(serializers.ModelSerializer):
    specimens = SampleDataInfoSerializer(many=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'project',
                  'submission_title', 'material', 'material_ontology',
                  'person_last_name', 'person_email', 'person_affiliation',
                  'person_role', 'person_role_ontology', 'organization_name',
                  'organization_role', 'organization_role_ontology',
                  'gene_bank_name', 'gene_bank_country',
                  'gene_bank_country_ontology', 'data_source_type',
                  'data_source_version', 'species', 'species_ontology', 'etag',
                  'submission_description', 'person_first_name',
                  'organization_address', 'organization_country',
                  'organization_country_ontology', 'description',
                  'person_initial', 'organization_uri', 'publication_doi',
                  'specimens')

    def create(self, validated_data):
        specimens_data = validated_data.pop('specimens')
        sample = SampleInfo.objects.create(**validated_data)
        for specimen in specimens_data:
            SampleDataInfo.objects.create(sample=sample, **specimen)
        return sample


class SpecimensSerializerShort(serializers.ModelSerializer):
    specimens = SampleDataInfoSerializerShort(many=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'species', 'specimens')

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
        fields = ('data_source_id', 'alternative_id', 'project',
                  'submission_title', 'material', 'material_ontology',
                  'person_last_name', 'person_email', 'person_affiliation',
                  'person_role', 'person_role_ontology', 'organization_name',
                  'organization_role', 'organization_role_ontology',
                  'gene_bank_name', 'gene_bank_country',
                  'gene_bank_country_ontology', 'data_source_type',
                  'data_source_version', 'species', 'species_ontology', 'etag',
                  'submission_description', 'person_first_name',
                  'organization_address', 'organization_country',
                  'organization_country_ontology', 'description',
                  'person_initial', 'organization_uri', 'publication_doi',
                  'organisms')

    def create(self, validated_data):
        organisms_data = validated_data.pop('organisms')
        sample = SampleInfo.objects.create(**validated_data)
        for organism in organisms_data:
            AnimalInfo.objects.create(sample=sample, **organism)
        return sample


class OrganismsSerializerShort(serializers.ModelSerializer):
    organisms = AnimalInfoSerializerShort(many=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'species', 'organisms')

    def create(self, validated_data):
        organisms_data = validated_data.pop('organisms')
        sample = SampleInfo.objects.create(**validated_data)
        for organism in organisms_data:
            AnimalInfo.objects.create(sample=sample, **organism)
        return sample
