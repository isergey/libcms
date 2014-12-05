from django.contrib import admin
import models

class ContentManagerAdmin(admin.ModelAdmin):
    list_display = ["user",'library']

admin.site.register(models.ContentManager, ContentManagerAdmin)

class LibraryAvatarAdmin(admin.ModelAdmin):
    list_display = ["library",'avatar']

admin.site.register(models.LibraryAvatar, LibraryAvatarAdmin)