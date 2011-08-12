from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', 'lino.tutorials.t2.views.index'),

    # Uncomment the next line to enable the admin:
    url(r'^lino/', include('lino.ui.extjs3.urls')),
)