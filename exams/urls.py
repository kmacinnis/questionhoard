from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from exams.views import *

urlpatterns = patterns('',

    # ex: /exams/
    url(
        r'^$',
        login_required(ExamRecipeList.as_view()),
        name='ExamRecipeList'
    ),
    
    # ex: /exams/create/
    url(
        r'^create/$', 
        login_required(CreateExamRecipe.as_view()), 
        name='CreateExamRecipe'
    ),

    # ex: /exams/5/
    url(
        r'^(?P<pk>\d+)/$',
        login_required(ExamRecipeDetail.as_view()),
        name='ExamRecipeDetail'
    ),

    # ex: /exam/5/generate/
    url(
        r'^(?P<recipe_id>\d+)/generate/$',
        generate_exam,
        name='GenerateExam'
    ),

    # ex: /exams/5/edit/
    url(
        r'^(?P<pk>\d+)/edit/$',
        login_required(EditExamRecipe.as_view()),
        name='EditExamRecipe'
    ),

    # ex: /exams/5/add_part/
    url(
        r'^(?P<exam_id>\d+)/add_part/$',
        login_required(CreateExamPartRecipe.as_view()),
        name='CreateExamPartRecipe'
    ),

    # ex: /exams/1/edit_exam_part/
    url(
        r'^(?P<pk>\d+)/edit_exam_part/$',
        login_required(EditPartRecipe.as_view()),
        name='EditPartRecipe'
    ),
    url(
        r'^(?P<pk>\d+)/edit-exam-part/$',
        login_required(EditPartRecipe.as_view()),
    ),
    
    # ex: /exams/partrecipe/5/add_pool/
    url(
        r'^partrecipe/(?P<part_recipe_id>\d+)/add_pool/$',
        login_required(AddPool.as_view()),
        name='AddPoolToPart'
    ),
    
    # ex: /exams/pool/5/
    url(
        r'^pool/(?P<pk>\d+)/$',
        login_required(EditPool.as_view()),
        name='EditPool'
    ),
    
    
    # ex: /exams/new_erq_form/
    url(r'^new_erq_form/$', ajax_add_examrecipequestion),
    
    # ex: /exams/1/view_exam_part/5/
    url(
        r'^(?P<exam_recipe_id>\d+)/view_exam_part/(?P<pk>\d+)/$', 
        login_required(PartRecipeDetail.as_view()), 
        name='PartRecipeDetail'
    ),
    
    
    # ex: /exams/viewexam/5/tex/
    # ex: /exams/viewexam/5/pdf/
    url(
        r'^viewdoc/(?P<exam_id>\d+)/(?P<filetype>\w+)/$', 
        view_exam, 
        name='ViewExam'
    ),
    
    # ex: /exams/unfreeze/5/
    url(
        r'^unfreeze/(?P<exam_recipe_id>\d+)/(?P<action>\w+)/$',
        unfreeze_exam_recipe,
        name='UnfreezeRecipe'
    ),
    
    # ex: /exams/duplicate_recipe/5/
    url(
        r'^duplicate_recipe/(?P<recipe_id>\d+)/$',
        duplicate_exam_recipe,
        name='DuplicateExamRecipe',
    ),
    
    # ex: /exams/ajax_add_question_to_pool/
    url(
        r'^ajax_add_question_to_pool/$',
        ajax_add_question_to_pool
    ),
    
    # ex: /exams/ajax_remove_question_from_pool/
    url(
        r'^ajax_remove_question_from_pool/$',
        ajax_remove_question_from_pool
    )
    
    
)

