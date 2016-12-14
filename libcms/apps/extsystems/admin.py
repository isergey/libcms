# coding=utf-8
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from models import Party


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint', 'status', 'notify', 'statistics_url', 'journal_url')

    def statistics_url(self, obj):
        return format_html(u'<a href="/dashbuilder/workspace/en/overdue">%s</a>' % (obj.id, u'Статистика'))

    def journal_url(self, obj):
        return format_html(u'<a href="/dashbuilder/workspace/en/overdue">%s</a>' % (obj.id, u'Журнал'))

    statistics_url.short_description = u'Статистика'
    journal_url.short_description = u'Журнал'


admin.site.register(Party, PartyAdmin)
