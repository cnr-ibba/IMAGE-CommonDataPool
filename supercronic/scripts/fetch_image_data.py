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

from enum import Enum

from helpers.biosamples import (
    get_biosamples_ids, CONNECTOR as EBI_CONNECTOR, get_biosample_record)
from helpers.backend import (
    get_cdp_etag, post_record, put_record, CDPConverter, get_ruleset, Material,
    CONNECTOR as CDP_CONNECTOR)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Operation(Enum):
    ignored = 'ignored'
    created = 'created'
    updated = 'updated'
    error = 'error'


async def process_record(accession, ebi_session, cdp_session, converter):
    """
    Process a single BioSamples accession (BioSample ID): check etags
    in both BioSamples and CDP and if necessary CREATE/UPDATE record

    Parameters
    ----------
    accession : str
        The BioSamples ID.
    ebi_session : aiohttp.ClientSession
        a client session specific for EBI (with limits defined).
    cdp_session : aiohttp.ClientSession
        a client session specific for CDP.
    converter : CDPConverter
        a CDPConverter instance for data conversion.

    Returns
    -------
    operation : Operation
        created or updated if creating or updating an object. Ignored when
        there's nothing to do.
    accession : str
        The processed The BioSamples ID (needed when collecting tasks).
    ebi_etag : str
        the BioSamples etag header attribute.
    """

    record, ebi_etag = await get_biosample_record(accession, ebi_session)

    # determine material
    try:
        material = Material(record["characteristics"]["material"][0]["text"])

    except KeyError as exc:
        logger.error(
            f"Cannot find material for {accession}: {record['message']}")
        logger.debug("Missing key %s" % str(exc))
        return Operation.error, accession, record

    logger.debug(
        f'Search for {accession} ({material.name}) in CDP')

    # get info from CDP
    cdp_etag = await get_cdp_etag(cdp_session, accession, material.name)

    logger.debug(
        f"Check etags for {accession}: Biosample {ebi_etag}, CDP {cdp_etag}")

    # default operation
    operation = Operation.ignored

    if cdp_etag is None:
        # new insert
        logger.debug(f"Creating {accession}")
        operation = Operation.created

        await post_record(
            cdp_session,
            # convert BioSamples data into CDP format
            converter.convert_record(record, ebi_etag),
            material.name)

    elif cdp_etag != ebi_etag:
        # make update to CDP
        logger.debug(f"Tags differ: Update {accession}")
        operation = Operation.updated

        await put_record(
            cdp_session,
            accession,
            # convert BioSamples data into CDP format
            converter.convert_record(record, ebi_etag),
            material.name)

    else:
        logger.debug(f"Etags are equal. Ignoring {accession}")

    return operation, accession, ebi_etag


async def check_task_complete(task):
    """
    Await for task completion and print messages to console

    Parameters
    ----------
    task : asyncio.Task
        A task create with process_record function

    Returns
    -------
    None.

    """
    operation, accession, etag = await task

    if operation == Operation.ignored:
        logger.debug(
            f"Sample {accession} ({etag}) {operation.value}!"
        )

    elif operation in (Operation.created, Operation.updated):
        logger.info(
            f"Sample {accession} ({etag}) {operation.value}!"
        )

    else:
        logger.error(
            f"{operation.value} for {accession} "
            f"({etag['error']}): is this a private sample?"
        )


async def main():
    """
    Main function for asyncio loop

    Returns
    -------
    None.
    """

    # limiting the number of request sent to backend
    async with aiohttp.ClientSession(
            connector=CDP_CONNECTOR) as cdp_session:

        # Get rules from github
        logger.info("Getting ruleset")
        ruleset_task = asyncio.create_task(get_ruleset(cdp_session))

        # limiting the number of request sent to EBI
        async with aiohttp.ClientSession(
                connector=EBI_CONNECTOR) as ebi_session:

            # get results from github
            # HINT: could this be synchronous?
            standard_rules, organism_rules, specimen_rules = await ruleset_task

            # create a new CDPConverter instance for using IMAGE ruleset
            converter = CDPConverter(
                standard_rules,
                organism_rules,
                specimen_rules)

            # collect annotation task
            tasks = []
            counter = 0

            # go through biosample ids. async generator is not an iterable!
            async for accession in get_biosamples_ids(ebi_session):
                # process a BioSamples record
                task = asyncio.create_task(
                    process_record(
                        accession,
                        ebi_session,
                        cdp_session,
                        converter)
                )

                # append task
                tasks.append(task)
                counter += 1

                # There is no benefit to launching a million requests at once.
                # limit and wait for those before continuing the loop.
                # https://stackoverflow.com/a/54620443
                if (counter) % 100 == 0:
                    logger.debug(
                        "Completing a batch of tasks starting from %s" % (
                            counter-100)
                    )

                    for task in asyncio.as_completed(tasks):
                        await check_task_complete(task)

                    # reset task list
                    tasks = []

            # await for tasks completion (for remaining task)
            if len(tasks) > 0:
                logger.debug("Completing the remaining tasks")

                for task in asyncio.as_completed(tasks):
                    await check_task_complete(task)


if __name__ == "__main__":
    logger.info(f"{sys.argv[0]} started")

    # get the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    logger.info(f"{sys.argv[0]} completed")
