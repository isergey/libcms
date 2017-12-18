# -*- encoding: utf-8 -*-
from django.conf import settings
import os
from lxml import etree
# на эти трансформаторы ссылаются из других модулей
BASE_PATH = getattr(settings, 'PROJECT_PATH')
xslt_root = etree.parse(os.path.join(BASE_PATH, 'xsl/record_in_search.xsl'))
xslt_transformer = etree.XSLT(xslt_root)

xslt_marc_dump = etree.parse(os.path.join(BASE_PATH, 'xsl/marc_dump.xsl'))
xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)

xslt_bib_draw = etree.parse(os.path.join(BASE_PATH, 'xsl/full_document.xsl'))
xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)

xslt_indexing_root = etree.parse(os.path.join(BASE_PATH, 'xsl/record_indexing.xsl'))
xslt_indexing_transformer = etree.XSLT(xslt_indexing_root)

short_xslt_root = etree.parse(os.path.join(BASE_PATH, 'xsl/short_document.xsl'))
short_transform = etree.XSLT(short_xslt_root)
