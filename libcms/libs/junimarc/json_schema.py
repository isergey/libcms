# encode: utf-8
import json
from . import record


def make_data_subfield(subfield_dict):
    return record.DataSubfield(
        code=subfield_dict['id'],
        data=subfield_dict['d']
    )


def make_control_field(field_dict):
    return record.ControlField(
        tag=field_dict['tag'],
        data=field_dict['d']
    )


def make_extended_subfield(subfield_dict):
    fields = []

    for field_dict in subfield_dict.get('cf', []):
        fields.append(make_control_field(field_dict))

    for field_dict in subfield_dict.get('df', []):
        fields.append(make_data_field(field_dict))

    return record.ExtendedSubfield(
        code=subfield_dict['id'],
        fields=fields
    )


def make_data_field(field_dict):
    subfields = []

    for subfield_dict in field_dict.get('sf', []):
        subfields.append(make_data_subfield(subfield_dict))

    for subfield_dict in field_dict.get('esf', []):
        subfields.append(make_extended_subfield(subfield_dict))

    return record.DataField(
        tag=field_dict['tag'],
        ind1=field_dict.get('i1', u' '),
        ind2=field_dict.get('i2', u' '),
        subfields=subfields
    )


def record_from_json(json_record):
    record_dict = None

    if type(json_record) == dict:
        record_dict = json_record
    else:
        record_dict = json.loads(json_record)
    fields = []

    for field_dict in record_dict.get('cf', []):
        fields.append(make_control_field(field_dict))

    for field_dict in record_dict.get('df', []):
        fields.append(make_data_field(field_dict))

    return  record.Record(
        leader=record_dict.get('l'),
        fields=fields
    )