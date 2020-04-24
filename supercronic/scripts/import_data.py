import json
import logging
import requests

from decouple import config

from common import ETAG_FILE, PAGE_SIZE

BACKEND_URL = 'http://nginx/data_portal/backend'
IMPORT_PASSWORD = config('IMPORT_PASSWORD')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def import_data():
    # Read etags from biosamples and CPD
    biosample_etags = read_biosample_etags()
    organism_etags = read_cdp_etags('organism')
    specimen_etags = read_cdp_etags('specimen')

    # Read data from biosamples
    organisms_data, organisms_idx = read_data('organisms')
    specimens_data, specimens_idx = read_data('specimens')

    # Import all data if CPD is empty
    if organism_etags == {} and specimen_etags == {}:
        for organism in organisms_data:
            requests.post(
                f'{BACKEND_URL}/organism/', json=organism,
                auth=('admin', IMPORT_PASSWORD))
        for specimen in specimens_data:
            requests.post(
                f'{BACKEND_URL}/specimen/', json=specimen,
                auth=('admin', IMPORT_PASSWORD))
        return

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
            logger.info("Update organism: %s" % biosample_id)
            update_organism_record(
                biosample_id,
                organisms_data,
                organisms_idx)

        elif biosample_id in specimen_etags \
                and etag != specimen_etags[biosample_id]:
            logger.info("Update specimen: %s" % biosample_id)
            update_specimen_record(
                biosample_id,
                specimens_data,
                specimens_idx)


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
        response = requests.post(
            f'{BACKEND_URL}/organism/', json=record,
            auth=('admin', IMPORT_PASSWORD))

        if response.status_code != 201:
            logger.error(response.text)


    if specimens_data is not None and biosample_id in specimens_idx:
        # get positions from dict indexes
        idx = specimens_idx[biosample_id]
        record = specimens_data[idx]
        logger.debug(f"Loading {biosample_id}")
        response = requests.post(
            f'{BACKEND_URL}/specimen/', json=record,
            auth=('admin', IMPORT_PASSWORD))

        if response.status_code != 201:
            logger.error(response.text)


def update_organism_record(biosample_id, organisms_data, organisms_idx):
    """
    This function will update single record in organism table
    :param biosample_id: id of record from biosample
    :param organisms_data: file with organisms data
    :param organisms_idx: dictionary with biosample_id -> position
    """
    response = requests.delete(f"{BACKEND_URL}/organism/{biosample_id}",
                               auth=('admin', IMPORT_PASSWORD))

    if response.status_code != 202:
        logger.error(response.text)

    add_single_record(
        biosample_id,
        organisms_data=organisms_data,
        organisms_idx=organisms_idx)


def update_specimen_record(biosample_id, specimens_data, specimens_idx):
    """
    This function will update single record in specimens table
    :param biosample_id: id of record from biosample
    :param specimens_data: file with specimens data
    :param specimens_idx: dictionary with biosample_id -> position
    """
    response = requests.delete(f"{BACKEND_URL}/specimen/{biosample_id}")

    if response.status_code != 202:
        logger.error(response.text)

    add_single_record(
        biosample_id,
        specimens_data=specimens_data,
        specimens_idx=specimens_idx)


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
    cdp_etags = dict()
    response = requests.get(
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
    # now import data
    import_data()
