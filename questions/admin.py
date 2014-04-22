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
        # 'prompt',
        # 'body',
        ]
    inlines = [
        RandVarInline,
        ConditionInline,
        AnswerChoiceInline,
    ]

class BlockRecipeInline(admin.StackedInline):
    model = BlockRecipe
    extra = 3

class DocumentRecipeAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [BlockRecipeInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(DocumentRecipe, DocumentRecipeAdmin)
