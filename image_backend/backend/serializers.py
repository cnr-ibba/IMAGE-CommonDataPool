
from collections import OrderedDict

from django.contrib.gis.geos import Point

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.utils import model_meta

from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import (
    Specimen, Organism, Files, Species2CommonName, DADISLink, Etag)


class EtagSerializer(serializers.ModelSerializer):
    class Meta:
        # FIXME: this should return both Specimens and Organism etags
        model = Etag
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
        read_only_fields = ['geom']

    def check_coordinates(self, validated_data):
        geom = None

        lng = validated_data.get('collection_place_longitude')
        lat = validated_data.get('collection_place_latitude')

        if lng and lat:
            try:
                lng = float(lng)
                lat = float(lat)

            except ValueError:
                # I can't make a point
                return geom

            geom = Point(lng, lat, srid=4326)

        return geom

    def create(self, validated_data):
        # check coordinates
        geom = self.check_coordinates(validated_data)

        specimen = Specimen.objects.create(
            geom=geom,
            **validated_data
        )

        return specimen

    def update(self, instance, validated_data):
        """Override the default update method to update geom data"""

        instance = super().update(instance, validated_data)

        # check coordinates
        geom = self.check_coordinates(validated_data)

        if geom:
            # update geom coordinates
            instance.geom = geom
            instance.save()

        return instance


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
        read_only_fields = ['dadis', 'geom']

    def check_coordinates(self, validated_data):
        geom = None

        lng = validated_data.get('birth_location_longitude')
        lat = validated_data.get('birth_location_latitude')

        if lng and lat:
            try:
                lng = float(lng)
                lat = float(lat)

            except ValueError:
                # I can't make a point
                return geom

            geom = Point(lng, lat, srid=4326)

        return geom

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

        # check coordinates
        geom = self.check_coordinates(validated_data)

        organism = Organism.objects.create(
            dadis=dadis,
            geom=geom,
            **validated_data
        )

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

        # check coordinates
        geom = self.check_coordinates(validated_data)

        if geom:
            instance.geom = geom
            instance.save()

        return instance


class GeoOrganismSerializer(GeoFeatureModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='backend:geoorganism_detail',
        lookup_field='data_source_id'
    )

    distance = serializers.DecimalField(
        # get distance in kilometers
        source="distance.km",
        decimal_places=3,
        max_digits=8,
        read_only=True,
        required=False
    )

    class Meta:
        model = Organism
        geo_field = "geom"
        fields = (
            "url",
            "data_source_id",
            "species",
            "supplied_breed",
            "sex",
            "distance",
        )
        read_only_fields = ['distance']

    # override django-rest-framework-gis.serializers
    def get_properties(self, instance, fields):
        """
        Get the feature metadata which will be used for the GeoJSON
        "properties" key.
        By default it returns all serializer fields excluding those used for
        the ID, the geometry and the bounding box.
        :param instance: The current Django model instance
        :param fields: The list of fields to process (fields already processed have been removed)
        :return: OrderedDict containing the properties of the current feature
        :rtype: OrderedDict
        """

        properties = OrderedDict()

        for field in fields:
            if field.write_only:
                continue
            # similar to django-rest-framework.serializer.to_representation
            try:
                value = field.get_attribute(instance)
            except SkipField:
                continue
            representation = None
            if value is not None:
                representation = field.to_representation(value)
            properties[field.field_name] = representation

        return properties


class OrganismSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = (
            'data_source_id', 'species', 'supplied_breed',
            'efabis_breed_country', 'sex', 'birth_location_longitude',
            'birth_location_latitude'
        )
