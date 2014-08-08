from django.shortcuts import render
from django.core.urlresolvers import reverse
from vanilla import ListView, CreateView, DetailView
from organization.models import *
from organization.forms import *


class TopicList(ListView):
    model = Topic
    context_object_name = 'topics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_question_links'] = True
        return context


class CourseDetails(DetailView):
    model = Course
    context_object_name = 'course'


class CreateCourse(CreateView):
    model = Course
    form_class = CourseInfoForm

    def post(self, request):
        course = Course(instructor=request.user)
        form = CourseInfoForm(request.POST, instance=course)
        if form.is_valid():
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('CourseDetails', kwargs={'pk': self.object.id})


class SchemaDetails(DetailView):
    model = Schema
    context_object_name = 'schema'


