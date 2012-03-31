# coding: utf-8
import datetime
import hashlib
import sunburnt
from lxml import etree
from django.core.files.storage import default_storage
from forms import UploadForm
from ssearch.models import Upload, Record
from django.shortcuts import render, redirect, HttpResponse
from pymarc2 import reader, record, field, marcxml
from django.db import transaction




def return_record_class(scheme):
    if scheme == 'rusmarc' or scheme == 'unimarc':
        return record.UnimarcRecord
    elif scheme == 'usmarc':
        return record.Record
    else:
        raise Exception(u'Wrong record scheme')


def check_iso2709(source, scheme, encoding='utf-8'):
    record_cls = return_record_class(scheme)
    if not len(reader.Reader(record_cls, source, encoding)):
        raise Exception(u'File is not contains records')


def check_xml(source):
    try:
        etree.parse(source)
    except Exception as e:
        raise Exception(u'Wrong XML records file. Error: ' + e.message)

#Our initial page
def initial(request):
    return render(request, 'ssearch/administration/upload.html', {
        'form': UploadForm(),
        })


#Our file upload handler that the form will post to
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            source = default_storage.open(uploaded_file.file)

            try:
                if uploaded_file.records_format == 'iso2709':
                    check_iso2709(source, uploaded_file.records_scheme, uploaded_file.records_encodings)
                elif uploaded_file.records_format == 'xml':
                    check_xml(source)
                else:
                    return HttpResponse(u"Wrong file format")
            except Exception as e:
                default_storage.delete(uploaded_file.file)
                uploaded_file.delete()
                return HttpResponse(u"Error: wrong records file structure: " + e.message)

    return redirect('ssearch:administration:initial')


@transaction.commit_on_success
def pocess(request):
    uploaded_file = Upload.objects.filter(processed=False)[:1]

    if not uploaded_file:
        return HttpResponse(u'No files')
    else:
        uploaded_file = uploaded_file[0]

    source = default_storage.open(uploaded_file.file)
    record_cls = return_record_class(uploaded_file.records_scheme)

    records = []
    if uploaded_file.records_format == 'iso2709':
        for mrecord in reader.Reader(record_cls, source):
            if len(records) > 10:
                inset_records(records, uploaded_file.records_scheme)
                records = []
            records.append(mrecord)
        inset_records(records, uploaded_file.records_scheme)

    elif uploaded_file.records_format == 'xml':
        raise Exception(u"Not yeat emplemented")
    else:
        return HttpResponse(u"Wrong file format")

    return HttpResponse(u'ok')


def inset_records(records, scheme):
    for record in records:
        # gen id md5 hash of original marc record encoded in utf-8
        gen_id =  unicode(hashlib.md5(record.as_marc()).hexdigest())
        if record['001']:
            record_id = record['001'][0].data
            record['001'][0].data = gen_id
        else:
            record.add_field(field.ControlField(tag=u'001', data=gen_id))
            record_id = gen_id


        filter_attrs = {
            'record_id': record_id
        }
        attrs = {
            'gen_id': gen_id,
            'record_id': record_id,
            'scheme': scheme,
            'content': etree.tostring(marcxml.record_to_rustam_xml(record, syntax=scheme), encoding='utf-8'),
            'add_date': datetime.datetime.now()
        }

        rows = Record.objects.filter(**filter_attrs).update(**attrs)
        if not rows:
            attrs.update(filter_attrs)
            obj = Record.objects.create(**attrs)

def convert(request):

    pass

xslt_root = etree.parse('libcms/xsl/record_mars.xsl')
xslt_transformer = etree.XSLT(xslt_root)


def xml_to_dict(doc_tree):
    for el in doc_tree.get_root():
        print el

