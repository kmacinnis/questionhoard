from django.contrib import admin
from practicedocs.models import *

class BlockRecipeInline(admin.StackedInline):
    model = BlockRecipe
    extra = 3

class DocumentRecipeAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [BlockRecipeInline]

admin.site.register(DocumentRecipe, DocumentRecipeAdmin)
