from lxml import etree
from django.conf import settings

TRANSFORMERS = getattr(settings, 'TRANSFORMERS', {})

transformers = {}


def transformers_init():
    for key in TRANSFORMERS.keys():
        xsl_transformer = TRANSFORMERS[key]
        transformers[key] = etree.XSLT(etree.parse(xsl_transformer))


transformers_init()

