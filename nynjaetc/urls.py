import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_change, password_change_done, \
    password_reset, password_reset_done, password_reset_complete, \
    password_reset_confirm
from django.views.generic import TemplateView
from registration.backends.default.views import ActivationView

import nynjaetc.main.regviews as regviews
import nynjaetc.main.views as views


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'CAS_BASE'):
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

    # override the default urls for password
    url(r'^password/change/$',
        password_change,
        name='password_change'),
    url(r'^password/change/done/$',
        password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        name='password_reset_confirm'),

    # have to pull in a bunch of registration's urls
    # so we can override one. :(
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^accounts/register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^accounts/register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'),
        name='registration_disallowed'),
    (r'^accounts/', include('registration.auth_urls')),
    url(r'^accounts/register/$', regviews.RegistrationView.as_view(),
        name='registration_register'),

    (r'^resend_activation_email/$', views.ResendActivationEmailView.as_view()),

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
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # these need to be last
    (r'^edit/(?P<path>.*)$', views.EditView.as_view(),
     {}, 'edit-page'),
    (r'^latest/(?P<path>.*)$', views.LatestPageView.as_view(),
     {}, 'latest-page'),
    (r'^record_section_as_answered_correctly/$',
     views.RecordSectionAsAnsweredCorrectlyView.as_view(),
     {}, 'record_section_as_answered_correctly'),
    (r'^(?P<path>.*)$', views.PageView.as_view()),
)
