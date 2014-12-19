from django.contrib import admin
import models


class ADUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'login')


admin.site.register(models.AdUser, ADUserAdmin)

