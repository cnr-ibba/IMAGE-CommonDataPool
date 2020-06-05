#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 18:21:19 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import asyncio

from helpers.biosamples import get_biosamples_ids


async def get_accessions():
    accessions = []

    async for accession in get_biosamples_ids():
        accessions.append(accession)

    return accessions


if __name__ == "__main__":
    # get the event loop
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(get_accessions())
    loop.close()

    print(len(data))
