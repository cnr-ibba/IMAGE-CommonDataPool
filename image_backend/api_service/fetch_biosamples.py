import requests
import json
import logging
from datetime import date

SAMPLE_RULESET_URL = 'https://raw.githubusercontent.com/cnr-ibba/' \
                     'IMAGE-metadata/master/rulesets/sample_ruleset.json'
DAD_IS_BREEDS = ['Gouwenaar', 'Havana', 'Ekster', 'Hulstlander konijn',
                 'Beige', 'Sallander', 'Deilenaar', 'Thrianta konijn',
                 'Twentse landgans', 'Stabijhoun', 'Wetterhoun',
                 'Hulstlander', 'Thrianta', 'Flevolander']


def fetch_biosamples():
    """
    Main function to fet data from biosamples
    """
    new_logger = logging.getLogger('fetch_biosamples')
    today = date.today().strftime('%Y-%m-%d')
    f_handler = logging.FileHandler(f"fetch_biosamples_{today}.log")
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - line %(lineno)s - '
        '%(message)s', datefmt='%y-%b-%d %H:%M:%S')
    f_handler.setFormatter(f_format)
    new_logger.addHandler(f_handler)
    new_logger.setLevel(logging.INFO)
    # Get rules
    standard_rules, organism_rules, specimen_rules = get_ruleset()
    etags = read_etags()

    results = requests.get('https://www.ebi.ac.uk/biosamples/samples'
                           '?size=1000000&filter=attr:project:IMAGE').json()
    samples = results['_embedded']['samples']
    organisms = list()
    specimens = list()
    for sample in samples:
        errors = dict()
        errors_organism = dict()
        tmp_results, errors = parse_biosample(sample, standard_rules)
        tmp = tmp_results
        tmp['data_source_id'] = sample['accession']
        tmp['etag'] = etags[sample['accession']]
        if tmp['material'] == 'organism':
            tmp_results, errors_organism = parse_biosample(sample,
                                                           organism_rules)
            tmp['organisms'] = [tmp_results]
            if 'relationships' in sample:
                relationships = list()
                for relationship in sample['relationships']:
                    if relationship['type'] == 'child of':
                        if 'SAMEA' not in relationship['target']:
                            new_logger.error(f"{sample['accession']} doesn't "
                                             f"have proper name for child of "
                                             f"relationship, "
                                             f"{relationship['target']} "
                                             f"provided")
                            continue
                        relationships.append(relationship['target'])
                tmp['organisms'][0]['child_of'] = relationships
            organisms.append(tmp)
        else:
            tmp_results, _ = parse_biosample(sample, specimen_rules)
            tmp['specimens'] = [tmp_results]
            if 'relationships' in sample:
                for relationship in sample['relationships']:
                    if relationship['type'] == 'derived from':
                        if 'SAMEA' not in relationship['target']:
                            new_logger.error(f"{sample['accession']} doesn't "
                                             f"have proper name for derived "
                                             f"from relationship, "
                                             f"{relationship['target']} "
                                             f"provided")
                            continue
                        tmp['specimens'][0]['derived_from'] = \
                            relationship['target']
            specimens.append(tmp)
        if 'species' in errors and 'supplied_breed' in errors_organism:
            new_logger.error(f"For country: \""
                             f"{errors_organism['efabis_breed_country']}\", "
                             f"species: \"{errors['species']}\" and "
                             f"breed: \"{errors_organism['supplied_breed']}\" "
                             f"there is no record in dad-is database")
    return organisms, specimens


def read_etags():
    """
    This function will read etag_list_{currend_date} file generated by
    get_all_etags script and put data in a dict
    :return: dict with biosample ids as keys and etags as values
    """
    results_to_return = dict()
    today = date.today().strftime('%Y-%m-%d')
    with open(f"etag_list_{today}.txt", 'r') as f:
        for line in f:
            line = line.rstrip()
            data = line.split("\t")
            results_to_return[data[0]] = data[1]
    return results_to_return


