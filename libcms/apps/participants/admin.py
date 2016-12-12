# encoding: utf-8

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


admin.site.register(models.Library, MPTTModelAdmin)


class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ["user", 'library']


admin.site.register(models.UserLibrary, UserLibraryAdmin)


class LibraryContentEditorAdmin(admin.ModelAdmin):
    list_display = ["user", 'library']


admin.site.register(models.LibraryContentEditor, LibraryContentEditorAdmin)


class UserLibraryPositionAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(models.UserLibraryPosition, UserLibraryPositionAdmin)


class InteractionJournalAdmin(admin.ModelAdmin):
    list_display = ['library', 'records_created', 'records_updated', 'records_delete', 'datetime']

admin.site.register(models.InteractionJournal, InteractionJournalAdmin)

#
# class CountryAdmin(admin.ModelAdmin):
#    list_display = ["name" ]
#
#admin.site.register(Country, CountryAdmin)
#
#
#class CityAdmin(admin.ModelAdmin):
#    list_display = ["name"]
#
#admin.site.register(City, CityAdmin)
#
#class DistrictAdmin(admin.ModelAdmin):
#    list_display = ["name" ]
#
#admin.site.register(District, DistrictAdmin)