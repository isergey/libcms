# -*- coding: utf-8 -*-
from django.contrib import admin
from zgate.models import ZCatalog, SearchRequestLog
from guardian.admin import GuardedModelAdmin

class ZCatalogAdmin(GuardedModelAdmin):
    list_display = ('title', 'description', 'url', 'xml', 'xsl')

admin.site.register(ZCatalog, ZCatalogAdmin)


class SearchRequestLogAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'use', 'normalize', 'not_normalize', 'datetime', 'search_id')

admin.site.register(SearchRequestLog, SearchRequestLogAdmin)
