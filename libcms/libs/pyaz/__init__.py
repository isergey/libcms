# -*- coding: utf-8 -*-
import _pyaz


class ZException(Exception): pass
class ZConnectionException(ZException): pass
class ZQueryException(ZException): pass
class ZResultSetException(ZException): pass




class ZOptions(object):
    def __init__(self, args={}):
        self.zoptions = _pyaz.ZOptions()
        for key in args.keys():
            if not isinstance(args[key], unicode):
                raise TypeError(u'value of args must be unicode strings')
            self.zoptions.set_option(str(key), args[key].encode('utf-8'))

    def set_option(self, key, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self.zoptions.set_option(key, value)

    def set_implementation_name(self, param):
        self.set_option('implementationName', param.encode('utf-8'))

    def set_user(self, param):
        self.set_option('user', param.encode('utf-8'))

    def set_password(self, param):
        self.set_option('password', param.encode('utf-8'))

    def set_database(self, param):
        self.set_option('databaseName', param.encode('utf-8'))

    def set_charset(self, param):
        self.set_option('charset', param.encode('utf-8'))

    def set_group(self, param):
        self.set_option('group', param.encode('utf-8'))

    def set_syntax(self, param):
        self.set_option('preferredRecordSyntax', param.encode('utf-8'))

    def set_elementset_name(self, param):
        self.set_option('elementSetName', param.encode('utf-8'))

    def get_zoptions_object(self):
        return self.zoptions



class ZQuery(object):
    def __init__(self, query_string):
        if isinstance(query_string, unicode):
            try:
                self.zquery = _pyaz.ZQuery(query_string.encode('utf-8'))
            except _pyaz.ZQueryException as e:
                raise ZQueryException(e.message)
        else:
            raise TypeError('query_string must be unicode object')

    def get_zquery_object(self):
        return self.zquery






class ZRecord(object):
    def __init__(self, zrecord):
        if not isinstance(zrecord, _pyaz.ZRecord):
            raise TypeError('zrecord must be _pyaz.ZRecord object')

        self.zrecord = zrecord

    def render(self):
        return self.zrecord.render()

    def raw(self):
        return self.zrecord.raw()

    def get_zrecord_object(self):
        return self.zrecord

    def __str__(self):
        return self.render()




class ZResultSet(object):
    def __init__(self, zresult_set):
        if not isinstance(zresult_set, _pyaz.ZResultSet):
            raise TypeError('zresult_set must be _pyaz.ZResultSet object')

        self.zresult_set = zresult_set

    def __len__(self):
        return self.get_size()

    def __getitem__(self, offset):
        if offset < 0:
            offset = self.get_size() + offset
        return self.get_records(offset, 1)[0]

    def __getslice__(self,start, end):

        limit = end - start
        return self.get_records(start, limit)

    def __iter__(self):
        self.__next = -1
        self.records = self.get_records(0, self.get_size())
        return self

    def next(self):
        self.__next += 1
        while self.__next < len(self.records):
            return self.records[self.__next]
        raise StopIteration

    def set_option(self, key, value):
        self.zresult_set.set_option(key, value.encode('utf-8'))

    def get_size(self):
        return self.zresult_set.get_size()

    def get_record(self, index=0):
        try:
            return ZRecord(self.zresult_set.get_record(index))
        except _pyaz.ZResultSetException as e:
            raise ZResultSetException(e.message)

    def set_set_name(self, param):
        self.zresult_set.set_set_name(param.encode('utf-8'))

    def set_schema(self, param):
        self.zresult_set.set_schema(param.encode('utf-8'))

    def set_syntax(self, param):
        self.zresult_set.set_syntax(param.encode('utf-8'))

    def get_records(self, offset, limit, format='raw'):

        if offset < 0:
            raise ValueError('offset must be unsigned integer')
        
        if limit < 0:
            raise ValueError('limit must be unsigned integer')

        try:
            return  self.zresult_set.get_records(int(offset), int(limit))
        except _pyaz.ZResultSetException as e:
            raise ZResultSetException(e.message)

    def get_zresult_set_object(self):
        return self.zresult_set






class ZScanSet(object):
    def __init__(self, zscan_set):
        if not isinstance(zscan_set, _pyaz.ZScanSet):
            raise TypeError('zscan_set must be _pyaz.ZScanSet object')
        self.zscan_set = zscan_set

    def set_option(self, key, value):
        self.zscan_set.set_option(key, value.encode('utf-8'))

    def get_option(self, key):
        return self.zscan_set.get_option(key)

    def get_size(self):
        return self.zscan_set.get_size()

    def term(self, index):
        return self.zscan_set.term(index)

    def terms(self):
        return self.zscan_set.terms()

    def display_term(self, index):
        if index >= self.get_size():
            raise IndexError()
        
        return self.zscan_set.display_term(index)

    def get_zscan_set_object(self):
        return self.zscan_set






class ZConnection(object):
    def __init__(self, zoptions):
        if isinstance(zoptions, dict):
           zoptions =  ZOptions(zoptions)
        if not isinstance(zoptions, ZOptions):
            raise TypeError('zoptions must be ZOptions object')
        try:
            self.zconnection = _pyaz.ZConnection(zoptions.get_zoptions_object())
        except _pyaz.ZConnectionException as e:
            raise ZConnectionException(e.message)


    def connect(self, host, port):
        try:
            self.zconnection.connect(str(host), int(port))
        except _pyaz.ZConnectionException as e:
            raise ZConnectionException(e.message)


    def search(self, zquery):
        if isinstance(zquery, unicode):
            zquery = ZQuery(zquery)
        elif not isinstance(zquery, ZQuery):
            raise TypeError('zquery must be ZQuery object or unicode string')

        try:
            return ZResultSet(self.zconnection.search(zquery.get_zquery_object()))

        except _pyaz.ZConnectionException as e:
            raise ZConnectionException(e.message)

    def scan(self, zquery):
        if isinstance(zquery, unicode):
            zquery = ZQuery(zquery)
        elif not isinstance(zquery, ZQuery):
            raise TypeError('zquery must be ZQuery object or unicode string')

        try:
            return ZScanSet(self.zconnection.scan(zquery.get_zquery_object()))

        except _pyaz.ZConnectionException as e:
            raise ZConnectionException(e.message)

    def set_option(self, key, value):
        self.zconnection.set_option(key, value.encode('utf-8'))

    def get_option(self, key):
        return self.zconnection.get_option(key)

    def get_zconnection_object(self):
        return self.zconnection


class ZPackage(object):
    def __init__(self, zconnection, zoptions):

        if not isinstance(zconnection, ZConnection):
            raise TypeError('zconnection must be ZConnection object')
#        if not isinstance(zoptions, ZOptions):
#            raise TypeError('zoptions  must be ZOptions object')
        self.zpackage = _pyaz.ZPackage(zconnection.get_zconnection_object(),
                                        zoptions.get_zoptions_object())

    def set_option(self, key, value):
        self.zpackage.set_option(key, value)

    def get_option(self, key):
        return self.zpackage.get_option(key)

    def send(self, type):
        try:
            self.zpackage.send(str(type))
        except _pyaz.ZConnectionException as e:
            raise ZConnectionException(e.message)



class RPNQueryBuilder(object):
    RELATION_VALUES = ( # attr 2
        u'1', # Less than
        u'2', # Less than or equal
        u'3', # Equal (default)
        u'4', # Greater or equal
        u'5', # Greater than
        u'6', # Not equal (unsupported in Zebra)
        u'100', # Phonetic (unsupported in Zebra)
        u'101', # Stem (unsupported in Zebra)
        u'102', # Relevance
        u'103', # AlwaysMatches  (in Zebra: AlwaysMatches searches are only supported
        # if alwaysmatches indexing has been enabled)
    )

    POSITION_VALUES = ( # attr 3
        u'1', # First in field
        u'2', # First in subfield
        u'3', # Any position in field (default)
    )

    STRUCTURE_VALUES = ( # attr 4
        u'1', # Phrase (default)
        u'2', # Word
        u'3', # Key
        u'4', # Year
        u'5', # Date (normalized)
        u'6', # Word list
        u'100', # Date (un-normalized) (unsupported in Zebra)
        u'101', # Name (normalized)(unsupported in Zebra)
        u'102', # Name (un-normalized)(unsupported in Zebra)
        u'103', # Structure (unsupported in Zebra)
        u'104', # Urx
        u'105', # Free-form-text
        u'106', # Document-text
        u'107', # Local-number
        u'108', # String (unsupported in Zebra)
        u'109', # Numeric string
    )

    TRUNCATION_VALUES = ( # attr 5
        u'1', # Right truncation
        u'2', # Left truncation
        u'3', # Left and right truncation
        u'100', # Do not truncate  (default)
        u'101', # Process # in search term
        u'102', # RegExpr-1 (in Zebra)
        u'103', # RegExpr-2 (in Zebra)
    )

    COMPLETENESS_VALUES = ( # attr 6
        u'1', # Incomplete subfield (default)
        u'2', # Complete subfield
        u'3', # Complete field
    )

    def __init__(self):
        self.query_pieces = []
        self.operators = [] #стек операторов

    def __unicode__(self):
        return self.build()

    def __str__(self):
        return self.build().encode('UTF-8')

    def add_condition(self, term, use, relation=u'', position=u'', structure=u'',
                      truncation=u'', completeness=u'', operator=u'@and'):

        if self.query_pieces:
            self.query_pieces.insert(0, operator)

        if not isinstance(term, unicode):
            raise TypeError(u'term must be unicode string')
        term = term.replace("\\","\\\\")
        if not isinstance(use, unicode):
            raise TypeError(u'use must be unicode string')
        self.query_pieces.append(u'@attr 1=' + use)

        if relation:
            if relation not in self.RELATION_VALUES:
                raise ValueError(u'wrong relation attribute')
            self.query_pieces.append(u'@attr 2=' + relation)
#        else:
#            relation = u'3'

        if position:
            if  position not in self.POSITION_VALUES:
                raise ValueError(u'wrong position attribute')
            self.query_pieces.append(u'@attr 3=' + position)
#        else:
#            position = u'3'

        if structure:
            if structure not in self.STRUCTURE_VALUES:
                raise ValueError(u'wrong structure attribute')
            self.query_pieces.append(u'@attr 4=' + structure)
#        else:
#            structure = u'1'

        if truncation:
            if truncation not in self.TRUNCATION_VALUES:
                raise ValueError(u'wrong truncation attribute')
            self.query_pieces.append(u'@attr 5=' + truncation)
#        else:
#            truncation = u'100'

        if completeness:
            if completeness not in self.COMPLETENESS_VALUES:
                raise ValueError(u'wrong completeness attribute')
            self.query_pieces.append(u'@attr 6=' + completeness)
#        else:
#            completeness = u'1'










        term = u'"' + term.strip(u'"').strip() + u'"'
        self.query_pieces.append(term)

    def build(self):
        return u' '.join(self.query_pieces)

