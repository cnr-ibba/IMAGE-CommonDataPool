from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import (
    SampleInfo, AnimalInfo, SampleDataInfo, Files, Species2CommonName,
    DADISLink)


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('data_source_id', 'file_name', 'file_url', 'file_size',
                  'file_checksum', 'file_checksum_method')


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = (
            'derived_from', 'collection_place_accuracy', 'organism_part',
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


class Species2CommonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species2CommonName
        fields = ('scientific_name', 'common_name')


class DADISLinkSerializer(serializers.HyperlinkedModelSerializer):
    species = Species2CommonNameSerializer(many=False, read_only=False)

    url = serializers.HyperlinkedIdentityField(
        view_name='backend:dadis_link-detail',
        lookup_field='pk'
    )

    class Meta:
        model = DADISLink
        fields = (
            'url',
            'species',
            'supplied_breed',
            'efabis_breed_country',
            'dadis_url',
        )

    def create(self, validated_data):
        species = validated_data.pop('species')
        species_obj = Species2CommonName.objects.get(**species)
        dadis = DADISLink.objects.create(species=species_obj, **validated_data)

        return dadis


class AnimalInfoSerializer(serializers.ModelSerializer):
    dadis = DADISLinkSerializer(many=False, required=False, allow_null=True)

    class Meta:
        model = AnimalInfo
        fields = ('supplied_breed', 'efabis_breed_country', 'sex',
                  'sex_ontology', 'birth_location_accuracy', 'mapped_breed',
                  'mapped_breed_ontology', 'birth_date', 'birth_date_unit',
                  'birth_location', 'birth_location_longitude',
                  'birth_location_longitude_unit', 'birth_location_latitude',
                  'birth_location_latitude_unit', 'child_of', 'specimens',
                  'dadis')
        read_only_fields = ['dadis']


class AnimalInfoSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = ('supplied_breed', 'efabis_breed_country', 'sex',
                  'birth_location_longitude', 'birth_location_latitude')


class SpecimensSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='backend:specimendetail',
        lookup_field='data_source_id'
    )

    specimens = SampleDataInfoSerializer(many=True)

    class Meta:
        model = SampleInfo
        fields = ('url', 'data_source_id', 'alternative_id', 'project',
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

    def __update_instance(self, instance, validated_data):
        # ok update SampleInfo
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    def update(self, instance, validated_data):
        specimens_data = validated_data.pop('specimens', None)

        # ok update SampleInfo
        instance = self.__update_instance(instance, validated_data)

        if specimens_data:
            # Ok delete all AnimalInfo related objects
            # HINT: will be simpler with a One2One relationship
            instance.specimens.all().delete()

            # now process organism
            for specimen_data in specimens_data:
                # recreate info
                SampleDataInfo.objects.create(
                    sample=instance, **specimen_data)

        return instance


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


class OrganismsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='backend:organismdetail',
        lookup_field='data_source_id'
    )

    organisms = AnimalInfoSerializer(many=True)

    class Meta:
        model = SampleInfo
        fields = ('url', 'data_source_id', 'alternative_id', 'project',
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
            # need to get cut the dadis attribute
            dadis_data = organism.pop('dadis', None)

            if dadis_data:
                dadis = DADISLink.get_instance_from_dict(dadis_data)
            else:
                dadis = None

            AnimalInfo.objects.create(dadis=dadis, sample=sample, **organism)

        return sample

    def __update_instance(self, instance, validated_data):
        # ok update SampleInfo
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    def update(self, instance, validated_data):
        organisms_data = validated_data.pop('organisms', None)

        # ok update SampleInfo
        instance = self.__update_instance(instance, validated_data)

        if organisms_data:
            # Ok delete all AnimalInfo related objects
            # HINT: will be simpler with a One2One relationship
            instance.organisms.all().delete()

            # now process organism
            for organism_data in organisms_data:
                # not sure about this
                dadis_data = organism_data.pop('dadis', None)

                if dadis_data:
                    dadis = DADISLink.get_instance_from_dict(dadis_data)
                else:
                    dadis = None

                # recreate info
                AnimalInfo.objects.create(
                    dadis=dadis, sample=instance, **organism_data)

        return instance


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
