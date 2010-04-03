from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view

from lino.api.handlers import reporthandler_factory

auth = HttpBasicAuthentication(realm='My sample API')

#~ for a in ('contacts.Persons','contacts.Companies','projects.Projects'):
for rpt in reports.master_reports:
    rsc = Resource(handler=reporthandler_factory(rpt), authentication=auth)
    prefix = '^%s/%s' % (rpt.app_label,rpt._actor_name)
    urlpatterns += patterns('',
       url(prefix+r'/$', rsc),
       url(prefix+r'/(?P<emitter_format>.+)/$', rsc),
       url(prefix+r'\.(?P<emitter_format>.+)/$', rsc),
    )
    
    urlpatterns = patterns('',
        # automated documentation
        url(r'^$', documentation_view),
    )