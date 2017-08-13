from django.contrib import admin
from django.forms import models
from models import Question, Option


class MyInline(models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(MyInline, self).__init__(*args, **kwargs)
        self.can_delete = False

class OptionAdminInline(admin.TabularInline):
    model = Option
    exclude = ['id']
    formset = MyInline

class QuestionAdmin(admin.ModelAdmin):
    fields = ('text', 'question_type')
    inlines = (OptionAdminInline, )

admin.site.register(Question, QuestionAdmin)