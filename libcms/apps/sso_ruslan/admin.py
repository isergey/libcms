# encoding: utf-8
from django.contrib import admin
import models


class RuslanUserAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.RuslanUser, RuslanUserAdmin)

