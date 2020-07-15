#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:34:11 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os
import json

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from ..models import Organism

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

User = get_user_model()


class CommonMixin():
    fixtures = [
        "backend/organism"
    ]

    def setUp(self):
        user = User.objects.create(username="test", email="test")
        user.set_password("password")
        user.save()

        self.client.login(username="test", password="password")


class OrganismTestCase(CommonMixin, APITestCase):
    def setUp(self):
        super().setUp()

        # custom data
        self.dadis = {
            "species": {
                "scientific_name": "Bos taurus",
                "common_name": "Cattle"
            },
            "supplied_breed": "Asturiana de los Valles",
            "efabis_breed_country": "Spain",
            "dadis_url": (
                "https://dadis-breed-4eff5.firebaseapp.com/?country=Spain"
                "&specie=Cattle&breed=Asturiana%20de%20los%20Valles"
                "&callback=allbreeds")
        }

    def test_create_organism(self):
        # delete object before creating
        Organism.objects.all().delete()

        url = api_reverse("backend:organismindex")

        with open(os.path.join(BASE_DIR, "data/SAMEA7044752.json")) as handle:
            data = json.load(handle)

        # add dadis data
        data["dadis"] = self.dadis

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organism.objects.count(), 1)

    def test_update_organism(self):
        with open(os.path.join(BASE_DIR, "data/SAMEA7044752.json")) as handle:
            data = json.load(handle)

        data["dadis"] = self.dadis

        # update point is different
        url = api_reverse(
            "backend:organismdetail", args=["SAMEA7044752"])

        # update organism with put method
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_organism(self):
        url = api_reverse("backend:organismindex")
        response = self.client.get(url)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['data_source_id'], "SAMEA7044752")


class GISSearchTestCase(CommonMixin, APITestCase):
    def test_search(self):
        url = api_reverse("backend:organism_gis_search")
        response = self.client.get(
            url,
            {'latitude': 51,
             'longitude': 10,
             'radius': 1})
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        test = results[0]
        reference = {
            "data_source_id": "SAMEA7044752",
            "species": "Gallus gallus",
            "supplied_breed": "chicken",
            "sex": "female"
        }
        self.assertDictEqual(reference, test)

    def test_summary(self):
        url = api_reverse("backend:organism_graphical_summary")
        response = self.client.get(url)
        test = response.data
        reference = {
            'species': {'Gallus gallus': 1},
            'breeds': {'Gallus gallus': {'chicken': 1}},
            'countries': {'Germany': 1},
            'coordinates': [('10.000000', '51.000000')]
        }
        self.assertDictEqual(reference, test)


class GeoJSONTestCase(CommonMixin, APITestCase):
    def test_get_organism(self):
        url = api_reverse("backend:geoorganism_list")
        response = self.client.get(url)
        data = response.data
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertEqual(data["count"], 1)

        # convert a nested OrderedDict to dict
        test = json.loads(json.dumps(data['features'][0]))

        reference = {
            "id": "SAMEA7044752",
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    10.0,
                    51.0
                ]
            },
            "properties": {
                "url": (
                    "http://testserver/backend/organism.geojson/"
                    "SAMEA7044752/"),
                "species": "Gallus gallus",
                "supplied_breed": "chicken",
                "sex": "female"
            }
        }

        # asserta a GeoJSON object
        self.assertDictEqual(reference, test)
