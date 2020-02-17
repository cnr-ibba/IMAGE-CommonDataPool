import json
import requests
import sys
from datetime import date

BACKEND_URL = 'https://www.image2020genebank.eu/data_portal/backend'


def import_data():
    # Read etags from biosamples and CPD
    biosample_etags = read_biosample_etags()
    organism_etags = read_cdp_etags('organism')
    specimen_etags = read_cdp_etags('specimen')

    # Read data from biosamples
    organisms_data = read_data('organisms')
    specimens_data = read_data('specimens')

    # Import all data if CPD is empty
    if organism_etags == {} and specimen_etags == {}:
        for organism in organisms_data:
            requests.post(
                f'{BACKEND_URL}/organism/', json=organism,
                auth=('admin', sys.argv[1]))
        for specimen in specimens_data:
            requests.post(
                f'{BACKEND_URL}/specimen/', json=specimen,
                auth=('admin', sys.argv[1]))
        return

    for biosample_id, etag in biosample_etags.items():
        if biosample_id not in organism_etags and biosample_id \
                not in specimen_etags:
            add_single_record(biosample_id, organisms_data, specimens_data)
        if biosample_id in organism_etags \
                and etag != organism_etags[biosample_id]:
            update_organism_record(biosample_id, organisms_data)
        if biosample_id in specimen_etags \
                and etag != specimen_etags[biosample_id]:
            update_specimen_record(biosample_id, specimens_data)


def add_single_record(biosample_id, organisms_data=None, specimens_data=None):
    """
    This function will add new record to CPD
    :param biosample_id: id of record from biosample
    :param organisms_data: file with organisms data
    :param specimens_data: file with specimens data
    """
    if organisms_data is not None:
        for record in organisms_data:
            if record['data_source_id'] == biosample_id:
                response = requests.post(
                    f'{BACKEND_URL}/organism/', json=record,
                    auth=('admin', sys.argv[1]))

    if specimens_data is not None:
        for record in specimens_data:
            if record['data_source_id'] == biosample_id:
                response = requests.post(
                    f'{BACKEND_URL}/specimen/', json=record,
                    auth=('admin', sys.argv[1]))


def update_organism_record(biosample_id, organisms_data):
    """
    This function will update single record in organism table
    :param biosample_id: id of record from biosample
    :param organisms_data: file with organisms data
    """
    response = requests.delete(f"{BACKEND_URL}/organism/{biosample_id}",
                               auth=('admin', sys.argv[1]))
    add_single_record(biosample_id, organisms_data=organisms_data)


def update_specimen_record(biosample_id, specimens_data):
    """
    This function will update single record in specimens table
    :param biosample_id: id of record from biosample
    :param specimens_data: file with specimens data
    """
    response = requests.delete(f"{BACKEND_URL}/specimen/{biosample_id}")
    add_single_record(biosample_id, specimens_data=specimens_data)


def read_biosample_etags():
    """
    This function will read etags from BioSamples
    :return: dict with etags
    """
    today = date.today().strftime('%Y-%m-%d')
    biosample_etags = dict()
    with open(f"etag_list_{today}.txt", 'r') as f:
        for line in f:
            line = line.rstrip()
            data = line.split("\t")
            biosample_etags[data[0]] = data[1]
    return biosample_etags


def read_cdp_etags(records_type):
    """
    This function will get all etags from CPD
    :param records_type: type of record to parse
    :return: dict with etags
    """
    cdp_etags = dict()
    response = requests.get(
        f"{BACKEND_URL}/{records_type}/?page_size=10000").json()
    while response['next'] is not None:
        for record in response['results']:
            cdp_etags[record['data_source_id']] = record['etag']
        response = requests.get(response['next']).json()
    for record in response['results']:
        cdp_etags[record['data_source_id']] = record['etag']
    return cdp_etags


def read_data(file_type):
    """
    This function will read json file
    :param file_type: might be organisms or specimens
    :return: loaded json file
    """
    file_name = ''
    if file_type == 'organisms':
        file_name = 'organisms.json'
    elif file_type == 'specimens':
        file_name = 'specimens.json'
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    import_data()