def parse_biosample(sample, rules):
    """
    This function will parse biosample record using rules
    :param sample: biosample record
    :param rules: rules for this record
    :param logger: logger instance to write errors
    :return: dict of parsed values
    """
    results = dict()
    errors = dict()
    for field_type in ['mandatory', 'recommended', 'optional']:
        for field_name in rules[field_type]:
            if field_name in sample['characteristics']:
                biosample_name = field_name
            elif field_name.lower() in sample['characteristics']:
                biosample_name = field_name.lower()
            else:
                cdp_name = convert_to_underscores(field_name)
                return_value = list() if field_name in rules['allow_multiple'] \
                    else ''
                results[cdp_name] = return_value
                if field_name in rules['with_ontology']:
                    results[f'{cdp_name}_ontology'] = return_value
                if field_name in rules['with_units']:
                    results[f'{cdp_name}_unit'] = return_value
                continue
            cdp_name = convert_to_underscores(field_name)
            allow_multiple = field_name in rules['allow_multiple']

            # Should fetch 'text' field only
            if field_name not in rules['with_ontology'] and \
                    field_name not in rules['with_units']:
                results[cdp_name] = get_text_unit_field(sample, biosample_name,
                                                        'text', allow_multiple)

            # Should fetch 'text' and 'ontology' fields
            if field_name in rules['with_ontology']:
                results[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)
                results[f"{cdp_name}_ontology"] = get_ontology_field(
                    sample, biosample_name, allow_multiple)

            # Should fetch 'text' and 'unit' fields
            if field_name in rules['with_units']:
                results[cdp_name] = get_text_unit_field(
                    sample, biosample_name, 'text', allow_multiple)
                results[f"{cdp_name}_unit"] = get_text_unit_field(
                    sample, biosample_name, 'unit', allow_multiple)
            if cdp_name == 'species':
                errors[cdp_name] = results[cdp_name]
            if cdp_name == 'supplied_breed' and results[cdp_name] not in \
                    DAD_IS_BREEDS:
                errors[cdp_name] = results[cdp_name]
            if cdp_name == 'efabis_breed_country':
                errors[cdp_name] = results[cdp_name]
    return results, errors


def get_text_unit_field(sample, biosample_name, field_to_fetch, is_list=False):
    """
    This function will parse text and unit fields in biosamples
    :param sample: sample to parse
    :param biosample_name: name to use in biosample record
    :param field_to_fetch: text or unit to use
    :param is_list: does this record allow to use multiple values
    :return: parsed biosample record
    """
    if is_list:
        tmp = list()
        if biosample_name in sample['characteristics']:
            for item in sample['characteristics'][biosample_name]:
                tmp.append(item[field_to_fetch])
        return tmp
    else:
        if biosample_name in sample['characteristics']:
            return sample['characteristics'][biosample_name][0][field_to_fetch]
        else:
            return ''


def get_ontology_field(sample, biosample_name, is_list=False):
    """
    This function will parse ontology field in biosamples
    :param sample: sample to parse
    :param biosample_name: name to use in biosample record
    :param is_list: does this record allow to use multiple values
    :return: parsed biosample record
    """
    if is_list:
        tmp = list()
        if biosample_name in sample['characteristics']:
            for item in sample['characteristics'][biosample_name]:
                tmp.append(item['ontologyTerms'][0])
        return tmp
    else:
        if biosample_name in sample['characteristics']:
            return sample['characteristics'][biosample_name][0][
                'ontologyTerms'][0]
        else:
            return ''


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
            if rule['Allow Multiple'] == 'yes' \
                    or rule['Allow Multiple'] == 'max 2':
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
    organisms, specimens = fetch_biosamples()
    with open('organisms.json', 'w') as outfile:
        json.dump(organisms, outfile)
    with open('specimens.json', 'w') as outfile:
        json.dump(specimens, outfile)
