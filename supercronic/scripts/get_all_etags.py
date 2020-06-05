
import sys
import aiohttp
import asyncio
import requests
import logging

from common import rotate_file, ETAG_FILE, PAGE_SIZE

# Global variables
ETAG = []
ETAG_IDS = []

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("get all accession from BioSamples")
    biosample_ids = fetch_biosample_ids()

    logger.info("get all etags from BioSamples")
    asyncio.get_event_loop().run_until_complete(fetch_all_etags(biosample_ids))

    if len(biosample_ids) != len(ETAG_IDS):
        logger.info("Searching for missing IDS")
        for my_id in biosample_ids:
            if my_id not in ETAG_IDS:
                logger.debug(f"Get missing {my_id}")
                resp = requests.get(
                    f"http://www.ebi.ac.uk/biosamples/samples/{my_id}").headers
                if 'ETag' in resp and resp['ETag']:
                    ETAG.append(f"{my_id}\t{resp['ETag']}")


async def fetch_all_etags(ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for my_id in ids:
            task = asyncio.ensure_future(fetch_etag(session, my_id))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


async def fetch_etag(session, my_id):
    url = "http://www.ebi.ac.uk/biosamples/samples/{}".format(my_id)
    resp = await session.get(url)
    etag_value = resp.headers.get('ETag')
    if etag_value:
        ETAG.append("{}\t{}".format(my_id, etag_value))
    ETAG_IDS.append(my_id)


# TODO: implement with async stuff
def fetch_biosample_ids():
    """Return a list of biosample ids for IMAGE project"""

    results = requests.get(
        f"https://www.ebi.ac.uk/biosamples/accessions?"
        f"size={PAGE_SIZE}&filter=attr:project:IMAGE").json()

    accessions = results['_embedded']['accessions']

    while 'next' in results['_links']:
        results = requests.get(results['_links']['next']['href']).json()
        accessions.extend(results['_embedded']['accessions'])

    return accessions


if __name__ == "__main__":
    logger.info("%s started!" % (sys.argv[0]))

    # rotating files
    rotate_file(ETAG_FILE)

    # downloading etags from biosamples
    main()

    # now write into output files
    with open(ETAG_FILE, 'w') as w:
        for item in sorted(ETAG):
            w.write(item + "\n")

    logger.info("%s completed!" % (sys.argv[0]))
