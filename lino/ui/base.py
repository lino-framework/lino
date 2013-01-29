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

import logging
logger = logging.getLogger(__name__)
import os

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


import lino
from urllib import urlencode
from django.conf import settings
#~ from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, include, url
from django.utils.translation import string_concat

from django.utils.translation import get_language


#~ from django import http
#~ from django.views.generic import View


from lino.core import actions
from lino.core import web


from lino.core.modeltools import resolve_app
from lino.core.modeltools import is_devserver


#~ from django.conf.urls.defaults import patterns, url, include


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
  'xcallback',
  #~ 'thread_id',
  #~ 'dialog_fn',
  'open_url','open_davlink_url','eval_js'))
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

        
class UI(object):
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
            
            
    #~ def pop_thread(self,id):
        #~ return self.pending_threads.pop(id,None)
        
    def abandon_response(self):
        return self.success(_("User abandoned"))
        
    #~ def build_admin_url(self,*args,**kw):
        #~ return settings.LINO.build_admin_url(*args,**kw)
        
    #~ def media_url(self,*args,**kw):
        #~ return settings.LINO.media_url(*args,**kw)
        
    def unused_get_plain_urls(self):
        from lino.ui.extjs3 import views

        urlpatterns = []
        rx = '^' # + settings.LINO.plain_prefix
        urlpatterns = patterns('',
            (rx+r'$', views.PlainIndex.as_view()),
            (rx+r'(?P<app_label>\w+)/(?P<actor>\w+)$', views.PlainList.as_view()),
            (rx+r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.PlainElement.as_view()),
        )
        return urlpatterns
      
    def unused_get_media_urls(self):
        #~ print "20121110 get_urls"
        urlpatterns = []
        from os.path import exists, join, abspath, dirname
        
        logger.info("Checking /media URLs ")
        prefix = settings.MEDIA_URL[1:]
        assert prefix.endswith('/')
        
        def setup_media_link(short_name,attr_name=None,source=None):
            target = join(settings.MEDIA_ROOT,short_name)
            if exists(target):
                return
            if attr_name:
                source = getattr(settings.LINO,attr_name)
                if not source:
                    raise Exception(
                      "%s does not exist and LINO.%s is not set." % (
                      target,attr_name))
            if not exists(source):
                raise Exception("LINO.%s (%s) does not exist" % (attr_name,source))
            if is_devserver():
                urlpatterns.extend(patterns('django.views.static',
                (r'^%s%s/(?P<path>.*)$' % (prefix,short_name), 
                    'serve', {
                    'document_root': source,
                    'show_indexes': False })))
            else:
                logger.info("Setting up symlink %s -> %s.",target,source)
                symlink = getattr(os,'symlink',None)
                if symlink is not None:
                    symlink(source,target)
            
        if not settings.LINO.extjs_base_url:
            setup_media_link('extjs','extjs_root')
        if settings.LINO.use_bootstrap:
            setup_media_link('bootstrap','bootstrap_root')
        if settings.LINO.use_jasmine:
            setup_media_link('jasmine','jasmine_root')
        if settings.LINO.use_extensible:
            setup_media_link('extensible','extensible_root')
        if settings.LINO.use_tinymce:
            setup_media_link('tinymce','tinymce_root')
        if settings.LINO.use_eid_jslib:
            setup_media_link('eid-jslib','eid_jslib_root')
            
        setup_media_link('lino',source=join(dirname(lino.__file__),'..','media'))

        if is_devserver():
            urlpatterns += patterns('django.views.static',
                (r'^%s(?P<path>.*)$' % prefix, 'serve', 
                  { 'document_root': settings.MEDIA_ROOT, 
                    'show_indexes': True }),
            )

        return urlpatterns
        
        
    def unused_get_patterns(self):
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
        
        if settings.LINO.plain_prefix:
            urlpatterns += patterns('',
              ('^'+settings.LINO.plain_prefix[1:]+"/", include(self.get_plain_urls()))
            )
        if settings.LINO.django_admin_prefix:
            from django.contrib import admin
            admin.autodiscover()
            urlpatterns += patterns('',
              ('^'+settings.LINO.django_admin_prefix[1:]+"/", include(admin.site.urls))
            )
           
        if settings.LINO.admin_prefix:
        
            urlpatterns += patterns('',
              ('^'+settings.LINO.admin_prefix[1:]+"/", include(self.get_urls()))
            )
            
            pages = resolve_app('pages')

            class PagesIndex(View):
              
                def get(self, request,ref='index'):
                    if not ref: 
                        ref = 'index'
                  
                    #~ print 20121220, ref
                    obj = pages.lookup(ref,None)
                    if obj is None:
                        raise http.Http404("Unknown page %r" % ref)
                    html = pages.render_node(request,obj)
                    return http.HttpResponse(html)

            urlpatterns += patterns('',
                (r'^(?P<ref>\w*)$', PagesIndex.as_view()),
            )
        else:
            urlpatterns += self.get_urls()
        return urlpatterns
        
    def get_urls(self):
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
    
    def confirm(self,ok_func,*msgs,**kw):
        """
        Execute the specified callable `ok` after the user has confirmed 
        the specified message.
        All remaining positional arguments to `confirm` 
        are concatenated to a single callback message.
        This method then calls :meth:`callback` (see there for implementation notes).
        
        The callable may not expect any mandatory arguments
        (this is different than for the raw callback method)
        
        """
        cb = self.callback(*msgs)
        def noop():
            return dict(success=True,message=_("Aborted"))
        #~ def func(request):
            #~ return ok_func()
        cb.add_choice('yes',ok_func,_("Yes"))
        cb.add_choice('no',noop,_("No"))
        return cb
        
    #~ def callback(self,msg,yes,no=None):
    def callback(self,*msgs):
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
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]
        return Callback(msg)
          
        #~ if no is None:
            #~ no = self.abandon_response
            
        #~ return Callback(msg,yes=yes,no)
        #~ return Callback(yes,no)
        #~ cb = Callback(yes,no)
        #~ h  = hash(cb)
        #~ self.pending_threads[h] = cb
        
        #~ r = dict(
          #~ success=True,
          #~ message=msg,
          #~ thread_id=h)
        #~ return r 
        
    def callback_get(self,request,thread_id,button_id):
        thread_id = int(thread_id)
        cb = self.pending_threads.pop(thread_id,None)
        #~ d = self.pop_thread(int(thread_id))
        if cb is None: 
            return self.action_response(self.error("Unknown callback %r" % thread_id))
        #~ buttonId = request.GET[ext_requests.URL_PARAM_'bi']
        #~ print buttonId
        for c in cb.choices:
            if c.name == button_id:
                #~ rv = c.func(request)
                rv = c.func()
                return self.action_response(rv)
                
        return self.action_response(self.error(
            "Invalid button %r for callback" % (button_id,thread_id)))
                
        #~ m = getattr(d,button_id)
        #~ rv = m(request)
        #~ if button_id == 'yes':
            #~ rv = d.yes()
        #~ elif button_id == 'no':
            #~ rv = d.no()
        #~ return self.action_response(rv)
  
        

        
    def check_action_response(self,rv):
        """
        Raise an exception if the action responded using an unknown keyword.
        """
        
        if rv is None:
            rv = self.success()
        elif isinstance(rv,Callback):
            h = hash(rv)
            self.pending_threads[h] = rv
            #~ def cb2dict(c):
                #~ return dict(name=c.name,label=c.label)
            #~ choices=[cb2dict(c) for c in rv.choices]
            buttons = dict()
            for c in rv.choices:
                buttons[c.name] = c.label
            rv = dict(
              success=True,
              message=rv.message,
              xcallback=dict(id=h,
                  title=rv.title,
                  buttons=buttons))
              #~ callback_id=h)
              #~ thread_id=h)
            #~ return r 
          
        for k in rv.keys():
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown key %r in action response." % k)
        return rv
                
    def action_response(self,kw):
        """
        """
        raise NotImplementedError
        

