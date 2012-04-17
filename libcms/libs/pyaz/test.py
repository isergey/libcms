# -*- coding: utf-8 -*-
from pyaz import *
import pymarc
from pymarc.marcxml import record_to_xml
import time

#record = pymarc.Record()
#
#field = pymarc.Field(
#    tag='200',
#    indicators=['1', ' '],
#    subfields=['a', u'привет'])
#record.add_field(field)
#
#writer = pymarc.MARCWriter(open('utf.mrc', 'wb'))
#writer.write(record, encoding='cp1251')
#writer.close()
#

#zcon.connect('ruslan.ru', 210)
#
#
#zopts = ZOptions()
##zopts.set_option('databaseName',u'test')
#zopts.set_option('syntax',u'rusmarc')
#zpac = ZPackage(zcon, zopts)
#zpac.set_option('action', 'recordInsert')
#zpac.set_option('record', record.as_marc(encoding='utf-8'))
#
s = time.time()
#for i in xrange(100):
#    print i
#    zpac.send('update')
#
#print'time: ', time.time() - s
#
#zres = zcon.search(u'@attr 1=4 привет')
#print zres.get_size()


#
#print record_to_xml(record ,namespace=True)


def delete(zcon, records):
    zopts = ZOptions()
    zopts.set_option('databaseName', u'USTORUS')
    zopts.set_option('syntax', u'usmarc')

    zpac = ZPackage(zcon, zopts)
    zpac.set_option('action', 'recordDelete')

    for i, record in enumerate(records):
        print i
        zpac.set_option('record', record)
        zpac.send('update')


def insert(zcon):
    zopts = ZOptions()
    zopts.set_option('databaseName', u'USTORUS')
    zopts.set_option('syntax', u'usmarc')

    zpac = ZPackage(zcon, zopts)
    zpac.set_option('action', 'recordInsert')

    reader = pymarc.MARCReader(file('utf.mrc', 'r'), to_unicode=True, encoding='utf-8')

    for i, record in enumerate(reader):
        print i
        zpac.set_option('record', record.as_marc(encoding='utf-8'))
        zpac.send('update')


def write_records(file_name, records):
    rusmarc_out = open(file_name, 'wb')
    for record in records:
        rusmarc_out.write(record)

    rusmarc_out.close()


def test_zwork():
    zcon = ZConnection(
        {
            'user': u'erm',
            'password': u'123456',
            'databaseName': u'USTORUS',
            'preferredRecordSyntax': u'rusmarc',
        }
    )
    zcon.connect('172.16.174.128', 210)
    #zcon.connect('arch.zi.ipq.co', 9999)
    s = time.time()

    for i in xrange(1000):
        res = zcon.search(u'@attr 1=4 a')

    print'time: ', time.time() - s,

    print res.get_size()
    print res.get_record(0)
    #records = res.get_records(0,res.get_size())

    #write_records('rusmarc_ebsco.mrc', records)


def test_reader():
    reader = pymarc.MARCReader(file('rusmarc_ebsco.mrc', 'r'), to_unicode=True, encoding='utf-8')
    for i, record in enumerate(reader):
        if i == 100: break
        print record_to_xml(record)


test_zwork()
#test_reader()
#records = res.get_records(0, res.get_size())


#delete(zcon,records)



#insert(zcon)


##
#zpac = ZPackage(zcon, zopts)
#zpac.set_option('action', 'recordInsert')
#zpac.set_option('record', record.as_marc(encoding='utf-8'))
#zpac.send('update')


#for i, zrecord in enumerate(res.get_records(0, res.get_size())):
#     print i
#     zpac.set_option('record', zrecord)
#     zpac.send('update')
#    record =  pymarc.Record(data=zrecord,to_unicode=True, encoding='utf-8')


print'time: ', time.time() - s
#zopts = ZOptions()
##zopts.set_option('databaseName',u'test')
#zopts.set_option('syntax', u'rusmarc')
#
#zpac = ZPackage(zcon, zopts)
#zpac.set_option('action', 'recordInsert')
#
#reader = pymarc.MARCReader(file('utf.mrc', 'r'), to_unicode=True, encoding='utf-8')
##writer = pymarc.MARCWriter(open('utf.mrc','wb'))
#s = time.time()
#for i, record in enumerate(reader):
#    print i
#    field = pymarc.Field(
#        tag='200',
#        indicators=['1', ' '],
#        subfields=['a', u'привет '+unicode(i)])
#    record.add_field(field)
#    print record
#
#    #    writer.write(record, encoding=('utf-8'))
#    zpac.set_option('record', record.as_marc(encoding='utf-8'))
#    zpac.send('update')
#    if i == 1000: break
#writer.close()

#print'time: ', time.time() - s

#record.force_utf8 = True
#writer.write(record,encoding='utf-8')
#writer.close()
#print record
#xml_file.write(str(record))
#xml_file.write('\n')

#print'time: ', time.time() - s
#
#
#
#try:
#    zcon.connect('172.16.174.128', 210)
#    for i in xrange(1):
#        s = time.time()
#
#        zres = zcon.search(u'@attr 1=4 test')
#
#        print i, 'time: ', time.time() - s
#        #        print zres.get_size()
#        records = zres.get_records(0, 10, 'xml; charset=utf-8,utf-8')
##        for record in records:
##            print record
#except Exception as e:
#    print e, 'ee'




#def detectCPUs():
#    import os
#    """
#    #Detects the number of CPUs on a system. Cribbed from pp.
#    """
#    # Linux, Unix and MacOS:
#    if hasattr(os, "sysconf"):
#        if os.sysconf_names.has_key("SC_NPROCESSORS_ONLN"):
#            # Linux & Unix:
#            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
#            if isinstance(ncpus, int) and ncpus > 0:
#                return ncpus
#        else: # OSX:
#            return int(os.popen2("sysctl -n hw.ncpu")[1].read())
#        # Windows:
#    if os.environ.has_key("NUMBER_OF_PROCESSORS"):
#        ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
#        if ncpus > 0:
#            return ncpus
#    return 1 # Default
#
#print detectCPUs(),1
