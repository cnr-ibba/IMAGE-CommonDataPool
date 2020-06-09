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
    session : aiohttp.ClientSession, optional
        a client session object.
    accession : str
        The biosample accession id.
    record_type : str
        Could be 'organism' or 'specimen'

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

    return record['etag']


async def post_organism(session, record):
    """Post a single organism"""

    global AUTH

    url = f'{BACKEND_URL}/organism/'
    logger.debug("POST {accession} {url}".format(record["accession"], url))

    response = await session.post(
        url,
        json=record,
        auth=AUTH)

    if response.status != 201:
        logger.error(response.text[-200:])


async def put_organism(session, biosample_id, record):
    """Put a single organism"""

    global AUTH

    url = f"{BACKEND_URL}/organism/{biosample_id}/"
    logger.debug("PUT {accession} {url}".format(record["accession"], url))

    response = await session.put(
        url,
        json=record,
        auth=AUTH)

    if response.status != 200:
        logger.error(response.text[-200:])


async def post_specimen(session, record):
    """post a single specimen"""

    global AUTH

    url = f'{BACKEND_URL}/specimen/'
    logger.debug("POST {accession} {url}".format(record["accession"], url))

    response = await session.post(
        url,
        json=record,
        auth=AUTH)

    if response.status != 201:
        logger.error(response.text[-200:])


async def put_specimen(session, biosample_id, record):
    """Put a single specimen"""

    global AUTH

    url = f"{BACKEND_URL}/specimen/{biosample_id}/"
    logger.debug("PUT {accession} {url}".format(record["accession"], url))

    response = await session.put(
        url,
        json=record,
        auth=AUTH)

    if response.status_code != 200:
        logger.error(response.text[-200:])
