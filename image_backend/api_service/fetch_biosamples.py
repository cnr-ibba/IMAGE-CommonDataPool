import requests
import json

SAMPLE_RULESET_URL = 'https://raw.githubusercontent.com/cnr-ibba/' \
                     'IMAGE-metadata/master/rulesets/sample_ruleset.json'


def fetch_biosamples():
    """
    Main function to fet data from biosamples
    """
    standard_rules, organism_rules, specimen_rules = get_ruleset()

    results = requests.get('https://www.ebi.ac.uk/biosamples/samples'
                           '?size=1000&filter=attr:project:IMAGE').json()
    samples = results['_embedded']['samples']
    return samples


def get_ruleset():
    """
    This function will parse rules from GitHub and return them in dict format
    """
    standard = dict()
    organism = dict()
    specimen = dict()
    rules = requests.get(SAMPLE_RULESET_URL).json()
    for rule_type in rules['rule_groups']:
        results = {
            'mandatory': list(),
            'recommended': list(),
            'optional': list(),
            'with_ontology': list(),
            'with_units': list(),
            'allow_multiple': list()
        }
        for rule in rule_type['rules']:
            if rule['Required'] == 'mandatory':
                results['mandatory'].append(rule['Name'])
            elif rule['Required'] == 'recommended':
                results['recommended'].append(rule['Name'])
            elif rule['Required'] == 'optional':
                results['optional'].append(rule['Name'])

            # Adding rules with ontology id
            if rule['Type'] == 'ontology_id':
                results['with_ontology'].append(rule['Name'])

            # Adding rules with units
            if 'Valid units' in rule:
                results['with_units'].append(rule['Name'])

            # Adding rules with possible multiple values
            if rule['Allow Multiple'] == 'yes':
                results['allow_multiple'].append(rule['Name'])
        if rule_type['name'] == 'standard':
            print('Standard')
            standard = results
            print(json.dumps(standard))
        elif rule_type['name'] == 'organism':
            print('Organism')
            organism = results
            print(json.dumps(organism))
        elif rule_type['name'] == 'specimen from organism':
            print('Specimen')
            specimen = results
            print(json.dumps(specimen))

    return standard, organism, specimen


if __name__ == "__main__":
    fetch_biosamples()
