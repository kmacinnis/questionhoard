from django.conf.urls import patterns, url

from questions.views import *

urlpatterns = patterns('',
    # ex: /questions/
    url(r'^$', index, name='QuestionList'),
    # ex: /questions/mathjax
    url(r'^mathjax$', mathjaxtest, name='mathjaxtest'),
    # ex: /questions/5/
    url(r'^(?P<question_id>\d+)/$', detail, name='detail'),
    # ex: /questions/5/preview/
    url(r'^(?P<question_id>\d+)/preview/$', preview, name='preview'),
    # ex: /questions/5/edit/
    url(r'^(?P<pk>\d+)/edit/$', EditQuestion.as_view(), name='edit'),
    # ex: /questions/5/validate/
    url(r'^(?P<pk>\d+)/validate/$', ValidateQuestion.as_view(), name='validate'),

    # ex: /questions/create/
    url(r'^create/$', CreateQuestion.as_view(), name='create'),
    # ex: /questions/create/obj12345/
    url(r'^create/obj(?P<obj_id>\d+)/$', 
            CreateQuestion.as_view(), name='create_question_for_objective'),



    # ex: /questions/justcreate
    # url(r'^justcreate', views.create_just_question, name='justcreate'),
    # # ex: /questions/5/vote/
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)

