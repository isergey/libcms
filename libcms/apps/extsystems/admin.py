# coding=utf-8
from django.contrib import admin
from django.utils.html import format_html
from models import Party, NotificationTime


class NotificationTimeInline(admin.StackedInline):
    model = NotificationTime
    extra = 3


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint', 'status', 'notify', 'statistics_url', 'journal_url')
    inlines = [NotificationTimeInline]

    def statistics_url(self, obj):
        return format_html(u'<a href="%s">%s</a>' % (u'/dashbuilder/workspace/en/overdue', u'Статистика'))

    def journal_url(self, obj):
        return format_html(u'<a href="%s">%s</a>' % (u'/dashbuilder/workspace/en/overdue', u'Журнал'))

    statistics_url.short_description = u'Статистика'
    journal_url.short_description = u'Журнал'


admin.site.register(Party, PartyAdmin)
