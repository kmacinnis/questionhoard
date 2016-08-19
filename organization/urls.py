from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from organization.views import *
import zother.views as zviews

urlpatterns = [

    # ex: /organization/chapters/
    url(r'^chapters/$', ChapterList.as_view(), name='ChapterList'),
    
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

    # ex: /organization/book/
    url(
        r'^book/$',
        login_required(BookList.as_view()),
        name='BookList'
    ),

    # ex: /organization/book/create/
    url(
        r'^book/create/$',
        login_required(CreateBook.as_view()),
        name='CreateBook'
    ),

    # ex: /organization/book/5/details/
    url(
        r'^book/(?P<pk>\d+)/details/$',
        login_required(BookDetails.as_view()),
        name='BookDetails'
    ),

    # ex: /organization/book/5/edit/
    url(
        r'^book/(?P<pk>\d+)/edit/$',
        login_required(EditBook.as_view()),
        name='EditBook'
    ),
    
    # ex: /organization/book/5/add_questions/
    url(
        r'^book/(?P<pk>\d+)/add_questions/$',
        login_required(BookWithQuestions.as_view()),
        name='BookWithQuestions'
    ),

    # ex: /organization/book/5/edit_and_add_questions/
    url(
        r'^book/(?P<pk>\d+)/edit_and_add_questions/$',
        login_required(EditBookWithQuestions.as_view()),
        name='EditBookWithQuestions'
    ),

    # ex: /organization/book/1/add_chapter/
    url(
        r'^book/(?P<book_id>\d+)/add_chapter/$',
        add_chapter,
        name='add_chapter'
    ),
    
    # ex: /organization/chapter/1/add_section/
    url(
        r'^chapter/(?P<chapter_id>\d+)/add_section/$',
        add_section,
        name='add_section'
    ),
    
    # ex: /organization/chapter/1/edit/
    url(
        r'^chapter/(?P<chapter_id>\d+)/edit/$',
        edit_chapter,
        name='edit_chapter'
    ),
    
    # ex: /organization/section/1/edit/
    url(
        r'^section/(?P<section_id>\d+)/edit/$',
        edit_section,
        name='edit_section'
    ),
    
    # ex: /organization/section/1/add_objective/
    url(
        r'^section/(?P<section_id>\d+)/add_objective/$',
        add_objective,
        name='add_objective'
    ),

    # ex: /organization/objective/1/edit/
    url(
        r'^objective/(?P<objective_id>\d+)/edit/$',
        edit_objective,
        name='edit_objective'
    ),
    
    # ex: /organization/get_accordion_panel/chapter/1/
    url(
        r'^get_accordion_panel/(?P<item_type>\w+)/(?P<item_id>\d+)/$',
        get_accordion_panel,
        name='get_accordion_panel'
    ),
    
    # ex: /organization/delete_item/chapter/1/
    url(
        r'^delete_item/(?P<item_type>\w+)/(?P<item_id>\d+)/$',
        delete_item,
        name='delete_item'
    ),
    
    # ex: /organization/course/1/related_courses/
    url(
        r'^course/(?P<course_id>\d+)/related_courses/$',
        related_courses,
        name='related_courses'
    )
]
