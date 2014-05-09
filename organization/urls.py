from django.conf.urls import patterns, url

from organization.views import *

urlpatterns = patterns('',
    url(r'^topics/$', TopicList.as_view(), name='TopicList'),
)