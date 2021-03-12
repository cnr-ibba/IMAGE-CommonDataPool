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

from helpers.backend import BACKEND_URL, IMPORT_PASSWORD


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# global variables
SPECIES2COMMON, COMMON2SPECIES = dict(), dict()
SESSION = None


# a function to get the list of common species from data_portal
# TODO: can I return a dict from CDP?
def get_species2commonname():
    """
    Query CDP /species/ endpoint and try to resolve the coorrespondance
    bretween common name (used in dadis for species)and scientific name
    used in CDP

    Raises
    ------
    Exception
        Called if it's not possible to query CDP endpoint

    Returns
    -------
    species2commonnames : dict
        A dictionary with CDP scientific name as keys and common names as
        values for species
    commonnames2species : dict
        A dictionary with common names as key and scientific names as
        values for species
    """

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
def get_fao_metadata(filename="Report_Export_Data.csv"):
    """
    Read the downloaded FAO table, sanitize column name and returns an
    iterator of collections.namedtuple where attributes are table column
    names (lowercase, replacing spaces with "_")

    Parameters
    ----------
    filename : string, optional
        Local path of downloaded FAO metadata table.
        The default is "20201015_Report_Export_Data.csv".

    Yields
    ------
    collections.namedtuple
        A single FAO metadata table record.
    """

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


def parse_fao_records(commonnames2species):
    """
    Process each FAO records, determine the CDP species scientific name and
    return an iterator giving only the data I need for my CDP updates.
    User need to provide the 'supplied_breed' attribute in order to use
    the returned dictionary for dadis_link endpoint updates

    Parameters
    ----------
    commonnames2species : dict
        The species dictionary which relates dad-is common name with the CDP
        scientific name

    Yields
    ------
    data : dictionary
        Data required to update dadis_link endpoint. Please note that the
        supplied breed need to be provided by the user before updating a
        record.
    """

    # great. Now process fao data and filter only the species I have
    for record in filter(
            lambda x: x.species in commonnames2species.keys(),
            get_fao_metadata()):

        # get common name
        common_name = record.species

        # get scientific name from my dictionary
        scientific_name = commonnames2species[common_name]

        # contruct a species dictionary
        species = {
            'common_name': common_name,
            'scientific_name': scientific_name}

        # deal with other name
        other_name = []

        if record.other_name is not None and record.other_name != "":
            other_name = [
                name.strip() for name in record.other_name.split(",")]

        # now create a dictionary for my object
        data = {
            'species': species,
            'most_common_name': record.most_common_name,
            'country': record.country,
            'iso3': record.iso3,
            'transboundary_name': record.transboundary_name,
            'other_name': other_name
        }

        yield data


def process_custom_records():
    """
    Search in CDP for custom links to FAO data (supplied breeds that don't
    match the efabis common_name but which we know the correspondance with FAO
    data). Those record have 'is_custom' attribute set to True. All
    organism records matching the species, country and supplied_breed will be
    updated with those DAD-is records.

    Returns
    -------
    None.

    """

    global SESSION

    # a manually added DAD-IS link (where the supplied_breed doesn't match the
    # FAO breed name) is supposed to be a CUSTOM (=manually added) record
    params = {'is_custom': True}

    logger.info("Search CDP for custom DAD-IS links")

    response = SESSION.get(
        BACKEND_URL + "/dadis_link/",
        params=params)

    response_data = response.json()

    if response_data['count'] == 0:
        logger.debug("No custom DAD-IS link in database")
        return

    logger.debug("Got %s records for %s" % (
        response_data['count'], params))

    # Ok take results and append considering pagination
    dadis_records = response_data['results']

    while response_data['next']:
        response = SESSION.get(response_data['next'])
        response_data = response.json()
        dadis_records += response_data['results']

    # now process custom records
    for dadis in dadis_records:
        params = {
            'species': dadis['species']['scientific_name'],
            'efabis_breed_country': dadis['country'],
            # case insensitive search for supplied breed
            'search': dadis['supplied_breed'],
        }

        # test and update my organism if necessary, relying on custom record
        # 'supplied_breed' column (that must match the organism.supplied_breed
        # I want to annotate)
        update_organism(params, dadis, check_key='supplied_breed')

    logger.info("Custom DAD-IS annotation completed")


