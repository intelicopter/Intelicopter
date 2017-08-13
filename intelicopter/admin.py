from django.contrib import admin
from models import Question, Option


class OptionAdminInline(admin.TabularInline):
    model = Option
    exclude = ['id']


class QuestionAdmin(admin.ModelAdmin):
    fields = ('text', 'question_type')
    inlines = (OptionAdminInline, )
    can_delete = False

admin.site.register(Question, QuestionAdmin)