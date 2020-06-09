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

from fetch_biosamples import get_ruleset, parse_biosample

from helpers.biosamples import (
    get_biosamples_ids, CONNECTOR as EBI_CONNECTOR, get_biosample_record)
from helpers.backend import get_cdp_etag, post_record, put_record

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

standard_rules, organism_rules, specimen_rules = None, None, None


def convert_record(sample, etag):
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
    global standard_rules, organism_rules, specimen_rules

    # covert agains standard rules
    record = parse_biosample(sample, standard_rules)

    # custom attributes
    record['data_source_id'] = sample['accession']
    record['etag'] = etag

    if record['material'] == 'organism':
        tmp_results = parse_biosample(sample, organism_rules)
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
        tmp_results = parse_biosample(sample, specimen_rules)
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


async def process_record(accession, ebi_session, cdp_session):
    record, ebi_etag = await get_biosample_record(accession, ebi_session)
    # logger.debug("%s,%s,%s" % (accession, record, etag))

    # determine material
    try:
        material = record["characteristics"]["material"][0]["text"]
    except KeyError as exc:
        logger.error("Cannot find material")
        logger.error(str(record))
        raise exc

    # check CDP record
    if material == 'organism':
        record_type = "organism"

    elif material == 'specimen from organism':
        record_type = "specimen"

    else:
        raise NotImplementedError(f"Material '{material}' not implemented")

    logger.debug(
        f'Search for {accession} ({record_type}) in CDP')

    # get info from CDP
    cdp_etag = await get_cdp_etag(cdp_session, accession, record_type)

    logger.debug(
        f"Check etags for {accession}: Biosample {ebi_etag}, CDP {cdp_etag}")

    if cdp_etag is None:
        # new insert
        logger.debug(f"Creating {accession}")

        await post_record(
            cdp_session,
            convert_record(record, ebi_etag),
            record_type)

    elif cdp_etag != ebi_etag:
        # make update to CDP
        logger.debug(f"Tags differ: Update {accession}")

        await put_record(
            cdp_session,
            accession,
            convert_record(record, ebi_etag),
            record_type)

    else:
        logger.debug(f"Etags are equal. Ignoring {accession}")

    return accession, ebi_etag


async def main():
    async with aiohttp.ClientSession(connector=EBI_CONNECTOR) as ebi_session:
        async with aiohttp.ClientSession() as cdp_session:

            tasks = []
            async for accession in get_biosamples_ids(ebi_session):
                # process a BioSamples record
                task = asyncio.create_task(
                    process_record(accession, ebi_session, cdp_session)
                )

                # append task
                tasks.append(task)

            # await for tasks completion
            for task in asyncio.as_completed(tasks):
                accession, etag = await task
                logger.debug(f"{accession} ({etag}) completed!")


if __name__ == "__main__":
    logger.info(f"{sys.argv[0]} started")

    # Get rules
    logger.info("Getting ruleset")
    standard_rules, organism_rules, specimen_rules = get_ruleset()

    # get the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    logger.info(f"{sys.argv[0]} completed")
