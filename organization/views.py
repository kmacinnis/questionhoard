from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from vanilla import ListView, CreateView, DetailView
from organization.models import *
from organization.forms import *
import json


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
    """
    On GET, returns the form to be used to add a topic.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            panel_url   : if form.is_valid, the new panel for the accordion,
            place       : if form.is_valid, the place to stick the new panel,
            form_html   : if form not valid, the html to represent the form
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'schema' : schema,
            'form' : form,
            'form_title' : form_title,
            'action_url' : reverse('add_topic', kwargs={'schema_id':schema.id})
        })
        return render_to_response('organization/schema_form.html',variables)
    
    schema = get_object_or_404(Schema, id=schema_id)
    form_title = "Add topic to schema “{}”".format(schema.name)

    if request.POST:
        topic = Topic(schema=schema, order=schema.topic_set.count())
        form = TopicForm(request.POST,instance=topic)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'panel_url' : reverse('get_accordion_panel', 
                    kwargs={'item_type':'topic','item_id':topic.id}),
                'place' : '#accordion-main',
                'action' : 'add',
                'panel_html' : get_accordion_panel(
                        request, 'topic', topic.id
                ).content.decode()
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(TopicForm())

@login_required
def edit_topic(request, topic_id):
    """
    On GET, returns the form to be used to edit the topic.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            form_html   : if form not valid, the html to represent the form
            action      : "edit"
            label       : the id of the panel label
            name        : the new name of the subtopic
            
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'form' : form,
            'form_title' : 'Edit Topic',
            'item_type' : 'topic',
            'item_id' : topic_id,
            'action_url' : reverse('edit_topic', kwargs={'topic_id':topic.id}),
        })
        return render_to_response('organization/schema_form.html',variables)
    
    topic = get_object_or_404(Topic, id=topic_id)

    if request.POST:
        form = TopicForm(request.POST,instance=topic)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'action' : 'edit',
                'label' : '#label-topic-{}'.format(topic.id),
                'name' : topic.name
                
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(TopicForm(instance=topic))

@login_required
def edit_topic_old(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.POST:
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    else: # request.GET
        form = TopicForm(instance=topic)
    variables = RequestContext(request, 
        {
            'form' : form,
            'form_title' : 'Edit Topic',
            'item_type' : 'topic',
            'item_id' : topic_id,
            'action_url' : reverse('edit_topic', kwargs={'topic_id':topic.id}),
        })
    return render_to_response('organization/schema_form.html',variables)

@login_required
def delete_item(request, item_type, item_id):
    
    if not 'confirmed' in request.GET:
        raise Http404
    Item = {
        'topic' : Topic,
        'subtopic' : Subtopic,
        'objective' : Objective,
        'question' : Question,
    }[item_type]
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return HttpResponse('deleted')

@login_required
def add_subtopic(request, topic_id):
    """
    On GET, returns the form to be used to add a subtopic.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            panel_url   : if form.is_valid, the new panel for the accordion,
            place       : if form.is_valid, the place to stick the new panel,
            form_html   : if form not valid, the html to represent the form
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'schema' : topic.schema,
            'topic' : topic,
            'form' : form,
            'form_title' : form_title,
            'action_url' : reverse('add_subtopic', kwargs={'topic_id':topic.id})
        })
        return render_to_response('organization/schema_form.html',variables)
    
    topic = get_object_or_404(Topic, id=topic_id)
    form_title = "Add subtopic to topic “{}”".format(topic.name)

    if request.POST:
        subtopic = Subtopic(topic=topic, order=topic.subtopic_set.count())
        form = SubtopicForm(request.POST,instance=subtopic)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'panel_url' : reverse('get_accordion_panel', 
                    kwargs={'item_type':'subtopic','item_id':subtopic.id}),
                'place' : '#accordion-topic-{}'.format(topic.id),
                'action' : 'add',
                'panel_html' : get_accordion_panel(
                        request, 'subtopic', subtopic.id
                ).content.decode()
                
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(TopicForm())

@login_required
def edit_subtopic(request, subtopic_id):
    """
    On GET, returns the form to be used to edit the subtopic.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            form_html   : if form not valid, the html to represent the form
            action      : "edit"
            label       : the id of the panel label
            name        : the new name of the subtopic
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'form' : form,
            'form_title' : 'Edit Subtopic',
            'item_type' : 'subtopic',
            'item_id' : subtopic_id,
            'action_url' : reverse(
                    'edit_subtopic', 
                    kwargs={'subtopic_id':subtopic.id})
        })
        return render_to_response('organization/schema_form.html',variables)
    
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)

    if request.POST:
        form = SubtopicForm(request.POST, instance=subtopic)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'action' : 'edit',
                'label' : '#label-subtopic-{}'.format(subtopic.id),
                'name' : subtopic.name,
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(SubtopicForm(instance=subtopic))



# @login_required
def get_accordion_panel(request, item_type, item_id):
    template = "organization/accordions/{}_panel.html".format(item_type)
    Item = {
        'topic' : Topic,
        'subtopic' : Subtopic,
        'objective' : Objective,
        'question' : Question,
    }[item_type]
    item = get_object_or_404(Item, id=item_id)
    variables = RequestContext(request, {
        item_type : item,
        'schema_detail': True,
    })
    return render_to_response(template, variables)

@login_required
def add_objective(request, subtopic_id):
    pass