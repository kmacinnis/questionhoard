from django.shortcuts import render

from vanilla import ListView



from organization.models import *



class TopicList(ListView):
    model = Topic
    context_object_name = 'topics'


