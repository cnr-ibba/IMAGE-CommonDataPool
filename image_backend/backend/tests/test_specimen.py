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


class SpecimenTestCase(APITestCase):
    fixtures = [
        "backend/specimen"
    ]

    def setUp(self):
        user = User.objects.create(username="test", email="test")
        user.set_password("password")
        user.save()

        self.client.login(username="test", password="password")

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
