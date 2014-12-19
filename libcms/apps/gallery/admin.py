from django.contrib import admin


from models import Album, AlbumImage


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('slug', 'create_date')

admin.site.register(Album,AlbumAdmin)


class AlbumImageAdmin(admin.ModelAdmin):
    list_display = ('album', 'comments', 'create_date')

admin.site.register(AlbumImage,AlbumImageAdmin)
