from django.contrib import admin

from exams.models import *

# Register your models here.

admin.site.register(ExamRecipe)
admin.site.register(ExamPartRecipe)

admin.site.register(Exam)
admin.site.register(GeneratedSet)