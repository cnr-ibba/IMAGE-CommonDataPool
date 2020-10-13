#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:26:45 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os
import csv
import collections

from django.core.management import BaseCommand

from backend.models import Species2CommonName, DADISLink


class Command(BaseCommand):
    help = 'Fill dadis link table with customized links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--table',
            type=str,
            default="custom_dad-is.csv",
            help="Provide a custom dad-is table"
        )

    def handle(self, *args, **options):
        """Import custom data into dadis table"""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, options['table'])

        # open data file
        handle = open(filename)
        reader = csv.reader(handle, delimiter=";")

        # species;supplied_breed;efabis_breed_country;dadis_url
        header = next(reader)

        # define data type
        Data = collections.namedtuple('Data', header)

        for row in map(Data._make, reader):
            # get a specie
            species = Species2CommonName.objects.get(
                scientific_name=row.species)

            # create a record
            instance, created = DADISLink.objects.update_or_create(
                species=species,
                supplied_breed=row.supplied_breed,
                efabis_breed_country=row.efabis_breed_country,
                dadis_url=row.dadis_url
            )

            if created:
                print(f"Created {instance}")
