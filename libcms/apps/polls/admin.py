# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Poll, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question',)

admin.site.register(Poll, PollAdmin)