#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:41:54 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import logging
import aiohttp
import asyncio

from multidict import MultiDict
from enum import Enum
from decouple import config

from .common import parse_json, HEADERS, fetch_page

# Setting page size for CDP requests
PAGE_SIZE = 500

# define custom parameters
PARAMS = MultiDict([
    ('page_size', PAGE_SIZE),
])

# limiting the number of connections
# https://docs.aiohttp.org/en/stable/client_advanced.html
CONNECTOR = aiohttp.TCPConnector(limit=20, ttl_dns_cache=300)

BACKEND_URL = 'http://nginx/backend'
IMPORT_PASSWORD = config('IMPORT_PASSWORD')
SAMPLE_RULESET_URL = (
    'https://raw.githubusercontent.com/cnr-ibba/'
    'IMAGE-metadata/master/rulesets/sample_ruleset.json')

# This is required for authenticating with aiohttp
AUTH = aiohttp.BasicAuth('admin', IMPORT_PASSWORD)

# Get an instance of a logger
logger = logging.getLogger(__name__)


async def get_cdp_etag(session, accession):
    """
    Get etag from CDP using BioSamples ID and material type

    Parameters
    ----------
    session : aiohttp.ClientSession
        a client session object.
    accession : str
        The biosample accession id.

    Raises
    ------
    NotImplementedError
        A status code different from 200 and 404.

    Returns
    -------
    str
        the CDP Etag or None (if not found)
    """

    url = f"{BACKEND_URL}/etag/{accession}/"
    logger.debug(f"GET {url}")

    response = await session.get(url, headers=HEADERS)

    if response.status == 404:
        logger.debug(f"{accession} not in CDP")
        return None

    if response.status == 200:
        record = await parse_json(response, url)
        logger.debug(f"Got data for {accession}")
        return record['etag']

    else:
        message = await response.text()
        logger.error(response.status)
        logger.error(message)
        raise NotImplementedError("Status code not managed")


async def get_all_cdp_etags(session, params=PARAMS):
    """
    Get all CPD etags as a dict

    Parameters
    ----------
    session : aiohttp.ClientSession
        an async session object.
    params : MultiDict, optional
        Specify query parameters. The default is PARAMS.

    Raises
    ------
    ConnectionError
        raised if there are connection issues.

    Returns
    -------
    results : dict
        A dictionary of etags for each BioSamples accessions.
    """

    url = f"{BACKEND_URL}/etag/"
    logger.debug(f"GET {url}")

    # get data for the first time to determine how many pages I have
    # to request
    data, url = await fetch_page(session, url, params)

    logger.debug(f"Got data from {url}")

    # maybe the request had issues
    if data == {}:
        logger.warning("Got a result with no data")
        raise ConnectionError("Can't fetch CDP for accession")

    logger.info("Got %s etags from CDP" % (data['count']))

    # define the results array
    results = dict()

    # ok collect the next tasks
    tasks = []

    # get total page
    totalPages = data['total_pages']

    # generate new awaitable objects. The last page is COMPRISED
    # page 1 is the same of not saying pages in query params.
    for page in range(1, totalPages+1):
        # get a new param object to edit
        my_params = params.copy()

        # edit a multidict object
        my_params.update(page=page)

        # track the new awaitable object
        tasks.append(fetch_page(session, url, my_params))

        # There is no benefit to launching a million requests at once.
        # limit and wait for those before continuing the loop.
        # https://stackoverflow.com/a/54620443
        # TODO: process a batch of tasks or increase page size as a
        # workaround)

    # Run awaitable objects in the aws set concurrently.
    # Return an iterator of Future objects.
    for task in asyncio.as_completed(tasks):
        # read data
        data, url = await task

        logger.debug(f"Got data from {url}")

        # maybe the request had issues
        if data == {}:
            logger.warning(f"Got a result with no data for {url}")
            continue

        # iterate over result once
        for result in data['results']:
            results[result["data_source_id"]] = result["etag"]

    return results


async def post_record(session, record, record_type):
    """
    Post a generic 'record_type' in CPD (new record)

    Parameters
    ----------
    session : aiohttp.ClientSession
        a client session object.
    record : dict
        The CDP record to add.
    record_type : str
        Could be 'organism' or 'specimen'.

    Returns
    -------
    None.
    """

    global AUTH

    url = f'{BACKEND_URL}/{record_type}/'
    logger.debug("POST {accession} {url}".format(
        accession=record["data_source_id"],
        url=url))

    response = await session.post(
        url,
        json=record,
        auth=AUTH)

    if response.status != 201:
        message = await response.text()
        logger.error(message[-200:])


