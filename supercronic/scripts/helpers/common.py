#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:50:45 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import aiohttp
import logging

HEADERS = {
    'Accept': 'application/json',
}

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
