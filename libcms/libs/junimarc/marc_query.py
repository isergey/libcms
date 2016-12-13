from collections import OrderedDict
from record import Record, ControlField, DataField, DataSubfield, ExtendedSubfield


class SubfieldQuery(object):
    def __init__(self, subfields):
        self.subfields = subfields or []

    def get_data(self, default_value=''):
        if not self.subfields:
            return default_value

        subfield = self.subfields[0]
        if isinstance(subfield, DataSubfield):
            return subfield.get_data()
        return default_value

    def get_field(self, tag):
        fields = []
        for subfield in self.subfields:
            if isinstance(subfield, ExtendedSubfield):
                fields += subfield.get_fields(tag)
        return FieldQuery(fields)

    def each(self, callback):
        for subfield in self.subfields:
            callback(SubfieldQuery([subfield]))

    def list(self):
        subfield_queries = []
        for subfield in self.subfields:
            subfield_queries.append(SubfieldQuery([subfield]))
        return subfield_queries

    def at(self, index):
        if index < len(self.subfields):
            return SubfieldQuery([self.subfields[index]])
        return SubfieldQuery([])

    def is_exist(self):
        return len(self.subfields) > 0

    def get_element(self):
        return self.subfields[0]


class FieldQuery(object):
    def __init__(self, fields=None):
        self.fields = fields or []
        self.extended_subfields = ['1']

    def set_extended_subfields(self, extended_subfields):
        self.extended_subfields = extended_subfields

    def get_subfield(self, code):
        subfields = []
        for field in self.fields:
            if not isinstance(field, DataField):
                continue
            exist_subfields = field.get_subfields(code)
            if exist_subfields:
                subfields = exist_subfields
                break
        return SubfieldQuery(subfields)

    def get_inner_field(self, tag):
        fields = []
        for extended_subfield in self.extended_subfields:
            subfield_queries = self.get_subfield(extended_subfield).list()
            for subfield_query in subfield_queries:
                field_query = subfield_query.get_field(tag)
                if field_query.is_exist():
                    fields.append(field_query.get_element())
        return FieldQuery(fields)

    def get_ind1(self, default_value=' '):
        if self.fields:
            field = self.fields[0]
        else:
            return default_value

        if isinstance(field, DataField):
            return field.get_ind1()
        return default_value

    def get_ind2(self, default_value=' '):
        if self.fields:
            field = self.fields[0]
        else:
            return default_value

        if isinstance(field, DataField):
            return field.get_ind2()
        return default_value

    def each(self, callback):
        for field in self.fields:
            callback(FieldQuery([field]))

    def list(self):
        field_queries = []
        for field in self.fields:
            field_queries.append(FieldQuery([field]))
        return field_queries

    def at(self, index):
        if index < len(self.fields):
            return FieldQuery([self.fields[index]])
        return FieldQuery([])

    def is_exist(self):
        return len(self.fields) > 0

    def get_element(self):
        return self.fields[0]

    def get_data(self, default_value=u''):
        if len(self.fields) > 0:
            field = self.fields[0]
            if isinstance(field, ControlField):
                return field.get_data()
        return default_value

class MarcQuery(object):
    def __init__(self, record):
        if not isinstance(record, Record):
            raise TypeError('record must be instance of junimarc Record')

        self.record = record
        self.fields_index = None

    def get_field(self, tag):
        if self.fields_index is None:
            self.__build_index()

        fields = self.fields_index.get(tag, [])
        return FieldQuery(fields)

    def get_element(self):
        return self.record

    def __build_index(self):
        self.fields_index = OrderedDict()
        for field in self.record.get_fields():
            exist_fields = self.fields_index.get(field.get_tag())
            if exist_fields is None:
                exist_fields = []
                self.fields_index[field.get_tag()] = exist_fields
            exist_fields.append(field)
