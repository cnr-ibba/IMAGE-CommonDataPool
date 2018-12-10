import json
import requests
import sys


def import_data():
    organisms_data = read_data('organisms')
    specimens_data = read_data('specimens')
    for organism in organisms_data:
        requests.post('http://localhost:8000/api/backend/organism/', json=organism, auth=('admin', sys.argv[1]))
    for specimen in specimens_data:
        requests.post('http://localhost:8000/api/backend/specimen/', json=specimen, auth=('admin', sys.argv[1]))


def read_data(file_type):
    file_name = ''
    if file_type == 'organisms':
        file_name = 'organisms.test_data.json'
    elif file_type == 'specimens':
        file_name = 'specimens.test_data.json'
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    import_data()
