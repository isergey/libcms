from django.contrib import admin

from . import models


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'client_id', 'client_secret')

admin.site.register(models.Application, ApplicationAdmin)



