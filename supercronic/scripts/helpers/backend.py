#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:41:54 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import logging
import aiohttp

from decouple import config

from .biosamples import parse_json, HEADERS

BACKEND_URL = 'http://nginx/data_portal/backend'
IMPORT_PASSWORD = config('IMPORT_PASSWORD')

AUTH = aiohttp.BasicAuth('admin', IMPORT_PASSWORD)

# Get an instance of a logger
logger = logging.getLogger(__name__)


async def get_cdp_etag(session, accession, record_type):
    """
    Get etag from CDP using biosample id and material type

    Parameters
    ----------
    session : aiohttp.ClientSessio
        a client session object.
    accession : str
        The biosample accession id.
    record_type : str
        Could be 'organism' or 'specimen'.

    Returns
    -------
    str
        the CDP Etag or None (if not found)
    """

    url = f"{BACKEND_URL}/{record_type}/{accession}/"
    logger.debug(f"GET {url}")

    resp = await session.get(url, headers=HEADERS)

    if resp.status == 404:
        logger.debug(f"{accession} not in CDP")
        return None

    record = await parse_json(resp, url)

    logger.debug(f"Got data for {accession}")

    return record['etag']


async def post_record(session, record, record_type):
    """
    Post a generic 'record_type' in CPD (new record)

    Parameters
    ----------
    session : aiohttp.ClientSessio
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
    session : aiohttp.ClientSessio
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
