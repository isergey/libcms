# encode: utf-8
from lxml import etree
import re

import record


# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                 (unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                  unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                  unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff))
# x = u"<foo>text\u001a</foo>"
# x = re.sub(RE_XML_ILLEGAL, "?", x)


def smart_urlquote(text):
    return re.sub(RE_XML_ILLEGAL, "?", text)


def build_cf_elem(field):
    control_field = etree.Element('field')
    control_field.set('id', field.get_tag())
    control_field.text = smart_urlquote(field.get_data())
    return control_field


def buld_data_subfield(subfield):
    data_subfield = etree.Element('subfield')
    data_subfield.set('id', subfield.get_code())
    data_subfield.text = smart_urlquote(subfield.get_data())
    return data_subfield


def buld_extended_subfield(subfield):
    subfield_el = etree.Element('subfield')
    subfield_el.set('id', subfield.get_code())
    for field in subfield.get_fields():
        if isinstance(field, record.DataField):
            subfield_el.append(build_df_elem(field))
        else:
            subfield_el.append(build_cf_elem(field))
    return subfield_el


def build_df_elem(field):
    data_field = etree.Element('field')
    data_field.set('id', field.get_tag())

    ind1 = etree.SubElement(data_field, 'indicator')
    ind1.set('id', '1')
    ind1.text = smart_urlquote(field.get_ind1())

    ind2 = etree.SubElement(data_field, 'indicator')
    ind2.set('id', '2')
    ind2.text = smart_urlquote(field.get_ind2())

    for subfield in field.get_subfields():
        if isinstance(subfield, record.DataSubfield):
            data_field.append(buld_data_subfield(subfield))
        else:
            data_field.append(buld_extended_subfield(subfield))

    return data_field


def record_to_xml(record_obj, syntax='1.2.840.10003.5.28', namespace=False):
    """
    default syntax rusmarc
    """
    string_leader = record_obj.get_leader()

    root = etree.Element('record')
    root.set('syntax', syntax)
    leader = etree.SubElement(root, 'leader')

    length = etree.SubElement(leader, 'length')
    length.text = smart_urlquote(string_leader[0:5])

    status = etree.SubElement(leader, 'status')
    status.text = smart_urlquote(string_leader[5])

    type = etree.SubElement(leader, 'status')
    type.text = smart_urlquote(string_leader[6])

    leader07 = etree.SubElement(leader, 'leader07')
    leader07.text = smart_urlquote(string_leader[7])

    leader08 = etree.SubElement(leader, 'leader08')
    leader08.text = smart_urlquote(string_leader[8])

    leader09 = etree.SubElement(leader, 'leader09')
    leader09.text = smart_urlquote(string_leader[9])

    indicator_count = etree.SubElement(leader, 'indicatorCount')
    indicator_count.text = smart_urlquote(string_leader[10])

    indicator_length = etree.SubElement(leader, 'identifierLength')
    indicator_length.text = smart_urlquote(string_leader[11])

    data_base_address = etree.SubElement(leader, 'dataBaseAddress')
    data_base_address.text = smart_urlquote(string_leader[12:17])

    leader17 = etree.SubElement(leader, 'leader17')
    leader17.text = smart_urlquote(string_leader[17])

    leader18 = etree.SubElement(leader, 'leader18')
    leader18.text = smart_urlquote(string_leader[18])

    leader19 = etree.SubElement(leader, 'leader19')
    leader19.text = smart_urlquote(string_leader[19])

    entry_map = etree.SubElement(leader, 'entryMap')
    entry_map.text = smart_urlquote(string_leader[20:23])

    for field in record_obj.get_fields():
        if isinstance(field, record.DataField):
            root.append(build_df_elem(field))
        else:
            root.append(build_cf_elem(field))

    return root