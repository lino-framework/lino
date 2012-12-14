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
This module deserves a better docstring.
"""

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

import lino
from urllib import urlencode
from django.conf import settings
#~ from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, include, url
from django.utils.translation import string_concat

from lino.core import actions

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
  #~ 'confirm_message', 'step',
  'thread_id',
  #~ 'dialog_fn',
  'open_url','open_davlink_url','eval_js'))
"""
Action responses supported by `Lino.action_handler` (defined in :xfile:`linolib.js`).
"""

class DialogThread(object):
    def __init__(self,yes,no):
        self.yes = yes
        self.no = no
            
        #~ d = Decision(yes,no)
        #~ self.pending_dialogs[d.hash()] = d

        
class UI:
    """
    """
    name = None
    #~ prefix = None
    verbose_name = None
    
    def __init__(self,prefix='',**options):
        self.pending_threads = {}
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
            
            
    def pop_thread(self,id):
        return self.pending_threads.pop(id,None)
        
    def abandon_response(self):
        return self.success(_("User abandoned"))
        
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
        """
        This is the method called from :mod:`lino.ui.extjs3.urls` 
        (see there for more explanations).
        """
        #~ return patterns('',(self.prefix, include(self.get_urls())))
        #~ urlpatterns = []
        #~ urlpatterns = patterns('',
            #~ (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
                #~ {'url': settings.MEDIA_URL + 'lino/favicon.ico'})
        #~ )
        urlpatterns = self.get_media_urls()
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
        
    def success(self,message=None,alert=None,**kw):
        """
        Shortcut for building a success response.
        First argument should be a textual message.
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

    def error(self,e=None,message=None,**kw):
        """
        Shortcut for building an error response.
        The first argument should be either an exception object or a message.
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
    
    def confirm(self,ok,*msgs,**kw):
        """
        Execute the specified callable `ok` after the user has confirmed 
        the specified message.
        All remaining positional arguments to `confirm` 
        are concatenated to a single prompt message.
        This method then calls :meth:`prompt` (see there for implementation notes).
        """
        return self.prompt('\n'.join([force_text(s) for s in msgs]),ok)
        
    def prompt(self,msg,yes,no=None):
        """
        Returns an action response which will initiate a dialog thread 
        by asking a question to the user and suspending execution until 
        the user's answer arrives in a next HTTP request.
        
        Implementation notes:
        Calling this from an Action's :meth:`Action.run` method will
        interrupt the execution, send the specified message back to 
        the user, adding the executables `yes` and optionally `no` to a queue 
        of pending "dialog threads".
        The client will display the prompt and will continue this thread 
        by requesting :class:`lino.ui.extjs3.views.Threads`.
        """
        if no is None:
            no = self.abandon_response
            
        d = DialogThread(yes,no)
        h  = hash(d)
        self.pending_threads[h] = d
        
        r = dict(
          success=True,
          message=msg,
          thread_id=h)
        return r # self.action_response(r)

        
    def check_action_response(self,kw):
        """
        Raise an exception if the action responded using an unknown keyword.
        """
        for k in kw.keys():
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown action response %r" % k)
                
    def action_response(self,kw):
        """
        """
        raise NotImplementedError
        
