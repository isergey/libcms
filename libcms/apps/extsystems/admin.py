from django.contrib import admin
from models import Party


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint', 'status', 'notify')


admin.site.register(Party, PartyAdmin)
