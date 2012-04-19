# -*- encoding: utf-8 -*-
from lxml import etree
# на эти трансформаторы ссылаются из других модулей


xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
xslt_transformer = etree.XSLT(xslt_root)

xslt_marc_dump = etree.parse('libcms/xsl/marc_dump.xsl')
xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)

xslt_bib_draw = etree.parse('libcms/xsl/full_document.xsl')
xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)