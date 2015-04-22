from django.contrib import admin

from . import models


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'client_id', 'client_secret')

admin.site.register(models.Application, ApplicationAdmin)



