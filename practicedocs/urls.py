from django.conf.urls import patterns, url


from practicedocs.views import *

urlpatterns = patterns('',

    # ex: /practicedocs/
    url(r'^$', DocRecipeList.as_view(), name='DocRecipeList'),

    # ex: /practicedocs/doclist/
    url(r'^doclist/$', DocList.as_view(), name='DocList'),

    # ex: /practicedocs/5/
    url(r'^(?P<pk>\d+)/$', DocRecipeDetail.as_view(), name='DocRecipeDetail'),

    # ex: /practicedocs/5/generate/
    url(r'^(?P<recipe_id>\d+)/generate/$', generate_document, name='GenerateDoc'),

    # ex: /practicedocs/5/edit/
    url(r'^(?P<recipe_id>\d+)/edit/$', edit_recipe, name='EditRecipe'),
    
    # ex: /practicedocs/create/
    url(r'^create/$', CreateDocRecipe.as_view(), name='CreateDocRecipe'),
    
    # ex: /practicedocs/viewdoc/5
    url(r'^viewdoc/(?P<document_id>\d+)/(?P<filetype>\w+)/$', view_document, name='ViewDoc'),
)

