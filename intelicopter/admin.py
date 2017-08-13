from django.contrib import admin
import os

from models import Question, Option

admin.site.register(Question)

class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]