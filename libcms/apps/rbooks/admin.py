from django.contrib import admin


from models import InternalAccessRange



class InternalAccessRangeAdmin(admin.ModelAdmin):
    list_display = ('range', 'type', 'comments')
    readonly_fields=('type',)
    exclude = ('pickle',)

admin.site.register(InternalAccessRange, InternalAccessRangeAdmin)
