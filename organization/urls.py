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
        name='CourseDetails'
    ),
)
