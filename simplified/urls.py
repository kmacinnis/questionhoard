from django.conf.urls import patterns, url

from simplified.views import *

urlpatterns = patterns('',
    url(r'^$', ListFoo.as_view(), name='listfoo'),
    url(r'^(?P<pk>\d+)/edit/$', EditFoo.as_view(), name='editfoo'),
    url(r'^create/$', CreateFoo.as_view(), name='createfoo'),
    url(r'^(?P<pk>\d+)/nested/$', NestedFoo.as_view(), name='nestedfoo'),

)

