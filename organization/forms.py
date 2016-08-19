from django import forms
from organization.models import Course, Chapter, Section, Objective




class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor','assistants','is_active')


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = ('book', 'order')

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ('chapter', 'order', 'objectives')

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        exclude = ('questions',)
