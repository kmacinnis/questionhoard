from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView
from utils import views as zviews





admin.autodiscover()

urlpatterns = [

    url(r'^questions/', include('questions.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', zviews.main_page),
    url(r'^login/$', login),
    url(r'^accounts/login/$', login),
    url(r'^logout/$', zviews.logout_page),
    url(r'^register/$', zviews.register_page),
    url(r'^register/success/$',
        TemplateView.as_view(template_name='registration/register_success.html')),
    url(r'^temp/', zviews.temp),
    url(r'^not_implemented_yet/$', zviews.not_implemented, name="NotImplemented"),
    
    url(r'^practicedocs/', include('practicedocs.urls')),
    url(r'^organization/', include('organization.urls')),
    # url(r'^org/', include('organization.urls')),
    url(r'^exams/', include('exams.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
