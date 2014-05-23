from django.contrib import admin
from questions.models import *


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 3

class ConditionInline(admin.StackedInline):
    model = Condition
    extra = 1

class RandVarInline(admin.TabularInline):
    model = RandVar
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'symbol_vars',
        # 'code',
        # 'question_text',
        # 'prompt',
        # 'short_version',
        ]
    inlines = [
        RandVarInline,
        ConditionInline,
        AnswerChoiceInline,
    ]


admin.site.register(Question, QuestionAdmin)
