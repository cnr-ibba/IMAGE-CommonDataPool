#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:35:50 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import aiohttp
import asyncio
import logging

from yarl import URL
from multidict import MultiDict

from .common import parse_json, HEADERS

# Setting page size for biosample requests
PAGE_SIZE = 500

# define custom parameters
PARAMS = MultiDict([
    ('size', PAGE_SIZE),
    ('filter', 'attr:project:IMAGE'),
])

# limiting the number of connections
# https://docs.aiohttp.org/en/stable/client_advanced.html
CONNECTOR = aiohttp.TCPConnector(limit=10, ttl_dns_cache=300)

# Get an instance of a logger
logger = logging.getLogger(__name__)


async def fetch_page(session, url, params=PARAMS):
    """
    Fetch a generic url, read data as json and return a promise

    Parameters
    ----------
    session : aiohttp.ClientSession
        an async session object.
    url : str
        the desidered url. The default is BIOSAMPLE_URL.
    params : MultiDict, optional
        Additional params for request. The default is BIOSAMPLE_PARAMS.

    Returns
    -------
    dict
        json content of the page

    """
    """"""

    # define a URL with yarl
    url = URL(url)
    url = url.update_query(params)

    logger.debug(f"GET {url}")

    try:
        async with session.get(url, headers=HEADERS) as response:
            # try to read json data
            return await parse_json(response, url)

    except aiohttp.client_exceptions.ServerDisconnectedError as exc:
        logger.error(repr(exc))
        logger.warning(
            "server disconnected during %s" % url)
        return {}


async def get_biosamples_ids(session, params=PARAMS):
    """


    Parameters
    ----------
    session : aiohttp.ClientSession
        an async session object.
    params : MultiDict, optional
        Specify query parameters. The default is PARAMS.

    Raises
    ------
    ConnectionError
        raised if there are connection issues

    Yields
    ------
    accession : str
        a BioSample ID.

    """

    url = "https://www.ebi.ac.uk/biosamples/accessions"

    # get data for the first time to determine how many pages I have
    # to request
    data = await fetch_page(session, url, params)

    # maybe the request had issues
    if data == {}:
        logger.debug("Got a result with no data")
        raise ConnectionError("Can't fetch biosamples for accession")

    for accession in data['_embedded']['accessions']:
        yield accession

    tasks = []

    # get pages # debug
    totalPages = 2  # data['page']['totalPages']

    # generate new awaitable objects
    for page in range(1, totalPages):
        # get a new param object to edit
        my_params = params.copy()

        # edit a multidict object
        my_params.update(page=page)

        # track the new awaitable object
        tasks.append(fetch_page(session, url, my_params))

    # Run awaitable objects in the aws set concurrently.
    # Return an iterator of Future objects.
    for task in asyncio.as_completed(tasks):
        # read data
        data = await task

        # maybe the request had issues
        if data == {}:
            logger.debug("Got a result with no data for accession")
            continue

        for accession in data['_embedded']['accessions']:
            yield accession


async def get_biosample_record(accession, session):
    """
    Get a biosample record from a BioSample id

    Parameters
    ----------
    accession : str
        The biosample accession id.
    session : aiohttp.ClientSession, optional
        a client session object. The default is SESSION.

    Returns
    -------
    record : dict
        the BioSample record
    etag : str
        The etag value read from response header.

    """

    url = "https://www.ebi.ac.uk/biosamples/samples/{}".format(accession)
    logger.debug(f"GET {url}")

    resp = await session.get(url, headers=HEADERS)
    record = await parse_json(resp, url)

    etag = resp.headers.get('ETag')
    return record, etag
