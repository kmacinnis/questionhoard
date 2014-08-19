from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from organization.views import *
import zother.views as zviews

urlpatterns = patterns('',

    # ex: /organization/topics/
    url(r'^topics/$', TopicList.as_view(), name='TopicList'),
    
    # ex: /organization/courses/
    url(
        r'^courses/$',
        course_list,
        name='course_list'
    ),
    
    # ex: /organization/courses/create/
    url(
        r'^courses/create/$',
        login_required(CreateCourse.as_view()),
        name='CreateCourse'
    ),

    # ex: /organization/courses/details/5/
    url(
        r'^course/(?P<pk>\d+)/details/$',
        login_required(CourseDetails.as_view()),
        name='CourseDetails'
    ),

    # ex: /organization/course/5/edit/
    url(
        r'^course/(?P<pk>\d+)/edit/$',
        login_required(EditCourseDetails.as_view()),
        name='EditCourseDetails'
    ),

    # ex: /organization/schema/
    url(
        r'^schema/$',
        login_required(SchemaList.as_view()),
        name='SchemaList'
    ),

    # ex: /organization/schema/create/
    url(
        r'^schema/create/$',
        login_required(CreateSchema.as_view()),
        name='CreateSchema'
    ),

    # ex: /organization/schema/5/details/
    url(
        r'^schema/(?P<pk>\d+)/details/$',
        login_required(SchemaDetails.as_view()),
        name='SchemaDetails'
    ),

    # ex: /organization/schema/5/edit/
    url(
        r'^schema/(?P<pk>\d+)/edit/$',
        login_required(EditSchema.as_view()),
        name='EditSchema'
    ),
    
    # ex: /organization/schema/5/add_questions/
    url(
        r'^schema/(?P<pk>\d+)/add_questions/$',
        login_required(SchemaWithQuestions.as_view()),
        name='SchemaWithQuestions'
    ),

    # ex: /organization/schema/1/add_topic/
    url(
        r'^schema/(?P<schema_id>\d+)/add_topic/$',
        add_topic,
        name='add_topic'
    ),
    
    # ex: /organization/topic/1/add_subtopic/
    url(
        r'^topic/(?P<topic_id>\d+)/add_subtopic/$',
        add_subtopic,
        name='add_subtopic'
    ),
    
    # ex: /organization/topic/1/edit/
    url(
        r'^topic/(?P<topic_id>\d+)/edit/$',
        edit_topic,
        name='edit_topic'
    ),
    
    # ex: /organization/subtopic/1/edit/
    url(
        r'^subtopic/(?P<subtopic_id>\d+)/edit/$',
        edit_subtopic,
        name='edit_subtopic'
    ),
    
    # ex: /organization/subtopic/1/add_objective/
    url(
        r'^subtopic/(?P<subtopic_id>\d+)/add_objective/$',
        add_objective,
        name='add_objective'
    ),
    
    # ex: /organization/get_accordion_panel/topic/1/
    url(
        r'^get_accordion_panel/(?P<item_type>\w+)/(?P<item_id>\d+)/$',
        get_accordion_panel,
        name='get_accordion_panel'
    ),
    
    # ex: /organization/delete_item/topic/1/
    url(
        r'^delete_item/(?P<item_type>\w+)/(?P<item_id>\d+)/$',
        delete_item,
        name='delete_item'
    ),
)
