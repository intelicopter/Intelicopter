from django.contrib import admin
from models import Question, Option

class OptionAdminInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = (OptionAdminInline, )

admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)