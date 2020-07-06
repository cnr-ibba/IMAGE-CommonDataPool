from rest_framework import serializers

from .models import (
    Specimen, Organism, Files, Species2CommonName,
    DADISLink)


class EtagSerializer(serializers.ModelSerializer):
    class Meta:
        # FIXME: this should return both Specimens and Organism etags
        model = Organism
        fields = (
            'data_source_id',
            'etag'
        )


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('data_source_id', 'file_name', 'file_url', 'file_size',
                  'file_checksum', 'file_checksum_method')


class SpecimenSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='backend:specimendetail',
        lookup_field='data_source_id'
    )

    class Meta:
        model = Specimen


class SpecimenSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Specimen
        fields = (
            'data_source_id', 'species', 'derived_from', 'organism_part',
            'collection_place_latitude', 'collection_place_longitude'
        )


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


class OrganismSerializer(serializers.ModelSerializer):
    dadis = DADISLinkSerializer(many=False, required=False, allow_null=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='backend:organismdetail',
        lookup_field='data_source_id'
    )

    class Meta:
        model = Organism
        read_only_fields = ['dadis']

    def create(self, validated_data):
        # need to get cut the dadis attribute
        dadis_data = validated_data.pop('dadis', None)
        dadis = None

        # create a new DADIS object
        if dadis_data:
            species = dadis_data.pop('species')
            species_obj = Species2CommonName.objects.get(**species)
            dadis, _ = DADISLink.objects.get_or_create(
                species=species_obj, **dadis_data)

        organism = Organism.objects.create(dadis=dadis, **validated_data)

        return organism


class OrganismSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = (
            'data_source_id', 'species', 'organisms', 'supplied_breed',
            'efabis_breed_country', 'sex', 'birth_location_longitude',
            'birth_location_latitude'
        )
