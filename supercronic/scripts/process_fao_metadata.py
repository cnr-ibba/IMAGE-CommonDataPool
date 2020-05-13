#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 19:13:23 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>

A module to parse FAO exported metadata

"""

import re
import csv
import logging
import requests
import collections

from decouple import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# global variables
SPECIES2COMMON, COMMON2SPECIES = dict(), dict()
SESSION = None

BACKEND_URL = 'http://nginx/data_portal/backend'
IMPORT_PASSWORD = config('IMPORT_PASSWORD')


# a function to get the list of common species from data_portal
# TODO: can I return a dict from CDP?
def get_species2commonname():
    global SESSION

    response = SESSION.get(BACKEND_URL + '/species/')

    if response.status_code != 200:
        raise Exception(response.text)

    species2commonnames = dict()
    commonnames2species = dict()

    for item in response.json():
        scientific_name = item['scientific_name']
        common_name = item['common_name']

        species2commonnames[scientific_name] = common_name
        commonnames2species[common_name] = scientific_name

    return species2commonnames, commonnames2species


# a function to get back fao metadata
def get_metadata(filename="Report_Export_Data.csv"):
    pattern = re.compile(r"(.*)_\((.*)\)_?(.*)")

    def sanitize(col, pattern=pattern):
        match = re.search(pattern, col)

        if match:
            return "_".join(
                filter(
                    lambda item: len(item) > 0,
                    re.search(pattern, col).groups()))

        else:
            return col

    handle = open(filename)

    # throw away the first two lines
    for i in range(2):
        line = handle.readline().strip()
        logger.warning(f"Ignoring line {i}: {line}")

    # Ok now track the position of the file
    position = handle.tell()

    # sniff data and try to determine file type
    chunk = handle.read(2048)
    dialect = csv.Sniffer().sniff(chunk)

    logger.info(dialect)

    # rewind file
    handle.seek(position)

    # now process data with csv
    reader = csv.reader(handle, dialect)

    # get header
    header = next(reader)

    # now replace space and pharentesis from header
    header = [col.replace(" ", "_").lower() for col in header]

    # sanitize column names (remove parenthesis)
    header = [sanitize(col) for col in header]

    logger.info(header)
    logger.info(f"Header length {len(header)}")

    Row = collections.namedtuple("Row", header+['extra_field'], rename=True)

    # now process data
    for line in reader:
        if len(line) > len(header):
            line, extra_field = line[:len(header)], \
                ",".join(line[len(header):])

        record = Row._make(line + [extra_field])
        logger.debug(record)

        yield record

    handle.close()


def process_record(commonnames2species):
    # great. Now process fao data and filter only the species I have
    for record in filter(
            lambda x: x.specie in commonnames2species.keys(),
            get_metadata()):

        # get common name
        common_name = record.specie

        # get scientific name from my dictionary
        scientific_name = commonnames2species[common_name]

        # contruct a species dictionary
        species = {
            'common_name': common_name,
            'scientific_name': scientific_name}

        # now create a dictionary for my object
        data = {
            'species': species,
            'supplied_breed': record.most_common_name,
            'efabis_breed_country': record.country
        }

        yield data


if __name__ == "__main__":
    logger.info("Starting process_fao_metadata")

    # start a session with CDP
    SESSION = requests.Session()
    SESSION.auth = ('admin', IMPORT_PASSWORD)

    # get species to common names
    SPECIES2COMMON, COMMON2SPECIES = get_species2commonname()

    # get info from summary method
    response = SESSION.get(BACKEND_URL + "/organism/summary/")
    summary = response.json()

    # get all breeds in an array, convert them into lowercase for comparison
    summary_breeds = [breed.lower() for breed in summary['breed']]

    # get data from FAO files and post to CDP
    for dadis in process_record(COMMON2SPECIES):
        # filter agains my countries
        if dadis['efabis_breed_country'] not in summary['country']:
            logger.debug("Skipping %s: Country not in CDP" % dadis)
            continue

        # filter also by breeds in summary
        if dadis['supplied_breed'].lower() not in summary_breeds:
            logger.debug("Skipping %s: Breed not in CDP" % dadis)
            continue

        # get params to do filtering
        params = {
            'species': dadis['species']['scientific_name'],
            'organisms__efabis_breed_country': dadis['efabis_breed_country'],
            # case insensitive search for supplied breed
            'search': dadis['supplied_breed'],
        }

        # need to get all organism by species scientific name, country and
        # supplied breed
        response = SESSION.get(BACKEND_URL + "/organism/", params=params)
        response_data = response.json()

        if response_data['count'] == 0:
            logger.debug("Skipping %s: Breed not in CDP" % dadis)
            continue

        logger.debug("Got %s records for %s" % (
            response_data['count'], params))

        # Ok take results and append considering pagination
        organisms = response_data['results']

        while response_data['next']:
            response = SESSION.get(response_data['next'])
            response_data = response.json()
            organisms += response_data['results']

        # count how many insert I did
        counter = 0

        # now update organisms dadis record
        for organism in organisms:
            # test for dadis link
            if organism['organisms'][0]['dadis']:
                logger.debug(
                    "Skipping %s: dadis link already set" % (
                        organism['data_source_id']))
                continue

            # get the unique URL
            url = organism['url']

            # define data to patch
            data = {
                'organisms': [{'dadis': dadis}]
            }

            logger.debug("Patching %s" % url)

            # patch object
            response = SESSION.patch(url, json=data)

            if response.status_code != 200:
                logger.error(response.text)

            counter += 1

        # block for a single record
        if counter > 0:
            logger.info("Updated %s record for %s" % (counter, dadis))

    # cicle for all records in dadis table
    logger.info("process_fao_metadata completed")
