from django.conf.urls import patterns, url


from practicedocs.views import *

urlpatterns = [

    # ex: /practicedocs/
    url(r'^$', DocRecipeList.as_view(), name='DocRecipeList'),

    # ex: /practicedocs/doclist/
    url(r'^doclist/$', DocList.as_view(), name='DocList'),

    # ex: /practicedocs/5/
    url(r'^(?P<pk>\d+)/$', DocRecipeDetail.as_view(), name='DocRecipeDetail'),

    # ex: /practicedocs/5/generate/
    url(r'^(?P<recipe_id>\d+)/generate/$', generate_document, name='GenerateDoc'),

    # ex: /practicedocs/5/edit/
    url(r'^(?P<pk>\d+)/edit/$', EditDocRecipe.as_view(), name='EditDocRecipe'),
    
    # ex: /practicedocs/create/
    url(r'^create/$', CreateDocRecipe.as_view(), name='CreateDocRecipe'),
    
    # ex: /practicedocs/viewdoc/5/
    url(r'^viewdoc/(?P<document_id>\d+)/(?P<filetype>\w+)/$', view_document, name='ViewDoc'),

    # ex: /practicedocs/new_blockrecipe_form/
    url(r'^new_blockrecipe_form/$', ajax_add_blockrecipe),
]

