from django.contrib import admin
import models


class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", 'image']

admin.site.register(models.Banner, BannerAdmin)

