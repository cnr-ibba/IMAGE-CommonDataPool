import json
import logging
import requests
import argparse

from decouple import config

from common import ETAG_FILE, PAGE_SIZE

BACKEND_URL = 'http://nginx/data_portal/backend'
IMPORT_PASSWORD = config('IMPORT_PASSWORD')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# a global variables
SESSION = None


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Upload IMAGE data in Common Data Pool')
    )

    parser.add_argument(
        "--force",
        help="Force data upload (overwrite data if exists)",
        action='store_true'
    )

    parser.add_argument(
        "-u",
        "--user",
        help="User id",
        default='admin'
    )

    parser.add_argument(
        "-p",
        "--password",
        help="User password",
        default=IMPORT_PASSWORD
    )

    return parser.parse_args()


def post_organism(record):
    """Post a single organism"""

    global SESSION

    logger.debug(record)

    response = SESSION.post(f'{BACKEND_URL}/organism/', json=record)

    if response.status_code != 201:
        logger.error(response.text[-200:])


def put_organism(biosample_id, record):
    """Put a single organism"""

    global SESSION

    logger.debug(record)

    url = f"{BACKEND_URL}/organism/{biosample_id}/"

    response = SESSION.put(url, json=record)

    if response.status_code != 200:
        logger.error(response.text[-200:])


def post_specimen(record):
    """post a single specimen"""

    global SESSION

    response = SESSION.post(f'{BACKEND_URL}/specimen/', json=record)

    if response.status_code != 201:
        logger.error(response.text[-200:])


def put_specimen(biosample_id, record):
    """Put a single specimen"""

    global SESSION

    logger.debug(record)

    url = f"{BACKEND_URL}/specimen/{biosample_id}/"

    response = SESSION.put(url, json=record)

    if response.status_code != 200:
        logger.error(response.text[-200:])


def import_data(force=False):
    # Read etags from biosamples and CPD
    biosample_etags = read_biosample_etags()
    organism_etags = read_cdp_etags('organism')
    specimen_etags = read_cdp_etags('specimen')

    # Read data from biosamples
    organisms_data, organisms_idx = read_data('organisms')
    specimens_data, specimens_idx = read_data('specimens')

    # Import all data if CPD is empty
    if organism_etags == {} and specimen_etags == {}:
        logger.info("Loading data into empty CDP")

        for organism in organisms_data:
            post_organism(organism)

        for specimen in specimens_data:
            post_specimen(specimen)

        return

    if force:
        # erase etags from CDP in order to simulate a full update
        logger.warning("Forcing CDP update")
        organism_etags = {k: '' for k in organism_etags.keys()}
        specimen_etags = {k: '' for k in specimen_etags.keys()}

    for biosample_id, etag in biosample_etags.items():
        if biosample_id not in organism_etags and biosample_id \
                not in specimen_etags:
            logger.debug("Got a new BioSamples: %s" % biosample_id)
            add_single_record(
                biosample_id,
                organisms_data,
                organisms_idx,
                specimens_data,
                specimens_idx)

        elif biosample_id in organism_etags \
                and etag != organism_etags[biosample_id]:
            logger.debug("Update organism: %s" % biosample_id)
            update_organism_record(
                biosample_id,
                organisms_data,
                organisms_idx)

        elif biosample_id in specimen_etags \
                and etag != specimen_etags[biosample_id]:
            logger.debug("Update specimen: %s" % biosample_id)
            update_specimen_record(
                biosample_id,
                specimens_data,
                specimens_idx)

    logger.info("Data import completed")


def add_single_record(
        biosample_id, organisms_data=None, organisms_idx=None,
        specimens_data=None, specimens_idx=None):
    """
    This function will add new record to CPD
    :param biosample_id: id of record from biosample
    :param organisms_data: file with organisms data
    :param organisms_idx: dictionary with biosample_id -> position
    :param specimens_data: file with specimens data
    :param specimens_idx: dictionary with biosample_id -> position
    """

    if organisms_data is not None and biosample_id in organisms_idx:
        # get positions from dict indexes
        idx = organisms_idx[biosample_id]
        record = organisms_data[idx]
        logger.debug(f"Loading {biosample_id}")
        post_organism(record)

    if specimens_data is not None and biosample_id in specimens_idx:
        # get positions from dict indexes
        idx = specimens_idx[biosample_id]
        record = specimens_data[idx]
        logger.debug(f"Loading {biosample_id}")
        post_specimen(record)


def update_organism_record(biosample_id, organisms_data, organisms_idx):
    """
    This function will update single record in organism table
    :param biosample_id: id of record from biosample
    :param organisms_data: file with organisms data
    :param organisms_idx: dictionary with biosample_id -> position
    """

    # get positions from dict indexes
    idx = organisms_idx[biosample_id]
    record = organisms_data[idx]
    logger.info(f"Update {biosample_id}")

    put_organism(biosample_id, record)


def update_specimen_record(biosample_id, specimens_data, specimens_idx):
    """
    This function will update single record in specimens table
    :param biosample_id: id of record from biosample
    :param specimens_data: file with specimens data
    :param specimens_idx: dictionary with biosample_id -> position
    """

    # get positions from dict indexes
    idx = specimens_idx[biosample_id]
    record = specimens_data[idx]
    logger.info(f"Update {biosample_id}")

    put_specimen(biosample_id, record)


def read_biosample_etags():
    """
    This function will read etags from BioSamples
    :return: dict with etags
    """

    biosample_etags = dict()

    with open(ETAG_FILE, 'r') as f:
        for line in f:
            line = line.rstrip()
            data = line.split("\t")
            biosample_etags[data[0]] = data[1]

    logger.info("Got %s etags from BioSamples" % (len(biosample_etags)))

    return biosample_etags


def read_cdp_etags(records_type):
    """
    This function will get all etags from CPD
    :param records_type: type of record to parse
    :return: dict with etags
    """

    global SESSION

    cdp_etags = dict()
    response = SESSION.get(
        f"{BACKEND_URL}/{records_type}/"
        f"?page_size={PAGE_SIZE}&ordering=data_source_id").json()

    while response['next'] is not None:
        for record in response['results']:
            cdp_etags[record['data_source_id']] = record['etag']
        response = requests.get(response['next']).json()

    for record in response['results']:
        cdp_etags[record['data_source_id']] = record['etag']

    logger.info("Got %s etags from CPD for %s" % (
        len(cdp_etags), records_type))

    return cdp_etags


def read_data(file_type):
    """
    This function will read json file
    :param file_type: might be organisms or specimens
    :return: loaded json file and index dictionary
    """

    file_name = ''

    if file_type == 'organisms':
        file_name = 'organisms.json'

    elif file_type == 'specimens':
        file_name = 'specimens.json'

    with open(file_name, 'r') as f:
        data = json.load(f)

    data_idx = dict()

    # data is a list, cicle along items and get a dict of indexes
    for i, item in enumerate(data):
        data_idx[item['data_source_id']] = i

    logger.info("Read %s record from %s" % (len(data), file_type))

    return data, data_idx


if __name__ == "__main__":
    # search for arguments
    args = parse_args()

    # start a session with CDP
    SESSION = requests.Session()
    SESSION.auth = (args.user, args.password)

    # now import data
    import_data(args.force)
