import json
import requests


def import_data():
    organisms_data = read_data('organisms')
    specimens_data = read_data('specimens')
    for organism in organisms_data:
        requests.post('http://localhost:8000/backend/organism/', json=organism)
    for specimen in specimens_data:
        requests.post('http://localhost:8000/backend/specimen/', json=specimen)


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
