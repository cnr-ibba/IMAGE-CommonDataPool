#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 18:21:19 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import sys
import asyncio
import aiohttp
import logging

from helpers.biosamples import (
    get_biosamples_ids, CONNECTOR as EBI_CONNECTOR, get_biosample_record)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def process_record(accession, session):
    record, etag = await get_biosample_record(accession, session)
    # logger.debug("%s,%s,%s" % (accession, record, etag))
    logger.debug(
        f'{accession}:{record["characteristics"]["material"][0]["text"]}')
    return accession, etag


async def main():
    async with aiohttp.ClientSession(connector=EBI_CONNECTOR) as session:
        tasks = []
        async for accession in get_biosamples_ids(session):
            # TODO: process a BioSamples record
            task = asyncio.create_task(
                process_record(accession, session)
            )

            # append task
            tasks.append(task)

        # await for tasks completion
        for task in asyncio.as_completed(tasks):
            accession, etag = await task
            logger.info(f"{accession},{etag} completed!")


if __name__ == "__main__":
    logger.info(f"{sys.argv[0]} started")

    # get the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    logger.info(f"{sys.argv[0]} completed")
