from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import QuestionManager, Question


class QuestionManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'available')

admin.site.register(QuestionManager,QuestionManagerAdmin)



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'create_date')

admin.site.register(Question,QuestionAdmin)

