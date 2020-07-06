#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:45:34 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from ..models import DADISLink

User = get_user_model()


class DADISLinkTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test", email="test")
        user.set_password("password")
        user.save()

        self.client.login(username="test", password="password")

    def test_create_dadis(self):
        url = api_reverse("backend:dadis_link")

        data = {
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
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DADISLink.objects.count(), 1)
