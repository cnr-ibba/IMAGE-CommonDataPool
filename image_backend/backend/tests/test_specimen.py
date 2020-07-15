#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 18:44:15 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os
import json

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from ..models import Specimen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

User = get_user_model()


class CommonMixin():
    fixtures = [
        "backend/specimen"
    ]

    def setUp(self):
        user = User.objects.create(username="test", email="test")
        user.set_password("password")
        user.save()

        self.client.login(username="test", password="password")


class SpecimenTestCase(CommonMixin, APITestCase):
    def test_create_specimen(self):
        # delete object before creating
        Specimen.objects.all().delete()

        url = api_reverse("backend:specimenindex")

        with open(os.path.join(BASE_DIR, "data/SAMEA7044739.json")) as handle:
            data = json.load(handle)

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Specimen.objects.count(), 1)

    def test_update_specimen(self):
        with open(os.path.join(BASE_DIR, "data/SAMEA7044739.json")) as handle:
            data = json.load(handle)

        # update point is different
        url = api_reverse(
            "backend:specimendetail", args=["SAMEA7044739"])

        # update organism with put method
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specimen(self):
        url = api_reverse("backend:specimenindex")
        response = self.client.get(url)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['data_source_id'], "SAMEA7044739")


class GISSearchTestCase(CommonMixin, APITestCase):
    def test_search(self):
        url = api_reverse("backend:specimen_gis_search")
        response = self.client.get(
            url,
            {'latitude': 51,
             'longitude': 10,
             'radius': 1})
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        test = results[0]
        reference = {
            "data_source_id": "SAMEA7044739",
            "species": "Gallus gallus",
            "derived_from": "SAMEA7044752",
            "organism_part": "blood"
        }
        self.assertDictEqual(reference, test)

    def test_summary(self):
        url = api_reverse("backend:specimens_graphical_summary")
        response = self.client.get(url)
        test = response.data
        reference = {
            'organism_part': {'blood': 1},
            'coordinates': [('10.000000', '51.000000')]
        }
        self.assertDictEqual(reference, test)


class GeoJSONTestCase(CommonMixin, APITestCase):
    def test_get_specimen(self):
        url = api_reverse("backend:geospecimen_list")
        response = self.client.get(url)
        data = response.data
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertEqual(data["count"], 1)

        # convert a nested OrderedDict to dict
        test = json.loads(json.dumps(data['features'][0]))

        reference = {
            "id": "SAMEA7044739",
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
                    "http://testserver/data_portal/backend/specimen.geojson/"
                    "SAMEA7044739/"),
                "species": "Gallus gallus",
                "derived_from": "SAMEA7044752",
                "organism_part": "blood"
            }
        }

        # asserta a GeoJSON object
        self.assertDictEqual(reference, test)
