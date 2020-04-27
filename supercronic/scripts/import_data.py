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
SPECIES2COMMON = dict()
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

    # ok, try to fill DADIS link table
    dadis_data = fill_dadis(record)

    # update record
    if dadis_data:
        record['organisms'][0]['dadis'] = dadis_data

    logger.debug(record)

    response = SESSION.post(f'{BACKEND_URL}/organism/', json=record)

    if response.status_code != 201:
        # logger.error(response.text)
        logger.error(record)
        raise Exception(response.text[-200:])


def post_specimen(record):
    """post a single specimen"""

    global SESSION

    response = SESSION.post(f'{BACKEND_URL}/specimen/', json=record)

    if response.status_code != 201:
        logger.error(response.text)


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

    global SESSION

    response = SESSION.delete(f"{BACKEND_URL}/organism/{biosample_id}")

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

    global SESSION

    response = SESSION.delete(f"{BACKEND_URL}/specimen/{biosample_id}")

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


# a function to get the list of common species from data_portal
def get_species2commonname():
    global SESSION

    response = SESSION.get(BACKEND_URL + '/species/')

    if response.status_code != 200:
        raise Exception(response.text)

    species2commonnames = dict()

    for item in response.json():
        scientific_name = item['scientific_name']
        common_name = item['common_name']

        species2commonnames[scientific_name] = common_name

    return species2commonnames


def fill_dadis(record):
    global SPECIES2COMMON, SESSION

    scientific_name = record['species']

    if scientific_name not in SPECIES2COMMON:
        # this species hasn't a coorrespondance in species tables, so
        # I can't provide a link for dadis
        logger.error(f"'{scientific_name}' is not modelled for DADIS")
        return

    common_name = SPECIES2COMMON[scientific_name]

    # contruct a species dictionary
    species = {
        'common_name': common_name,
        'scientific_name': scientific_name}

    # now create a dictionary for my object
    data = {
        'species': species,
        'supplied_breed': record['organisms'][0]['supplied_breed'],
        'efabis_breed_country': record['organisms'][0]['efabis_breed_country']
    }

    # check if record exists
    response = SESSION.get(BACKEND_URL + "/dadis_link/", params=data)

    dadis_data = None

    if response.json()['count'] == 0:
        response = SESSION.post(
            BACKEND_URL + '/dadis_link/',
            json=data)

        if response.status_code != 201:
            raise Exception(f"Cannot set {data}")

        else:
            logger.debug(f"{data} added to CDP")
            dadis_data = response.json()

    elif response.json()['count'] == 1:
        logger.debug(f"{data} already in CDP")
        dadis_data = response.json()['results'][0]

    else:
        raise Exception(response.json())

    # return dadis data to complete organism insert
    logger.debug(dadis_data)

    return dadis_data


if __name__ == "__main__":
    # search for arguments
    args = parse_args()

    # start a session with CDP
    SESSION = requests.Session()
    SESSION.auth = (args.user, args.password)

    # get species to common names
    SPECIES2COMMON = get_species2commonname()

    # now import data
    import_data(args.force)
