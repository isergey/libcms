from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import QuestionManager


class QuestionManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'available')

admin.site.register(QuestionManager,QuestionManagerAdmin)



