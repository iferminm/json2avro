import json
import os
import sys

TYPE_MAP = {
    str: "string",
    float: "float",
    int: "int",
    dict: "record",
    list: "array",
    bool: "boolean",
}

def read_file(filename: str) -> dict:
    filepath = os.path.join(os.path.curdir, filename)
    with open(filepath, 'r') as jsondata:
        data = jsondata.read()

    return json.loads(data)


def snake_to_pascal(name: str, name_type: str) -> str:
    pascal_name = ''.join([t.capitalize() for t in name.split('.')[0].split('_')])
    name_type = name_type.capitalize()
    return f'{pascal_name}{name_type}'


def build_document_header(filename: str) -> dict:
    header = {
        'name': snake_to_pascal(filename, 'schema'),
        'namespace': 'com.generated.example',
        'type': 'record',
        'fields': [],
    }
    return header

def parse_record(data: dict) -> list:
    result = []
    for name, value in data.items():
        result.append({"name": name, "type": TYPE_MAP[type(value)]})

    print(result)
    return result


filename = sys.argv[1]
data = read_file(filename)
header = build_document_header(filename)
root_fields = parse_record(data)
header['fields'].extend(root_fields)
print(json.dumps(header, indent=4))
