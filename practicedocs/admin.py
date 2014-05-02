from django.contrib import admin
from practicedocs.models import *

class BlockRecipeInline(admin.StackedInline):
    model = BlockRecipe
    extra = 3

class DocumentRecipeAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [BlockRecipeInline]
    
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()
    
    

admin.site.register(DocumentRecipe, DocumentRecipeAdmin)
admin.site.register(Document)
admin.site.register(BlockRecipe)
admin.site.register(Block)
admin.site.register(Exercise)

