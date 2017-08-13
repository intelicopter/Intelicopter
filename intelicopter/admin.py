from django.contrib import admin
from models import Question, Option


class OptionAdminInline(admin.TabularInline):
    model = Option
    exclude = ['id']
    #can_delete = False
    has_change_permission = False
    has_delete_permission = False

class QuestionAdmin(admin.ModelAdmin):
    fields = ('text', 'question_type')
    inlines = (OptionAdminInline, )

admin.site.register(Question, QuestionAdmin)