# coding=utf-8
from collections import OrderedDict

DEFAULT_RECORD_SYNTAX = '1.2.840.10003.5.105'

CONTENT_TYPES = {
    'string': 'string',
    'octets': 'octets',
    'numeric': 'numeric',
    'date': 'date',
    'ext': 'ext',
}


class Field(object):
    def __init__(self, value='', content='', type=3, occurrence=1, content_type='string'):
        self.__content = content
        self.__value = value
        self.__type = type
        self.__occurrence = occurrence
        self.__content_type = content_type

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def occurrence(self):
        return self.__occurrence

    @occurrence.setter
    def occurrence(self, value):
        self.__occurrence = value

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, value):
        self.__content_type = value

    def to_dict(self):
        return {
            'tagType': self.__type,
            'tagValue': self.__value,
            'tagOccurrence': self.__occurrence,
            'contentType': self.__content_type,
            'value': self.__content
        }


class Record(object):
    def __init__(self, fields=None, syntax=DEFAULT_RECORD_SYNTAX):
        self.__fields = fields or OrderedDict()
        self.__syntax = syntax

    def add_field(self, field):
        exist_fields = self.__fields.get(field.value, [])
        if not exist_fields:
            self.__fields[field.value] = exist_fields
        exist_fields.append(field)

    def get_fields(self):
        return self.__fields

    def get_field(self, value):
        return self.__fields.get(value, [])

    def remove_field(self, field):
        exist_fields = self.__fields.get(field.value)

        if not exist_fields:
            return

        exist_fields.remove(field)

        if not exist_fields:
            del self.__fields[field.value]

    def sort_fields(self):
        """
        Сортировать существющие поля по значению occurrence
        :return:
        """
        for key, fields in self.__fields.items():
            fields.sort(key=lambda x: x.occurrence)

    def recalculate_occurrence(self):
        self.sort_fields()
        for key, fields in self.__fields.items():
            fields.sort(key=lambda x: x.occurrence)
            for i, field in enumerate(fields):
                field.occurrence = i + 1

    def to_dict(self):
        self.recalculate_occurrence()

        field_dicts = []

        for key, fields in self.__fields.items():
            for field in fields:
                field_dicts.append(field.to_dict())

        return {
            'GRSTag': field_dicts,
            'syntax': self.__syntax
        }

    @staticmethod
    def from_dict(record_dict):
        if not isinstance(record_dict, dict):
            raise ValueError('record_dict must be dict')

        record = Record(syntax=record_dict.get('syntax', DEFAULT_RECORD_SYNTAX))

        for field_dict in record_dict.get('GRSTag', []):
            record.add_field(Field(
                value=field_dict.get('tagValue', ''),
                content=field_dict.get('value', ''),
                type=field_dict.get('tagType', 3),
                occurrence=field_dict.get('tagOccurrence', 1),
                content_type=field_dict.get('contentType', CONTENT_TYPES['string'])
            ))
        record.sort_fields()
        return record
