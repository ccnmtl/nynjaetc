from django.conf.urls.defaults import patterns
print "HELLO???"
urlpatterns = patterns(
    '',
    (r'$', 'nynjaetc.analytics.views.analytics_table', {}, 'analytics_table'),
)
