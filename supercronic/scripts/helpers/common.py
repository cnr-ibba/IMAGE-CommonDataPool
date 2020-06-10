#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:50:45 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import aiohttp
import logging

from yarl import URL
from multidict import MultiDict

HEADERS = {
    'Accept': 'application/json',
}

# An empty dictionary for params
PARAMS = MultiDict([])


# Get an instance of a logger
logger = logging.getLogger(__name__)


async def parse_json(response, url, content_type='application/json'):
    """Helper function to parse json data"""

    logger.debug(f"Got response from {url}")

    try:
        return await response.json(content_type=content_type)

    except aiohttp.client_exceptions.ContentTypeError as exc:
        logger.error(repr(exc))
        logger.warning(
            "error while getting data from %s" % url)
        return {}


async def fetch_page(session, url, params=PARAMS):
    """
    Fetch a generic url, read data as json and return a promise

    Parameters
    ----------
    session : aiohttp.ClientSession
        an async session object.
    url : str
        the desidered url.
    params : MultiDict, optional
        Additional params for request. The default is PARAMS.

    Returns
    -------
    data : dict
        Json content of the page
    url : str
        The requested URL (for debugging purposes)
    """

    # define a URL with yarl
    url = URL(url)
    url = url.update_query(params)

    logger.debug(f"GET {url}")

    try:
        async with session.get(url, headers=HEADERS) as response:
            # try to read json data
            data = await parse_json(response, url)
            return data, url

    except aiohttp.client_exceptions.ServerDisconnectedError as exc:
        logger.error(repr(exc))
        logger.warning(
            "server disconnected during %s" % url)
        return {}, url
