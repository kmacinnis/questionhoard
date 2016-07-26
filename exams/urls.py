from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from exams.views import *

urlpatterns = [

    # ex: /exams/
    url(
        r'^$',
        examrecipe_list,
        name='ExamRecipeList'
    ),
    
    # ex: /exams/create/
    url(
        r'^create/$', 
        login_required(CreateExamRecipe.as_view()), 
        name='CreateExamRecipe'
    ),

    # ex: /exams/create/course/56/
    url(
        r'^create/course/(?P<course_id>\d+)/$',
        login_required(CreateExamRecipe.as_view()),
        name='CreateExamRecipeForCourse'
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
    
    # ex: /exams/1/update_exam_part/
    url(
        r'^(?P<pk>\d+)/update_exam_part/$',
        login_required(UpdatePartRecipe.as_view()),
        name='UpdatePartRecipe'
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
    ),
    
    #ex: /exams/preferences/
    url(
        r'^preferences/$',
        set_preferences,
        name='set_preferences'
    ),
    
    # ex: /exams/add_question_to_exam/
    url(
        r'^add_question_to_exam/$',
        add_question_to_exam,
        name='add_question_to_exam'
    ),
    
    # ex: /exams/remove_item_from_exam/
    url(
        r'^remove_item_from_exam/$',
        remove_item_from_exam,
        name='remove_item_from_exam'
    ),
    
    # ex: /exams/pool/
    url(
        r'^pool/$',
        focus_pool,
        name='focus_pool'
    ),
    
    # ex: /exams/edit_item/123/
    url(
        r'^edit_item/(?P<item_id>\d+)/$',
        edit_item,
        name = 'EditExamItem'
    ),
    
]

