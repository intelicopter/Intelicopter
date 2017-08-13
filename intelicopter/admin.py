from django.contrib import admin
import os

from models import Question, Option

class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]

admin.site.register(Question, Option, OptionInline, QuestionAdmin)