from django.contrib import admin
import models


class LibraryAvatarAdmin(admin.ModelAdmin):
    list_display = ["library", 'avatar']

admin.site.register(models.LibraryAvatar, LibraryAvatarAdmin)
