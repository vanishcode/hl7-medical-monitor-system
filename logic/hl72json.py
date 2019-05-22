# -*- coding: utf-8 -*-
"""
json传输
"""
import sys
import re

# json 语义更好一些

INDENT = '  '
KEY_FIELD = '^~\&'


def cleanup_json(json):
    clean_json = re.sub(r':\s*{', ': {', json)
    clean_json = re.sub(r'}\n,', '},', clean_json)
    clean_json = re.sub(r',(\s*)}', r'\1}', clean_json)
    return clean_json


def is_json_object(value):
    return '{' in value


def is_json_boolean(value):
    return value.lower() == 'true' or value.lower() == 'false'


def is_json_string(value):
    return (not value.isdigit()) and (not is_json_object(value)) and (
        not is_json_boolean(value))


def build_json_property(key, value, indent_level):
    if is_json_string(value):
        value = '"' + value + '"'

    indent = INDENT * indent_level
    return indent + '"' + key + '": ' + value + ',\n'


def component_parts_to_json(component_name, component_parts, indent_level):
    indent = INDENT * indent_level
    json = '\n' + indent + '{\n'

    for index, part in enumerate(component_parts):
        if len(part) == 0:
            continue

        part_name = component_name + '.' + str(index + 1)
        json = json + build_json_property(part_name, part, indent_level + 1)

    json = json + indent + '}\n'
    return json


def field_components_to_json(field_name, field_components, indent_level):
    indent = INDENT * indent_level
    json = '\n' + indent + '{\n'

    for index, component in enumerate(field_components):
        if len(component.replace('~', '')) == 0:
            continue

        component_name = field_name + '.' + str(index + 1)

        component_parts = component.split('~')
        if len(component_parts) == 1:
            component_parts_json = component_parts[0]
        else:
            component_parts_json = component_parts_to_json(
                component_name, component_parts, indent_level + 1)

        json = json + build_json_property(component_name, component_parts_json,
                                          indent_level + 1)

    json = json + indent + '}\n'
    return json


def segment_fields_to_json(segment_name, segment_fields, indent_level):
    indent = INDENT * indent_level
    json = '\n' + indent + '{\n'
    for index, field in enumerate(segment_fields):
        if len(field.replace('^', '')) == 0:
            continue
        if field == KEY_FIELD:
            continue

        field_name = segment_name + '.' + str(index + 1)

        field_components = field.split('^')
        if len(field_components) == 1:
            field_components_json = field_components[0]
        else:
            field_components_json = field_components_to_json(
                field_name, field_components, indent_level + 1)

        json = json + build_json_property(field_name, field_components_json,
                                          indent_level + 1)

    json = json + indent + '}\n'
    return json


def hl7_to_json(hl7_segments, indent_level=0):
    indent = INDENT * indent_level
    json = '\n' + indent + '{\n'

    for index, segment in enumerate(hl7_segments):
        segment_fields = segment.split('|')
        segment_name = segment_fields[0] + '.' + str(index + 1)

        segment_fields_json = segment_fields_to_json(segment_name,
                                                     segment_fields,
                                                     indent_level + 1)
        json = json + build_json_property(segment_name, segment_fields_json,
                                          indent_level + 1)

    json = json + indent + '}\n'
    return json


def get_hl7_segments(filename):
    with open(filename) as f:
        segments = [l.strip() for l in f.readlines()]
        segments = [s for s in segments if len(s)]

    return segments


def hl72json(hl7_filename):
    segments = get_hl7_segments(hl7_filename)
    json = hl7_to_json(segments)
    return cleanup_json(json)


# test
jsonobj = hl72json(hl7_filename='demo.txt')
print(jsonobj)
