## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This is not a docstring.
"""

from django.utils.translation import ugettext_lazy as _

import lino
from urllib import urlencode
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url


class Handle:
  
    def __init__(self,ui):
        self.ui = ui
        
    def setup(self,ar):
        if self.ui is not None:
            self.ui.setup_handle(self,ar)


ACTION_RESPONSES = frozenset((
  'message','success','alert', 
  'errors',
  'html',
  #~ 'new_status',
  'goto_record_id',
  'refresh','refresh_all',
  'confirm_message', 'step','dialog_fn',
  'open_url','open_davlink_url','eval_js'))
"""
Action responses supported by `Lino.action_handler` (defined in :xfile:`linolib.js`).
"""


        
class UI:
    """
    """
    name = None
    #~ prefix = None
    verbose_name = None
    
    def __init__(self,prefix='',**options):
        #~ 20120614 settings.LINO.setup(**options)
        assert isinstance(prefix,basestring)
        assert len(prefix) == 0, "no longer supported"
        assert len(options) == 0, "no longer supported"
        #~ self.prefix = prefix
        #~ self.admin_url = settings.LINO.admin_url
        #~ if prefix:
            #~ assert not prefix.startswith('/')
            #~ assert not prefix.endswith('/')
            #~ self.admin_url += '/' + prefix
        
        
    def build_url(self,*args,**kw):
        #~ url = self.admin_url
        url = settings.LINO.admin_url
        if args:
            url += '/' + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def media_url(self,*args,**kw):
        url = '/media'
        if args:
            url += '/' + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url
      
        #~ return self.build_url('media',*args,**kw)
        
    def old_get_patterns(self):
        urlpatterns = patterns('',
            (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
                {'url': settings.MEDIA_URL + 'lino/favicon.ico'})
        )
        if self.prefix:
            urlpatterns += patterns('',
              ('^'+self.prefix+"/", include(self.get_urls()))
            )
        else:
            urlpatterns += self.get_urls()
        return urlpatterns
        
    def get_patterns(self):
        #~ return patterns('',(self.prefix, include(self.get_urls())))
        urlpatterns = patterns('',
            (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
                {'url': settings.MEDIA_URL + 'lino/favicon.ico'})
        )
        urlpatterns += self.get_media_urls()
        if settings.LINO.admin_url:
        #~ if self.prefix:
            from lino.ui.extjs3 import views
            urlpatterns += patterns('',
                ('^$', views.WebIndex.as_view()),
                ('^(?P<ref>\w+)$', views.WebIndex.as_view()),
            )
            urlpatterns += patterns('',
              ('^'+settings.LINO.admin_url[1:]+"/", include(self.get_urls()))
            )
        else:
            urlpatterns += self.get_urls()
        return urlpatterns
        
    def get_urls():
        raise NotImplementedError()
        

    def field2elem(self,lui,field,**kw):
        pass
        
    def setup_handle(self,h,ar):
        pass
        
    def request(self,actor,**kw):
        if isinstance(actor,basestring):
            actor = settings.LINO.modules.resolve(actor)
        #~ kw.update(ui=self)
        return actor.request(self,**kw)
        
    def check_action_response(self,kw):
        """
        Raise an exception if the action responded using an unknown keyword.
        """
        for k in kw.keys():
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown action response %r" % k)
                
    def success_response(self,message=None,alert=None,**kw):
        """
        Shortcut for building a success response.
        """
        kw.update(success=True)
        if alert is not None:
            if alert is True:
                alert = _("Success")
            kw.update(alert=alert)
        if message:
            kw.update(message=message)
        #~ return self.action_response(kw)
        return kw

    def error_response(self,e=None,message=None,**kw):
        """
        Shortcut for building an error response.
        """
        kw.update(success=False)
        #~ if e is not None:
        if isinstance(e,Exception):
            if False: # useful when debugging, but otherwise rather disturbing
                logger.exception(e)
            if hasattr(e,'message_dict'):
                kw.update(errors=e.message_dict)
        if message is None:
            message = unicode(e)
        kw.update(message=message)
        #~ return self.action_response(kw)
        return kw
    
    def action_response(self,kw):
        """
        """
        raise NotImplementedError
        
