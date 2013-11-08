## Copyright 2009-2013 Luc Saffre
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

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)
import os

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


from django.conf import settings

from django.db import models
from djangosite.dbutils import obj2unicode

from lino.core.requests import BaseRequest


class Handle:
  
    def __init__(self):
        self.ui = settings.SITE.ui
        
    def setup(self,ar):
        self.ui.setup_handle(self,ar)
        #~ settings.SITE.ui.setup_handle(self,ar)


ACTION_RESPONSES = frozenset((
  'message','success','alert', 
  'errors',
  'html',
  'goto_record_id',
  'refresh','refresh_all',
  'close_window',
  'xcallback',
  'open_url','open_davlink_url',
  #~ 'console_message',
  'info_message',
  'warning_message',
  'eval_js'))
"""
Action responses supported by `Lino.action_handler` (defined in :xfile:`linolib.js`).
"""

class CallbackChoice(object):
    #~ def __init__(self,name,label,func):
    def __init__(self,name,func,label):
        self.name = name
        #~ self.index = index
        self.func = func
        self.label = label
        
class Callback(object):
    """
    A callback is a question that rose during an AJAX action.
    The original action is pending until we get a request 
    that answers the question.
    """
    title = _('Confirmation')
    #~ def __init__(self,yes,no):
    def __init__(self,message):
    #~ def __init__(self,message,answers,labels=None):
        self.message = message
        self.choices = []
        self.choices_dict = {}
        #~ self.answers = {}
        #~ self.labels = labels
        #~ self.yes = yes
        #~ self.no = no
            
        #~ d = Decision(yes,no)
        #~ self.pending_dialogs[d.hash()] = d
        
    def __repr__(self):
		return "Callback(%r)" % self.message
		
    def set_title(self,title):
        self.title = title
        
    def add_choice(self,name,func,label):
        """
        Add a possible answer to this callback.
        - name: "yes", "no", "ok" or "cancel"
        - func: a callable to be executed when user selects this choice
        - the label of the button
        """
        assert not self.choices_dict.has_key(name)
        allowed_names = ("yes", "no", "ok", "cancel")
        if not name in allowed_names:
            raise Exception("Sorry, name must be one of %s" % allowed_names)
        cbc = CallbackChoice(name,func,label)
        self.choices.append(cbc)
        self.choices_dict[name] = cbc
        return cbc

#~ pending_threads = {}
        
class UI(object):
    """
    Base class for UI plugins.
    """
    #~ name = None
    #~ prefix = None
    #~ verbose_name = None
    
    def __init__(self,site):
        self.pending_threads = {}
        self.site = site
            
    #~ def pop_thread(self,id):
        #~ return self.pending_threads.pop(id,None)
        
    def abandon_response(self):
        return self.success(_("User abandoned"))
        
    #~ def build_admin_url(self,*args,**kw):
        #~ return settings.SITE.build_admin_url(*args,**kw)
        
    #~ def media_url(self,*args,**kw):
        #~ return settings.SITE.media_url(*args,**kw)
        
    def get_urls(self):
        raise NotImplementedError()
        

    def field2elem(self,lui,field,**kw):
        pass
        
    def setup_handle(self,h,ar):
        pass
    
        
    def get_callback(self,request,thread_id,button_id):
        """
        Return an existing (pending) callback. 
        This is called from `lino.ui.views.Callbacks`.
        """
        #~ logger.info("20130409 get_callback")
        ar = BaseRequest(request)
        thread_id = int(thread_id)
        cb = self.pending_threads.pop(thread_id,None)
        #~ d = self.pop_thread(int(thread_id))
        if cb is None: 
            #~ logger.info("20130811 No callback %r in %r" % (thread_id,self.pending_threads.keys()))
            ar.error("Unknown callback %r" % thread_id)
            return self.render_action_response(ar.response)
        #~ buttonId = request.GET[ext_requests.URL_PARAM_'bi']
        #~ print buttonId
        for c in cb.choices:
            if c.name == button_id:
                #~ rv = c.func(request)
                c.func(ar)
                return self.render_action_response(ar.response)
                
        ar.error("Invalid button %r for callback" % (button_id,thread_id))
        return self.render_action_response(ar.response)
                
        #~ m = getattr(d,button_id)
        #~ rv = m(request)
        #~ if button_id == 'yes':
            #~ rv = d.yes()
        #~ elif button_id == 'no':
            #~ rv = d.no()
        #~ return self.render_action_response(rv)
  
    def add_callback(self,ar,*msgs):
        """
        Returns an "action callback" which will initiate a dialog thread 
        by asking a question to the user and suspending execution until 
        the user's answer arrives in a next HTTP request.
        
        Implementation notes:
        Calling this from an Action's :meth:`Action.run` method will
        interrupt the execution, send the specified message back to 
        the user, adding the executables `yes` and optionally `no` to a queue 
        of pending "dialog threads".
        The client will display the prompt and will continue this thread 
        by requesting :class:`lino.ui.extjs3.views.Callbacks`.
        """
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]
            
        return Callback(msg)
        
        
    def set_callback(self,ar,cb):
        """
        """
        h = hash(cb)
        self.pending_threads[h] = cb
        #~ logger.info("20130531 Stored %r in %r" % (h,settings.SITE.pending_threads))
        
        buttons = dict()
        for c in cb.choices:
            buttons[c.name] = c.label
            
        ar.response.update(
          success=True,
          message=cb.message,
          xcallback=dict(id=h,
              title=cb.title,
              buttons=buttons))
          
            
    def check_action_response(self,rv):
        """
        Raise an exception if the action responded using an unknown keyword.
        """
        
        #~ if rv is None:
            #~ rv = self.success()
            
        #~ elif isinstance(rv,Callback):
          
        for k in rv.keys():
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown key %r in action response." % k)
        return rv
                
    def render_action_response(self,kw):
        """
        """
        raise NotImplementedError
        
    def run_action(self,ar):
        """
        """
        try:
            ar.bound_action.action.run_from_ui(ar)
            return self.render_action_response(ar.response)
        except Warning as e:
            ar.error(unicode(e),alert=True)
            #~ r = dict(
              #~ success=False,
              #~ message=unicode(e),
              #~ alert=True)
            return self.render_action_response(ar.response)
        #~ removed 20130913
        #~ except Exception as e:
            #~ if len(ar.selected_rows) == 0:
                #~ msg = unicode(e)
            #~ else:
                #~ elem = ar.selected_rows[0]
                #~ if isinstance(elem,models.Model):
                    #~ elem = obj2unicode(elem)
                #~ msg = _(
                  #~ "Action \"%(action)s\" failed for %(record)s:") % dict(
                  #~ action=ar.bound_action.full_name(),
                  #~ record=elem)
                #~ msg += "\n" + unicode(e)
            #~ msg += '.\n' + unicode(_(
              #~ "An error report has been sent to the system administrator."))
            #~ logger.warning(msg)
            #~ logger.exception(e)
            #~ r = self.error(e,msg,alert=_("Oops!"))
            #~ return self.render_action_response(r)
              

