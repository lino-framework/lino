"""
This is how to have Lino together with some hand-written views.
"""
from django.conf.urls.defaults import patterns, include, url

from lino.ui.extjs3 import UI

# define non-Lino urls 
urlpatterns = patterns('',
    url(r'^$', 'lino.tutorials.t2.polls.views.index'))
        
# add Lino urls under `/lino` 
urlpatterns += UI('lino').get_patterns()

