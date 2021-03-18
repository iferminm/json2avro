import json
import os
import sys

TYPE_MAP = {
    str: 'string',
    float: 'float',
    int: 'int',
    dict: 'record',
    list: 'array',
    bool: 'boolean',
}

COMPLEX_TYPES = (list, dict)

def read_file(filename: str) -> dict:
    filepath = os.path.join(os.path.curdir, filename)
    with open(filepath, 'r') as jsondata:
        data = jsondata.read()

    return json.loads(data)


def build_document_header(filename: str) -> dict:
    header = {
        'name': snake_to_pascal(filename, 'schema'),
        'namespace': 'com.generated.example',
        'type': 'record',
        'fields': [],
    }
    return header


def snake_to_pascal(name: str, name_type: str) -> str:
    pascal_name = ''.join([t.capitalize() for t in name.split('.')[0].split('_')])
    name_type = name_type.capitalize()
    return f'{pascal_name}{name_type}'


def parse_record_fields(data: dict) -> list:
    return [parse_field(name, value) for name, value in data.items()]


def parse_field(name: str, value):
    value_type = type(value)
    if value_type in COMPLEX_TYPES:
        return parse_complex(name, value, value_type)

    return {'name': name, 'value': TYPE_MAP[value_type]}


def parse_complex(name, value, value_type) -> dict:
    if value_type == dict:
        return parse_record(name, value)
    return parse_array(name, value)


def parse_record(name: str, data: dict) -> dict:
    parsed_record = {
        'name': name,
        'type': {
            'type': 'record',
            'name': snake_to_pascal(name, 'record'),
            'fields': parse_record_fields(data),
        }
    }
    return parsed_record


def parse_array(name: str, data: list) -> list:
    pass



filename = sys.argv[1]
data = read_file(filename)
header = build_document_header(filename)
root_fields = parse_record_fields(data)
header['fields'].extend(root_fields)
print(json.dumps(header, indent=4))
