from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$',
        'nynjaetc.treatment_activity.views.choose_treatment_path',
        name='choose-treatment-path'),

    url(r'^(?P<path_id>\d+)/(?P<node_id>\d+)/$',
        'nynjaetc.treatment_activity.views.get_next_steps',
        name="get-next-steps")
)
