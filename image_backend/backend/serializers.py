from rest_framework import serializers

from .models import SampleInfo, AnimalInfo, SampleDataInfo


class SampleDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleDataInfo
        fields = "__all__"


class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInfo
        fields = "__all__"


class SpecimensSerializer(serializers.ModelSerializer):
    specimens = SampleDataInfoSerializer(many=True, read_only=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'project', 'submission_title', 'material', 'person_last_name',
                  'person_email', 'person_affiliation', 'person_role', 'organization_name', 'organization_role',
                  'gene_bank_name', 'gene_bank_country', 'data_source_type', 'data_source_version', 'species',
                  'submission_description', 'person_first_name', 'organization_address', 'organization_country',
                  'description', 'person_initial', 'organization_uri', 'publication_doi', 'specimens')


class OrganismsSerializer(serializers.ModelSerializer):
    organisms = AnimalInfoSerializer(many=True, read_only=True)

    class Meta:
        model = SampleInfo
        fields = ('data_source_id', 'alternative_id', 'project', 'submission_title', 'material', 'person_last_name',
                  'person_email', 'person_affiliation', 'person_role', 'organization_name', 'organization_role',
                  'gene_bank_name', 'gene_bank_country', 'data_source_type', 'data_source_version', 'species',
                  'submission_description', 'person_first_name', 'organization_address', 'organization_country',
                  'description', 'person_initial', 'organization_uri', 'publication_doi', 'organisms')
