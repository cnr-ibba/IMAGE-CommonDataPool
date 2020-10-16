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

        # species;supplied_breed;country;most_common_name;transboundary_name;other_name
        header = next(reader)

        # define data type
        Data = collections.namedtuple('Data', header)

        for row in map(Data._make, reader):
            # get a specie
            species = Species2CommonName.objects.get(
                scientific_name=row.species)

            # deal with other name
            other_name = []

            if row.other_name is not None and row.other_name != "":
                other_name = [
                    name.strip() for name in row.other_name.split(",")]

            # create a record
            instance, created = DADISLink.objects.update_or_create(
                species=species,
                supplied_breed=row.supplied_breed,
                country=row.country,
                most_common_name=row.most_common_name,
                transboundary_name=row.transboundary_name,
                other_name=other_name,
                is_custom=True
            )

            if created:
                print(f"Created {instance}")
