from django.contrib import admin
from organization.models import *

class SubtopicInline(admin.TabularInline):
    model = Subtopic
    extra = 4
    fields = [
        'name',
        'order',
    ]

class TopicAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'comment',
        'order',
    ]
    inlines = [SubtopicInline]


admin.site.register(Topic, TopicAdmin)