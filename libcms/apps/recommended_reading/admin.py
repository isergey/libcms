from django.contrib import admin
from . import models


class ItemAttributeValueInline(admin.TabularInline):
    model = models.ItemAttributeValue


class ItemAttachmentInline(admin.TabularInline):
    model = models.ItemAttachment


class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemAttributeValueInline, ItemAttachmentInline]
    list_display = ['section', 'title', 'record_id', 'published', 'created', 'updated']


admin.site.register(models.Item, ItemAdmin)


class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


admin.site.register(models.ItemAttribute, ItemAttributeAdmin)
