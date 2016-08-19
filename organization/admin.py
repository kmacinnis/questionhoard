from django.contrib import admin
from organization.models import *

class SectionInline(admin.TabularInline):
    model = Section
    extra = 4
    fields = [
        'name',
        'order',
    ]

class ChapterAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'comment',
        'book',
        'order',
    ]
    inlines = [SectionInline]


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Book)
admin.site.register(CourseType)
admin.site.register(Objective)
admin.site.register(Section)
admin.site.register(Course)
