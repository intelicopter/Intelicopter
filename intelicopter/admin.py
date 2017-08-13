from django.contrib import admin
from models import Question, Option


class OptionInline(admin.TabularInline):
    model = Option


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]

admin.site.register(Question)
admin.site.register(Option, OptionInline, QuestionAdmin)