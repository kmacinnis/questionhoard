from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from questions.views import *

urlpatterns = patterns('',
    # ex: /questions/
    url(
        r'^$', 
        login_required(QuestionList.as_view()), 
        name='QuestionList'
    ),
    
    # ex: /questions/5/
    url(r'^(?P<question_id>\d+)/$', detail, name='detail'),
    
    # ex: /questions/5/preview/
    url(r'^(?P<question_id>\d+)/preview/$', preview, name='preview'),
    
    # ex: /questions/5/edit/
    url(
        r'^(?P<pk>\d+)/edit/$', 
        login_required(EditQuestion.as_view()), 
        name='edit'),
    
    # ex: /questions/5/edit/
    url(
        r'^(?P<pk>\d+)/edit/$', 
        login_required(EditQuestion.as_view()), 
        name='EditQuestion'),
    
    # ex: /questions/5/edit/
    url(
        r'^(?P<pk>\d+)/edit/$', 
        login_required(EditQuestion.as_view()), 
        name='EditQuestion'),
    
    # ex: /questions/5/validate/
    url(
        r'^(?P<pk>\d+)/validate/$', 
        login_required(ValidateQuestion.as_view()), 
        name='validate'
    ),

    # ex: /questions/5/validate/
    url(
        r'^(?P<pk>\d+)/validate/$', 
        login_required(ValidateQuestion.as_view()), 
        name='ValidateQuestion'
    ),

    # ex: /questions/create/
    url(
        r'^create/$', 
        login_required(CreateQuestion.as_view()), 
        name='CreateQuestion'
    ),

    # ex: /questions/create_for_objective/345/
    url(
        r'^create_for_objective/(?P<obj_id>\d+)/$',
        login_required(CreateQuestion.as_view()), 
        name='CreateQuestion'
    ),

)

