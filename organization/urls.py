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

    # ex: /organization/courses/
    url(
        r'organization/courses/details/(?P<pk>\d+)/',
        login_required(CourseDetails.as_view()),
        name='CourseDetails'
    ),
)
