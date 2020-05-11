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


def fill_dadis(record):
    global SPECIES2COMMON, SESSION

    scientific_name = record['species']

    if scientific_name not in SPECIES2COMMON:
        # this species hasn't a coorrespondance in species tables, so
        # I can't provide a link for dadis
        logger.error(f"'{scientific_name}' is not modelled for DADIS")
        return

    common_name = SPECIES2COMMON[scientific_name]

    # contruct a species dictionary
    species = {
        'common_name': common_name,
        'scientific_name': scientific_name}

    # now create a dictionary for my object
    data = {
        'species': species,
        'supplied_breed': record['organisms'][0]['supplied_breed'],
        'efabis_breed_country': record['organisms'][0]['efabis_breed_country']
    }

    # check if record exists
    response = SESSION.get(BACKEND_URL + "/dadis_link/", params=data)

    dadis_data = None

    if response.json()['count'] == 0:
        response = SESSION.post(
            BACKEND_URL + '/dadis_link/',
            json=data)

        if response.status_code != 201:
            raise Exception(f"Cannot set {data}")

        else:
            logger.debug(f"{data} added to CDP")
            dadis_data = response.json()

    elif response.json()['count'] == 1:
        logger.debug(f"{data} already in CDP")
        dadis_data = response.json()['results'][0]

    else:
        raise Exception(response.json())

    # return dadis data to complete organism insert
    logger.debug(dadis_data)

    return dadis_data


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
    # start a session with CDP
    SESSION = requests.Session()
    SESSION.auth = ('admin', IMPORT_PASSWORD)

    # get species to common names
    SPECIES2COMMON, COMMON2SPECIES = get_species2commonname()

    # get data from FAO files and post to CDP
    for record in process_record(COMMON2SPECIES):
        # TODO: need to get all organism by species scientific name, country and supplied breed
        print(record)
        break
