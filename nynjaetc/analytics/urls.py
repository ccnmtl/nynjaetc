from django.conf.urls.defaults import patterns, url
urlpatterns = patterns(
    '',
    url(r'^$',
        'nynjaetc.analytics.views.analytics_table',
        name="analytics_table"),

    url(r'^testing/$',
        'nynjaetc.analytics.views.analytics_table_testing',
        name="analytics_table_testing"),

    url(r'csv/$',
        'nynjaetc.analytics.views.analytics_csv',
        name="analytics_csv")
)
