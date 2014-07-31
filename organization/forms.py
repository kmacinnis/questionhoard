from django import forms
from organization.models import Course




class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor','assistants','is_active')

