from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

import nynjaetc.main.views as views

import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^_pagetree/', include('pagetree.urls')),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^_rgt/', include('nynjaetc.treatment_activity.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^analytics/', include('nynjaetc.analytics.urls')),

    ('^about/$', 'nynjaetc.main.views.background',
     {'content_to_show': 'about'}),
    ('^help/$', 'nynjaetc.main.views.background',
     {'content_to_show': 'help'}),
    ('^contact/$', 'nynjaetc.main.views.background',
     {'content_to_show': 'contact'}),
    ('^credits/$', 'nynjaetc.main.views.background',
     {'content_to_show': 'credits'}),

    (r'^accounts/', include('registration.backends.default.urls')),

    (r'^resend_activation_email/$',
     'nynjaetc.main.views.resend_activation_email'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),

    (r'manage/$', TemplateView.as_view(template_name='main/manage.html')),
    (r'manage/altnav/$', views.AltNavListView.as_view()),
    (r'manage/altnav/add/$', views.CreateAltNavView.as_view()),
    (r'manage/altnav/(?P<pk>\d+)/delete/$', views.DeleteAltNavView.as_view()),

    (r'manage/secpref/$', views.SecPrefListView.as_view()),
    (r'manage/secpref/add/$', views.CreateSecPrefView.as_view()),
    (r'manage/secpref/(?P<pk>\d+)/delete/$',
     views.DeleteSecPrefView.as_view()),

    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # old cloned hierarchy
    (r'^old/edit/(?P<path>.*)$', views.EditView.as_view(
        hierarchy_name="old",
        hierarchy_base="/old/"),
     {}, 'edit-page'),
    (r'^old/latest/(?P<path>.*)$', views.LatestPageView.as_view(
        hierarchy_name="old",
        hierarchy_base="/old/"),
     {}, 'latest-page'),
    (r'^old/record_section_as_answered_correctly/$',
     views.RecordSectionAsAnsweredCorrectlyView.as_view(),
     {}, 'record_section_as_answered_correctly'),
    (r'^old/(?P<path>.*)$', views.PageView.as_view(
        hierarchy="old")),

    # these need to be last
    (r'^edit/(?P<path>.*)$', views.EditView.as_view(),
     {}, 'edit-page'),
    (r'^latest/(?P<path>.*)$', views.LatestPageView.as_view(),
     {}, 'latest-page'),
    (r'^record_section_as_answered_correctly/$',
     views.RecordSectionAsAnsweredCorrectlyView.as_view(),
     {}, 'record_section_as_answered_correctly'),
    (r'^(?P<path>.*)$', views.PageView.as_view()),
) + staticmedia.serve()
