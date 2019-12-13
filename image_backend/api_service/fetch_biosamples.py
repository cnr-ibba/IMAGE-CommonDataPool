import requests
import json

SAMPLE_RULESET_URL = 'https://raw.githubusercontent.com/cnr-ibba/' \
                     'IMAGE-metadata/master/rulesets/sample_ruleset.json'


def fetch_biosamples():
    """
    Main function to fet data from biosamples
    """
    # Get rules
    standard_rules, organism_rules, specimen_rules = get_ruleset()

    results = requests.get('https://www.ebi.ac.uk/biosamples/samples'
                           '?size=1000&filter=attr:project:IMAGE').json()
    samples = results['_embedded']['samples']
    results_to_return = list()
    for sample in samples:
        tmp = dict()
        for field_name in standard_rules['mandatory']:
            if field_name in sample['characteristics']:
                biosample_name = field_name
            elif field_name.lower() in sample['characteristics']:
                biosample_name = field_name.lower()
            else:
                print(f"Error: can't find this field {field_name} in sample")
                return
            cdp_name = convert_to_underscores(field_name)
            allow_multiple = field_name in standard_rules['allow_multiple']

            # Should fetch 'text' field only
            if field_name not in standard_rules['with_ontology'] and \
                    field_name not in standard_rules['with_units']:
                tmp[cdp_name] = get_text_unit_field(sample, biosample_name,
                                                    'text', allow_multiple)

            # Should fetch 'text' and 'ontology' fields
            if field_name in standard_rules['with_ontology']:
                tmp[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)
                tmp[f"{cdp_name}_ontology"] = get_ontology_field(
                    sample, biosample_name, allow_multiple)

            # Should fetch 'text' and 'unit' fields
            if field_name in standard_rules['with_units']:
                tmp[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)
                tmp[f"{cdp_name}_unit"] = get_text_unit_field(
                    sample, biosample_name, 'unit', allow_multiple)

        results_to_return.append(tmp)
    return results_to_return


def get_text_unit_field(sample, biosample_name, field_to_fetch, is_list=False):
    if is_list:
        tmp = list()
        for item in sample['characteristics'][biosample_name]:
            tmp.append(item[field_to_fetch])
        return tmp
    else:
        return sample['characteristics'][biosample_name][0][field_to_fetch]


def get_ontology_field(sample, biosample_name, is_list=False):
    if is_list:
        tmp = list()
        for item in sample['characteristics'][biosample_name]:
            tmp.append(item['ontologyTerms'][0])
        return tmp
    else:
        return sample['characteristics'][biosample_name][0]['ontologyTerms'][0]


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
            standard = results
        elif rule_type['name'] == 'organism':
            organism = results
        elif rule_type['name'] == 'specimen from organism':
            specimen = results

    return standard, organism, specimen


def convert_to_underscores(name):
    """
    This function will convert name to underscores_name
    :param name: name to convert
    :return: parsed name
    """
    return "_".join(name.lower().split(" "))


if __name__ == "__main__":
    print(fetch_biosamples()[0])
