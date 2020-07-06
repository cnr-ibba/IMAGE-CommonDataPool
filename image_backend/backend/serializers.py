from rest_framework import serializers
from rest_framework.utils import model_meta

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
        fields = '__all__'


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
        fields = '__all__'
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

    def update(self, instance, validated_data):
        """Override the default update method which doens't support nested
        objects"""

        dadis_data = validated_data.pop('dadis', None)

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

        # create a new DADIS object if necessary and update instance
        if dadis_data:
            species = dadis_data.pop('species')
            species_obj = Species2CommonName.objects.get(**species)

            # get or create a DADis object
            dadis, _ = DADISLink.objects.get_or_create(
                species=species_obj, **dadis_data)

            # track relationship with dadis
            instance.dadis = dadis
            instance.save()

        return instance


class OrganismSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = (
            'data_source_id', 'species', 'supplied_breed',
            'efabis_breed_country', 'sex', 'birth_location_longitude',
            'birth_location_latitude'
        )
