# encoding: utf-8

from django.contrib import admin

from models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ["text",]

admin.site.register(Content, ContentAdmin)


#
#class CountryAdmin(admin.ModelAdmin):
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