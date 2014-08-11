from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
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


@login_required
def add_topic(request, schema_id):
    schema = get_object_or_404(Schema, id=schema_id)
    modal_title = "Add topic to schema “{}”".format(schema.name)

    if request.POST:        
        topic = Topic(schema=schema, order=schema.topic_set.count())
        form = TopicForm(request.POST,instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('SchemaDetails', kwargs={'pk':schema.id})
            )

    else: # request.GET
        form = TopicForm()
        variables = RequestContext(request,
        {
            'schema' : schema,
            'form' : form,
            'modal_title' : modal_title,
            'action_url' : reverse('add_topic', kwargs={'schema_id':schema.id})
        })
        return render_to_response('organization/schema_form.html',variables)

@login_required
def add_subtopic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    modal_title = "Add subtopic to topic “{}”".format(topic.name)

    if request.POST:        
        subtopic = Subtopic(topic=topic, order=topic.subtopic_set.count())
        form = SubtopicForm(request.POST,instance=subtopic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('SchemaDetails', kwargs={'pk':topic.schema.id})
            )

    else: # request.GET
        form = TopicForm()
        variables = RequestContext(request,
        {
            'schema' : topic.schema,
            'topic' : topic,
            'form' : form,
            'modal_title' : modal_title,
            'action_url' : reverse('add_subtopic', kwargs={'topic_id':topic.id})
        })
        return render_to_response('organization/schema_form.html',variables)


def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    return HttpResponseRedirect(
            reverse('SchemaDetails', kwargs={'pk':topic.schema.id})
    )


        