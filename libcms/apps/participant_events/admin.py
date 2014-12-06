from django.contrib import admin
import models

class AgeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(models.AgeCategory, AgeCategoryAdmin)

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ["name",]

admin.site.register(models.EventType, EventTypeAdmin)