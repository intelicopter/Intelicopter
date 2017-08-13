from django.contrib import admin
from models import Question, Option


class OptionAdminInline(admin.TabularInline):
    model = Option
    fields = ('option_text')


class QuestionAdmin(admin.ModelAdmin):
    fields = ('text', 'question_type')
    inlines = (OptionAdminInline, )

admin.site.register(Question, QuestionAdmin)