async def put_record(session, biosample_id, record, record_type):
    """
    Put a generic 'record_type' in CPD (update record)

    Parameters
    ----------
    session : aiohttp.ClientSession
        a client session object.
    biosample_id: str
        the BioSamples id I need to update
    record : dict
        The CDP record to add.
    record_type : str
        Could be 'organism' or 'specimen'.

    Returns
    -------
    None.
    """

    global AUTH

    url = f"{BACKEND_URL}/{record_type}/{biosample_id}/"
    logger.debug("PUT {accession} {url}".format(
        accession=record["data_source_id"],
        url=url))

    response = await session.put(
        url,
        json=record,
        auth=AUTH)

    if response.status != 200:
        message = await response.text()
        logger.error(message[-200:])


def get_text_unit_field(sample, biosample_name, field_to_fetch, is_list=False):
    """
    This function will parse text and unit fields in biosamples
    :param sample: sample to parse
    :param biosample_name: name to use in biosample record
    :param field_to_fetch: text or unit to use
    :param is_list: does this record allow to use multiple values
    :return: parsed biosample record
    """
    if is_list:
        tmp = list()
        if biosample_name in sample['characteristics']:
            for item in sample['characteristics'][biosample_name]:
                tmp.append(item[field_to_fetch])
        return tmp
    else:
        if biosample_name in sample['characteristics']:
            return sample['characteristics'][biosample_name][0][field_to_fetch]
        else:
            return ''


def convert_to_underscores(name):
    """
    This function will convert name to underscores_name
    :param name: name to convert
    :return: parsed name
    """
    return "_".join(name.lower().split(" "))


def get_ontology_field(sample, biosample_name, is_list=False):
    """
    This function will parse ontology field in biosamples
    :param sample: sample to parse
    :param biosample_name: name to use in biosample record
    :param is_list: does this record allow to use multiple values
    :return: parsed biosample record
    """
    if is_list:
        tmp = list()
        if biosample_name in sample['characteristics']:
            for item in sample['characteristics'][biosample_name]:
                tmp.append(item['ontologyTerms'][0])
        return tmp
    else:
        if biosample_name in sample['characteristics']:
            return sample['characteristics'][biosample_name][0][
                'ontologyTerms'][0]
        else:
            return ''


def parse_biosample(sample, rules):
    """
    This function will parse biosample record using rules
    :param sample: biosample record
    :param rules: rules for this record
    :param logger: logger instance to write errors
    :return: dict of parsed values
    """

    results = dict()

    for field_type in ['mandatory', 'recommended', 'optional']:
        for field_name in rules[field_type]:
            if field_name in sample['characteristics']:
                biosample_name = field_name

            elif field_name.lower() in sample['characteristics']:
                biosample_name = field_name.lower()

            else:
                cdp_name = convert_to_underscores(field_name)
                if field_name in rules['allow_multiple']:
                    return_value = list()
                else:
                    return_value = ''

                results[cdp_name] = return_value

                if field_name in rules['with_ontology']:
                    results[f'{cdp_name}_ontology'] = return_value

                if field_name in rules['with_units']:
                    results[f'{cdp_name}_unit'] = return_value

                continue

            cdp_name = convert_to_underscores(field_name)
            allow_multiple = field_name in rules['allow_multiple']

            # Should fetch 'text' field only
            if field_name not in rules['with_ontology'] and \
                    field_name not in rules['with_units']:

                results[cdp_name] = get_text_unit_field(
                    sample,
                    biosample_name,
                    'text',
                    allow_multiple)

            # Should fetch 'text' and 'ontology' fields
            if field_name in rules['with_ontology']:
                results[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)

                results[f"{cdp_name}_ontology"] = get_ontology_field(
                    sample, biosample_name, allow_multiple)

            # Should fetch 'text' and 'unit' fields
            if field_name in rules['with_units']:
                results[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)

                results[f"{cdp_name}_unit"] = get_text_unit_field(
                    sample, biosample_name, 'unit', allow_multiple)

    return results


