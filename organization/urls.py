from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from organization.views import *

urlpatterns = patterns('',

    # ex: /organization/topics/
    url(r'^topics/$', TopicList.as_view(), name='TopicList'),
    
    # ex: /organization/courses/create/
    url(
        r'courses/create/',
        login_required(CreateCourse.as_view()),
        name='CreateCourse'
    ),

    # ex: /organization/courses/details/5/
    url(
        r'courses/details/(?P<pk>\d+)/',
        login_required(CourseDetails.as_view()),
        name='CourseDetails'
    ),

    # ex: /organization/schema/details/5/
    url(
        r'schema/details/(?P<pk>\d+)/',
        login_required(SchemaDetails.as_view()),
        name='SchemaDetails'
    ),

    # ex: /organization/schema/1/add_topic/
    url(
        r'schema/(?P<schema_id>\d+)/add_topic/',
        add_topic,
        name='add_topic'
    ),
    
    # ex: /organization/topic/1/add_subtopic/
    url(
        r'topic/(?P<topic_id>\d+)/add_subtopic/',
        add_subtopic,
        name='add_subtopic'
    )
    

)