xml_doc = u"""\
<record syntax="1.2.840.10003.5.28">
<leader>
<length>03559</length>
<status>n</status>
<type>a</type>
<leader07>a</leader07>
<leader08>2</leader08>
<leader09>a</leader09>
<indicatorCount>2</indicatorCount>
<identifierLength>2</identifierLength>
<dataBaseAddress>00253</dataBaseAddress>
<leader17> </leader17>
<leader18>i</leader18>
<leader19> </leader19>
<entryMap>450 </entryMap>
</leader>
<field id="001">RU\SPSTU\\analits2005\\71784</field>
<field id="005">20091228133036.0</field>
<field id="035"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">RU\SPSTU\\analits2005\\71783</subfield></field>
<field id="100"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">20091202a2009    k  y0rusy01020304ca</subfield></field>
<field id="101"><indicator id="1">0</indicator><indicator id="2"> </indicator><subfield id="a">rus</subfield></field>
<field id="102"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">RU</subfield></field>
<field id="200"><indicator id="1">1</indicator><indicator id="2"> </indicator><subfield id="a">Автоформализация фрагментов Java-кода для UML-моделей</subfield><subfield id="f">Д.А. Лукашев, В.П. Котляров, Ю. В. Юсупов</subfield></field>
<field id="225"><indicator id="1">1</indicator><indicator id="2"> </indicator><subfield id="a">Конференция &quot;Технологии Microsoft в теории и практике программирования&quot;</subfield></field>
<field id="320"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="9">572</subfield><subfield id="a">Библиогр.: с. 236</subfield></field>
<field id="330"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">Рассмотрены проблемы формализации исходного кода Java в UML-диаграммах. Описан трансформации кодового фрагмента на языке Java в абстрагированное представление в нота­ции базовых протоколов с использованием инструмента Klocwork и системы специализиро­ванных чекеров</subfield></field>
<field id="330"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">In the article stated the problems of Java code formalization in UML models. Described process of transformation Java code in Basic protocols using Klocwork and special checker module</subfield></field>
<field id="461"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="1"><field id="001">RU\SPSTU\ser\\111514</field></subfield><subfield id="1"><field id="011"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">1994-2354</subfield></field></subfield><subfield id="1"><field id="101"><indicator id="1">0</indicator><indicator id="2"> </indicator><subfield id="a">rus</subfield></field></subfield><subfield id="1"><field id="102"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">RU</subfield></field></subfield><subfield id="1"><field id="200"><indicator id="1">1</indicator><indicator id="2"> </indicator><subfield id="a">Научно-технические ведомости СПбГПУ</subfield></field></subfield><subfield id="1"><field id="210"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">СПб</subfield><subfield id="c">Изд-во СПбГПУ</subfield><subfield id="d">1995-</subfield></field></subfield><subfield id="1"><field id="305"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">Выходит с 1995 г.</subfield></field></subfield><subfield id="1"><field id="311"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">Заглавие: 1995-2002 гг. - Научно-технические ведомости СПбГТУ; №4 2003-№2 2004 - Научно-технические ведомости; №3 2004-№4 2005 - Научно-технические ведомости СПбГТУ; с Т.1 №6 2006 - Научно-технические ведомости СПбГПУ. </subfield></field></subfield><subfield id="1"><field id="311"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">В надзаг.: 1995-№2 1996 - Государственный комитет РФ по высшему образованию; №3 1996-№2 1999 - Министерство общего и профессионального образования РФ; №3 1999-№2 2004 - Министерство образования РФ; №3 2004-№1 2005 - Министерство образования и науки РФ; с №2 2005 - Федеральное агентство по образованию</subfield></field></subfield><subfield id="1"><field id="311"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">Изд-во: 1995-№1 1996 - Изд.-полиграф. центр СПбГТУ; №2 1996-№1 2002 - изд-во СПбГТУ; с №2 2002 - изд-во СПбГПУ</subfield></field></subfield><subfield id="1"><field id="531"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">СПбГПУ</subfield></field></subfield><subfield id="1"><field id="675"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">62(051)</subfield><subfield id="v">3</subfield></field></subfield><subfield id="1"><field id="686"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="2">rubbk</subfield><subfield id="a">74.584(2)738.1</subfield></field></subfield><subfield id="1"><field id="710"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">Санкт-Петербургский  государственный политехнический университет</subfield><subfield id="2">spstush</subfield><subfield id="3">RU\SPSTU\sub\\106397</subfield></field></subfield></field>
<field id="463"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="1"><field id="001">RU\SPSTU\ser\\262527</field></subfield><subfield id="1"><field id="101"><indicator id="1">0</indicator><indicator id="2"> </indicator><subfield id="a">rus</subfield></field></subfield><subfield id="1"><field id="102"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">RU</subfield></field></subfield><subfield id="1"><field id="200"><indicator id="1">1</indicator><indicator id="2"> </indicator><subfield id="a">№3(80) : Информатика. Телекоммуникации. Управление</subfield><subfield id="v">С. 232-236 : ил</subfield></field></subfield><subfield id="1"><field id="210"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="d">2009</subfield></field></subfield></field>
<field id="610"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">формализация</subfield><subfield id="a">чекер</subfield><subfield id="a">базовый протокол</subfield></field>
<field id="700"><indicator id="1"> </indicator><indicator id="2">1</indicator><subfield id="a">Лукашев</subfield><subfield id="b">Д.А.</subfield><subfield id="g">Дмитирий Андреевич</subfield><subfield id="2">19013582</subfield><subfield id="3">ru\spstu\\authors\\2196</subfield><subfield id="p">СПбГПУ</subfield></field>
<field id="701"><indicator id="1"> </indicator><indicator id="2">1</indicator><subfield id="a">Котляров</subfield><subfield id="b">В.П.</subfield><subfield id="f">1944-</subfield><subfield id="g">Всеволод Павлович</subfield><subfield id="2">19013582</subfield><subfield id="3">ru\spstu\\authors\\1619</subfield><subfield id="p">СПбГПУ</subfield></field>
<field id="701"><indicator id="1"> </indicator><indicator id="2">1</indicator><subfield id="a">Юсупов</subfield><subfield id="b">Ю.В.</subfield><subfield id="g">Юрий Вадимович</subfield><subfield id="2">19013582</subfield><subfield id="3">ru\spstu\\authors\\2584</subfield><subfield id="p">СПбГПУ</subfield></field>
<field id="801"><indicator id="1"> </indicator><indicator id="2">2</indicator><subfield id="a">RU</subfield><subfield id="b">19013582</subfield><subfield id="c">20091228</subfield><subfield id="g">RCR</subfield></field>
<field id="998"><indicator id="1"> </indicator><indicator id="2"> </indicator><subfield id="a">АвфрJa000000Лука</subfield></field>
</record>
"""
@transaction.commit_on_success
def indexing(request):
#    import zlib
#
#    open('zip_string.bin','w').write(zlib.compress('абвгддддддддддд'))
#    print zlib.decompress(open('zip_string.bin','r').read())
#    record = Record.objects.using('records').get(id=101000)
#    print record.content
#    doc_tree = etree.XML(record.content)
    doc_tree = etree.XML(xml_doc)
    doc_tree = xslt_transformer(doc_tree)
    print etree.tostring(doc_tree, encoding='utf-8', pretty_print=True)
    return HttpResponse(u'Ok')

    offset = 0
    package_count = 29
    recs = []

    records = list(Record.objects.all()[offset:package_count])
    while len(records):
        recs += records
        offset += package_count
        records = list(Record.objects.all()[offset:offset + package_count])


    for rec in recs:
    #        print rec.content
        doc = etree.XML(rec.content)

        result_tree = xslt_transformer(doc)
        print etree.tostring(result_tree, encoding='utf-8')

    return HttpResponse(unicode(len(records)))