async def get_ruleset(session):
    """
    This function will parse rules from GitHub and return them in dict format
    """

    standard = dict()
    organism = dict()
    specimen = dict()

    logger.debug(f"GET {SAMPLE_RULESET_URL}")

    response = await session.get(SAMPLE_RULESET_URL, headers=HEADERS)

    rules = await parse_json(response, SAMPLE_RULESET_URL, content_type=None)

    for rule_type in rules['rule_groups']:
        results = {
            'mandatory': list(),
            'recommended': list(),
            'optional': list(),
            'with_ontology': list(),
            'with_units': list(),
            'allow_multiple': list()
        }
        for rule in rule_type['rules']:
            if rule['Required'] == 'mandatory':
                results['mandatory'].append(rule['Name'])
            elif rule['Required'] == 'recommended':
                results['recommended'].append(rule['Name'])
            elif rule['Required'] == 'optional':
                results['optional'].append(rule['Name'])

            # Adding rules with ontology id
            if rule['Type'] == 'ontology_id':
                results['with_ontology'].append(rule['Name'])

            # Adding rules with units
            if 'Valid units' in rule:
                results['with_units'].append(rule['Name'])

            # Adding rules with possible multiple values
            if rule['Allow Multiple'] == 'yes' \
                    or rule['Allow Multiple'] == 'max 2':
                results['allow_multiple'].append(rule['Name'])
        if rule_type['name'] == 'standard':
            standard = results
        elif rule_type['name'] == 'organism':
            organism = results
        elif rule_type['name'] == 'specimen from organism':
            specimen = results

    return standard, organism, specimen


class Material(Enum):
    organism = 'organism'
    specimen = 'specimen from organism'


class CDPConverter():
    def __init__(self, standard_rules, organism_rules, specimen_rules):
        self.standard_rules = standard_rules
        self.organism_rules = organism_rules
        self.specimen_rules = specimen_rules

        # defining managed keys
        self.managed = set(['accession', 'characteristics', 'relationships'])
        self.ignored = set([
            '_links',
            'certificates',
            'submittedVia',
            'domain',
            # currently all this keys are ignored
            'name',  # this is my IMAGEID
            'create',
            'release',
            'releaseDate',
            'update',  # HINT: need this field for update (not etag!!!)
            'updateDate',
            'taxId',

        ])

    def check_biosample_attr(self, sample):
        """Test biosample attributes for unmanaged keys

        Parameters
        ----------
        sample : dict
            A BioSamples record.
        """

        for key, value in sample.items():
            if key not in self.managed.union(self.ignored):
                logger.warning(f"Unmanaged key '{key}': {value}")

    def convert_record(self, sample, etag):
        """
        Convert a BioSample record into a CDP record

        Parameters
        ----------
        sample : dict
            A BioSamples record.
        etag : TYPE
            The BioSamples Etag.

        Returns
        -------
        record : dict
            a CDP record.
        """

        self.check_biosample_attr(sample)

        # covert agains standard rules
        record = parse_biosample(sample, self.standard_rules)

        # custom attributes
        record['data_source_id'] = sample['accession']
        record['etag'] = etag

        if record['material'] == 'organism':
            # update record with organism rules
            record.update(parse_biosample(sample, self.organism_rules))

            if 'relationships' in sample:
                child_of = list()
                # specimens are derived from this sample
                specimens = list()

                for relationship in sample['relationships']:
                    if relationship['type'] == 'child of':
                        if 'SAMEA' not in relationship['target']:
                            logger.error(
                                f"{sample['accession']} doesn't "
                                f"have proper name for child of "
                                f"relationship, "
                                f"{relationship['target']} "
                                f"provided")
                            continue

                        child_of.append(relationship['target'])

                    # my specimens are in the source of relationship
                    elif relationship['type'] == 'derived from':
                        if 'SAMEA' not in relationship['source']:
                            logger.error(
                                f"{sample['accession']} doesn't "
                                f"have proper name for derived "
                                f"from relationship, "
                                f"{relationship['source']} "
                                f"provided")
                            continue

                        specimens.append(relationship['source'])

                # add relationship to object
                record['child_of'] = child_of
                record['specimens'] = specimens

            return record

        else:
            # update record for specimen rules
            record.update(parse_biosample(sample, self.specimen_rules))

            if 'relationships' in sample:
                for relationship in sample['relationships']:
                    if relationship['type'] == 'derived from':
                        if 'SAMEA' not in relationship['target']:
                            logger.error(
                                f"{sample['accession']} doesn't "
                                f"have proper name for derived "
                                f"from relationship, "
                                f"{relationship['target']} "
                                f"provided")
                            continue

                        record['derived_from'] = relationship['target']

            return record
