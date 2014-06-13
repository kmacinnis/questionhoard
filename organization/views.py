from django.shortcuts import render

from vanilla import ListView



from organization.models import *



class TopicList(ListView):
    model = Topic
    context_object_name = 'topics'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_question_links'] = True
        return context


