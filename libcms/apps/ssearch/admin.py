from django.contrib import admin

from models import Source, Record, Upload, IndexStatus


class SourceAdmin(admin.ModelAdmin):
    list_display = ('source_type',)


admin.site.register(Source, SourceAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ('source', 'add_date')


admin.site.register(Record, RecordAdmin)


class UploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'processed', 'success')


admin.site.register(Upload, UploadAdmin)


class IndexStatusAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'last_index_date', 'indexed', 'deleted')


admin.site.register(IndexStatus, IndexStatusAdmin)
