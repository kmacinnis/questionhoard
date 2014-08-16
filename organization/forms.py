from django import forms
from organization.models import Course, Topic, Subtopic, Objective




class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor','assistants','is_active')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('schema', 'order')

class SubtopicForm(forms.ModelForm):
    class Meta:
        model = Subtopic
        exclude = ('topic', 'order', 'objectives')

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        exclude = ('questions',)
