#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:41:54 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import logging
import aiohttp

from enum import Enum
from decouple import config

from .common import parse_json, HEADERS

# limiting the number of connections
# https://docs.aiohttp.org/en/stable/client_advanced.html
CONNECTOR = aiohttp.TCPConnector(limit=20, ttl_dns_cache=300)

BACKEND_URL = 'http://nginx/data_portal/backend'
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
        logger.error(response.status)
        logger.error(response.text)
        raise NotImplementedError("Status code not managed")


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
        logger.error(response.text[-200:])


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
        logger.error(response.text[-200:])


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

        # covert agains standard rules
        record = parse_biosample(sample, self.standard_rules)

        # custom attributes
        record['data_source_id'] = sample['accession']
        record['etag'] = etag

        if record['material'] == 'organism':
            tmp_results = parse_biosample(sample, self.organism_rules)
            record['organisms'] = [tmp_results]

            if 'relationships' in sample:
                relationships = list()
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

                        relationships.append(relationship['target'])
                record['organisms'][0]['child_of'] = relationships

            return record

        else:
            tmp_results = parse_biosample(sample, self.specimen_rules)
            record['specimens'] = [tmp_results]

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

                        record['specimens'][0]['derived_from'] = \
                            relationship['target']

            return record
