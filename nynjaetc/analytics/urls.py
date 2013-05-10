from django.conf.urls.defaults import patterns
urlpatterns = patterns(
    '',
    (r'$', 'nynjaetc.analytics.views.analytics_table', {}, 'analytics_table'),
)