def process_fao_records():
    """
    Process the FAO metadata table, filter out records relying on data
    stored in CDP and try to annotate organism relying on 'supplied_breed'
    an FAO columns names ('most_common_name', 'transboundary_name' and
    'other_names').

    Returns
    -------
    None.

    """

    global SESSION

    logger.info("Search into FAO table and trying to update CDP")

    # get species to common names
    SPECIES2COMMON, COMMON2SPECIES = get_species2commonname()

    # get info from summary method
    response = SESSION.get(BACKEND_URL + "/organism/summary/")
    summary = response.json()

    # get all breeds in an array, convert them into lowercase for comparison
    summary_breeds = [breed.lower() for breed in summary['breed']]

    # get data from FAO files and post to CDP
    for dadis in parse_fao_records(COMMON2SPECIES):
        # filter agains my countries
        if dadis['country'] not in summary['country']:
            logger.debug("Skipping %s: Country not in CDP" % dadis)
            continue

        # get params to do filtering in organism endpoint
        params = {
            'species': dadis['species']['scientific_name'],
            'efabis_breed_country': dadis['country'],
        }

        # this will be the dad-is column used for linking dadis
        check_key = None

        if dadis['most_common_name'].lower() in summary_breeds:
            check_key = 'most_common_name'

            # case insensitive search for supplied breed
            params['search'] = dadis[check_key]

            logger.debug(
                f"{dadis}: Found a match in {check_key}: {dadis[check_key]}")

        elif dadis['transboundary_name'].lower() in summary_breeds:
            check_key = 'transboundary_name'

            # case insensitive search for supplied breed
            params['search'] = dadis[check_key]

            logger.debug(
                f"{dadis}: Found a match in {check_key}: {dadis[check_key]}")

        else:
            for name in dadis['other_name']:
                if name.lower() in summary_breeds:
                    check_key = 'other_name'

                    # case insensitive search for supplied breed
                    params['search'] = name

                    logger.debug(
                        f"{dadis}: Found a match in {check_key}: "
                        f"{dadis[check_key]}"
                    )

                    break

                # a match in other name array

            # a cicle in other name

        # Here I should have found a match somewhere or not. If I do, I have
        # a search attribute to get a list of organism to update
        if 'search' in params:
            # test and update my organism if necessary
            update_organism(params, dadis, check_key)

        else:
            logger.debug("Skipping %s: Breed not in CDP" % dadis)

    logger.info("FAO table processing complete")


def update_organism(params, dadis, check_key='most_common_name'):
    """


    Parameters
    ----------
    params : dict
        A dictionary passed to the organism endpoint to filter out organism
        record, relying on endpoint parameters like'species' and
        'efabis_breed_country'. Breed name is searched with 'search' key in
        order to provide a case insensitive search.
    dadis : dict
        A dictionary required to update the dadis_link endpoint, as
        returned by :py:meth:`parse_fao_record`. This function will manage
        the missing 'supplied_breed' keys relying on matched organism
    check_key : string, optional
        The dadis key required the organism 'supplied_breed'. If those values
        are equal, organism will be updated with the dadis link (if missing).
        The default is 'most_common_name'.

    Returns
    -------
    None.

    """

    # need to get all organism by species scientific name, country and
    # supplied breed
    response = SESSION.get(BACKEND_URL + "/organism/", params=params)
    response_data = response.json()

    if response_data['count'] == 0:
        logger.debug("Skipping %s: Breed not in CDP" % params)
        return

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
        # since I'm searching for breed name (not exact) I need to filter
        # out partial matches

        # check other_name first, since its a special case
        if check_key == 'other_name':
            other_name = [name.lower() for name in dadis['other_name']]
            if organism['supplied_breed'].lower() not in other_name:
                logger.warning("Skipping %s: breeds differ (%s:%s)" % (
                    organism['data_source_id'],
                    organism['supplied_breed'],
                    other_name
                    )
                )
                continue

            logger.debug(
                f"Found a match in {check_key}: {organism['supplied_breed']}"
                f": {other_name}"
            )

        # check most common name and transboundary breeds
        elif organism['supplied_breed'].lower() != \
                dadis[check_key].lower():
            logger.warning("Skipping %s: breeds differ (%s:%s)" % (
                organism['data_source_id'],
                organism['supplied_breed'],
                dadis[check_key].lower()
                )
            )
            continue

        logger.debug(
            f"Found a match in {check_key}: {organism['supplied_breed']}"
            f": {dadis[check_key]}"
        )

        # test for dadis link in my organism. If already set, I don't need an
        # update.
        # TODO: could fetch this with a REST query?
        if organism['dadis']:
            logger.debug(
                "Skipping %s: dadis link already set" % (
                    organism['data_source_id']))
            continue

        # get the unique URL
        url = organism['url']

        # add supplied breed to dadis dictionary (mandatory for updates)
        tmp = dadis.copy()
        tmp['supplied_breed'] = organism['supplied_breed']

        # define data to patch
        data = {
            'dadis': tmp
        }

        logger.debug("Patching %s" % url)

        # patch object
        response = SESSION.patch(url, json=data)

        if response.status_code != 200:
            logger.error(response.text)

        counter += 1

    # block for a single record
    if counter > 0:
        logger.info(
            f"Updated {counter} record for '{params['search']}': {dadis}")


if __name__ == "__main__":
    logger.info("Starting process_fao_metadata")

    # start a session with CDP
    SESSION = requests.Session()
    SESSION.auth = ('admin', IMPORT_PASSWORD)

    # read data from FAO CSV table and update database
    process_fao_records()

    # read data from custom records and update database
    process_custom_records()

    # cicle for all records in dadis table
    logger.info("process_fao_metadata completed")
