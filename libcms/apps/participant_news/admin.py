from django.contrib import admin
import models


class NewsImageAdmin(admin.ModelAdmin):
    list_display = ["news",]

admin.site.register(models.NewsImage, NewsImageAdmin)