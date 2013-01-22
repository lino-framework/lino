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

import logging
logger = logging.getLogger(__name__)

import traceback
#~ from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django import http
from django.db import models
#~ from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage


import lino
from lino.utils import AttrDict
from lino.utils import curry
from lino.utils import babel
#~ from lino.utils import jsgen
#~ from lino.utils import Warning
from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.ui import requests as ext_requests

from lino.core.modeltools import resolve_model, resolve_app
from lino.core import layouts
#~ from lino.core import changes
from lino.core import fields

#~ from lino.core.perms import UserLevels
#~ from lino.core import perms 



class VirtualRow(object):
    def __init__(self,**kw):
        self.update(**kw)
        
    def update(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)

    def get_row_permission(self,ar,state,ba):
        if ba.action.readonly:
            return True
        return False 
            

class PhantomRow(VirtualRow):
    def __init__(self,request,**kw):
        self._ar = request
        VirtualRow.__init__(self,**kw)
        
    def __unicode__(self):
        return unicode(self._ar.get_action_title())
        
class EmptyTableRow(VirtualRow):
    """
    Base class for virtual rows of an :class:`EmptyTable`.
    """
    def __init__(self,table,**kw):
        self._table = table
        VirtualRow.__init__(self,**kw)
        
    def __unicode__(self):
        return unicode(self._table.label)
        
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_templates_group(self):
        return self._table.app_label + '/' + self._table.__name__
    
    def filename_root(self):
        return self._table.app_label + '.' + self._table.__name__







class BaseRequest(object):
    def __init__(self,ui,request=None,renderer=None,**kw):
        if ui is None:
            ui = settings.LINO.ui
            #~ from lino.ui.extjs3 import ui
        self.ui = ui
        #~ self.error_response = ui.error_response
        #~ self.success_response = ui.success_response
        
        #~ self.prompt = ui.callback
        self.callback = ui.callback
        self.confirm = ui.confirm
        self.error = ui.error
        self.success = ui.success
        if renderer is None:
            renderer = ui.text_renderer
        self.renderer = renderer
        #~ self.step = 0 # confirmation counter
        #~ self.report = actor
        self.request = request
        if request is not None:
            if request.method == 'PUT':
                rqdata = http.QueryDict(request.body) # raw_post_data before Django 1.4
            else:
                rqdata = request.REQUEST
            kw = self.parse_req(request,rqdata,**kw)
        #~ 20120605 self.ah = actor.get_handle(ui)
        self.setup(**kw)
        
  
    def parse_req(self,request,rqdata,**kw): 
        #~ if self.actor.parameters:
            #~ kw.update(param_values=self.ui.parse_params(self.ah,request))
        kw.update(user=request.user)
        kw.update(subst_user=request.subst_user)
        kw.update(requesting_panel=request.requesting_panel)
        #~ if settings.LINO.user_model:
            #~ username = rqdata.get(ext_requests.URL_PARAM_SUBST_USER,None)
            #~ if username:
                #~ try:
                    #~ kw.update(subst_user=settings.LINO.user_model.objects.get(username=username))
                #~ except settings.LINO.user_model.DoesNotExist, e:
                    #~ pass
        #~ logger.info("20120723 ActionRequest.parse_req() --> %s",kw)
        return kw
        
    def setup(self,
            user=None,
            subst_user=None,
            requesting_panel=None,
            renderer=None):
        self.requesting_panel = requesting_panel
        self.user = user 
        if renderer is not None:
            self.renderer = renderer
        #~ if self.actor.parameters:
            #~ self.param_values = AttrDict(**param_values)
        self.subst_user = subst_user
        
        
    #~ def dialog(self,dlg):
        #~ # not finished
        #~ self.step += 1
        #~ if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            #~ return
        #~ raise DialogRequired(self.step,dlg)
        
    #~ def confirm(self,*messages):
        #~ """
        #~ Calling this from an Action's :meth:`Action.run` method will
        #~ interrupt the execution, send the specified message(s) back to 
        #~ the user, waiting for confirmation before continuing.
        
        #~ Note that this is implemented without any server sessions 
        #~ and cookies. While this system is genial, it has one drawback 
        #~ which you should be aware of: the code execution does not 
        #~ *continue* after the call to `confirm` but starts again at the 
        #~ beginning (with the difference that the client this time calls it with 
        #~ an internal `step` parameter that tells Lino that this `confirm()` 
        #~ has been answered and should no longer raise stop execution.
        #~ """
        #~ assert len(messages) > 0 and messages[0], "At least one non-empty message required"
        #~ self.step += 1
        #~ if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            #~ return
        #~ raise ConfirmationRequired(self.step,messages)
        
    #~ def decide(self,msg,yes,no=None):
        #~ """
        #~ Calling this from an Action's :meth:`Action.run` method will
        #~ interrupt the execution, send the specified message(s) back to 
        #~ the user, adding the executables `yes` and optionally `no` to a queue 
        #~ of pending dialogs.
        
        #~ """
        #~ raise DecisionRequired(msg,yes,no)
            
    def get_user(self):
        """
        Return the :class:`User <lino.modlib.users.models.User>` 
        instance of the user who issued the request.
        If the authenticated user is acting as somebody else, 
        return that :class:`User <lino.modlib.users.models.User>` instance.
        """
        return self.subst_user or self.user
        
        
    def add_system_note(self,owner,subject,body,silent):
        """
        System notes are a part of Lino's workflow management system. 
        A system note is a text message attached to a given 
        database object instance and propagated through a series of 
        configurable channels.
        The text part consists basically of a subject 
        and a body, both usually generated by the application and edited 
        by the user in an action's parameters dialog box. 
        Executing the action will then also trigger the sending of the system note.
        
        """
        #~ logger.info("20121016 add_system_note() '%s'",subject)
        notes = resolve_app('notes')
        if notes:
            notes.add_system_note(self,owner,subject,body)
        #~ if silent:
            #~ return
        recipients = []
        for addr in settings.LINO.get_system_note_recipients(self,owner,silent):
            if not '@example.com' in addr:
                recipients.append(addr)
        if not len(recipients):
            return
        sender = self.get_user().email or settings.SERVER_EMAIL
        if not sender or '@example.com' in sender:
            return
        msg = EmailMessage(subject=subject, 
            from_email=sender,body=body,to=recipients)
        msg.send()
        logger.info("System note '%s' from %s has been sent to %s",subject,sender,recipients)

      
class ActionRequest(BaseRequest):
    """
    Holds information about an indivitual web request and provides methods like

    - :meth:`get_user <lino.core.actions.ActionRequest.get_user>`
    - :meth:`callback <lino.ui.base.UI.callback>`
    - :meth:`confirm <lino.ui.base.UI.confirm>`
    - :meth:`success <lino.ui.base.UI.success>`
    - :meth:`error <lino.ui.base.UI.error>`
    - :meth:`spawn <lino.core.actions.ActionRequest.spawn>`

    
    """
    create_kw = None
    renderer = None
    
    offset = None
    limit = None
    order_by = None
    
    def __init__(self,ui,actor,request=None,action=None,renderer=None,param_values=None,**kw):
        """
        An ActionRequest is instantiated from different shortcut methods:
        
        - :meth:`lino.core.actors.Actor.request`
        - :meth:`lino.core.actions.Action.request`
        
        """
        #~ ActionRequest.__init__(self,ui,action)
        self.actor = actor
        #~ self.action = action or actor.default_action
        #~ self.bound_action = BoundAction(actor,action or actor.default_action)
        #~ if action and not isinstance(action,BoundAction):
            #~ raise Exception("20121003 %r is not a BoundAction" % action)
        self.bound_action = action or actor.default_action
        BaseRequest.__init__(self,ui,request,renderer,**kw)
        self.ah = actor.get_request_handle(self)
        """
        See 20120825
        """
        #~ if self.actor.parameters is None:
            #~ if param_values is not None:
                #~ raise Exception("Cannot request param_values on %s" % self.actor)
        #~ else:
        if self.actor.parameters is not None:
            pv = self.actor.param_defaults(self)
            
            """
            New since 20120913.
            E.g. newcomers.Newcomers is a simple pcsw.Clients with known_values=dict(client_state=newcomer)
            and since there is a parameter `client_state`, we override that parameter's default value.
            """
            for k,v in self.known_values.items():
                if pv.has_key(k):
                    pv[k] = v
            """
            New since 20120914.
            MyClientsByGroup has a known group, this 
            must also appear as `group` parameter value.
            Lino now understands tables where the master_key is also a parameter.
            """
            if self.actor.master_key is not None:
                if pv.has_key(self.actor.master_key):
                    pv[self.actor.master_key] = self.master_instance
                
            if param_values is None:
              if request is not None: # 20121025
                #~ pv.update(self.ui.parse_params(self.ah,request))
                #~ pv.update(self.ah.store.parse_params(request))
                pv.update(self.actor.params_layout.params_store.parse_params(request))
                
            if param_values is not None:
                for k in param_values.keys(): 
                    if not pv.has_key(k):
                        raise Exception("Invalid key %r in param_values" % k)
                pv.update(param_values)
                
            self.param_values = AttrDict(**pv)
            
        #~ print 20130121, __file__, self.bound_action.action, self.bound_action.action.parameters
        
        if self.bound_action.action.parameters is not None:
            apv = self.bound_action.action.action_param_defaults(self,None)
            if request is not None:
                #~ pv.update(self.ui.parse_params(self.ah,request))
                #~ pv.update(self.ah.store.parse_params(request))
                apv.update(self.bound_action.action.params_layout.params_store.parse_params(request))
            #~ logger.info("20130122 action_param_defaults() returned %s",apv)
            self.action_param_values = AttrDict(**apv)
            
            #~ if param_values:
                #~ # logger.info("20120608 param_values is %s",param_values)
                #~ for k,v in param_values.items():
                    #~ self.param_values.define(k,v)
                    
        self.bound_action.setup_action_request(self)
                
        
    def setup(self,
            #~ param_values={},
            known_values=None,
            **kw):
        BaseRequest.setup(self,**kw)
        #~ 20120111 
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        kv = dict()
        for k,v in self.actor.known_values.items():
            kv.setdefault(k,v)
        if known_values:
            kv.update(known_values)
        self.known_values = kv
        
    def create_phantom_rows(self,**kw):
        #~ logger.info('20121011 %s.create_phantom_rows(), %r', self,self.create_kw)
        if self.create_kw is None or not self.actor.editable or not self.actor.allow_create:
            #~ logger.info('20120519 %s.create_phantom_row(), %r', self,self.create_kw)
            return 
        if not self.actor.get_create_permission(self):
            return
        #~ # if not self.actor.get_permission(self.get_user(),self.actor.create_action):
        #~ # if not self.actor.allow_create(self.get_user(),None,None):
        #~ # ca = self.actor.get_url_action('create_action')
        #~ ca = self.actor.create_action
        #~ if ca is not None:
            #~ # if not self.actor.create_action.allow(self.get_user(),None,None):
            #~ # if not ca.allow(self.get_user(),None,None):
            #~ if not ca.get_bound_action_permission(self.get_user(),None,None):
                #~ return
        yield PhantomRow(self,**kw)
      
    def create_instance(self,**kw):
        if self.create_kw:
            kw.update(self.create_kw)
        #logger.debug('%s.create_instance(%r)',self,kw)
        if self.known_values:
            kw.update(self.known_values)
        #~ print "20120527 create_instance", self, kw
        obj = self.actor.create_instance(self,**kw)
        #~ print 20120630, self.actor, 'actions.TableRequest.create_instance'
        #~ if self.known_values is not None:
            #~ self.ah.store.form2obj(self.known_values,obj,True)
            #~ for k,v in self.known_values:
                #~ field = self.model._meta.get_field(k) ...hier
                #~ kw[k] = v
        return obj
        
        
    def get_data_iterator(self):
        raise NotImplementedError
        
    def get_base_filename(self):
        return str(self.actor)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')
        
    def get_action_title(self):
        return self.bound_action.action.get_action_title(self)
        
    def get_title(self):
        return self.actor.get_title(self)
        
    def render_to_dict(self):
        return self.bound_action.action.render_to_dict(self)
        
    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)

    def get_action_status(self,ba,obj,**kw):
        #~ logger.info("get_action_status %s",ba.full_name())
        if ba.action.parameters:
            if ba.action.params_layout.params_store is None:
                raise Exception("20121016 %s has no store" % ba.action.params_layout)
            kw.update(field_values=ba.action.params_layout.params_store.pv2dict(
                self.ui,ba.action.action_param_defaults(self,obj)))
        return kw
      
      
    def get_status(self,ui,**kw):
        if self.actor.parameters:
            #~ kw.update(param_values=self.ah.store.pv2dict(ui,self.param_values))
            #~ lh = self.actor.params_layout.get_layout_handle(ui)
            kw.update(param_values=self.actor.params_layout.params_store.pv2dict(ui,self.param_values))
        bp = kw.setdefault('base_params',{})
        if self.subst_user is not None:
            #~ bp[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.username
            bp[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.id
        #~ if self.actor.__name__ == 'MyClients':
            #~ print "20120918 actions.get_status", kw
        return kw
        

    def spawn(self,actor=None,**kw):
        """
        Create a new ActionRequest, taking default values from this one.
        """
        kw.setdefault('user',self.user)
        kw.setdefault('subst_user',self.subst_user)
        kw.setdefault('requesting_panel',self.requesting_panel)
        kw.setdefault('renderer',self.renderer)
        #~ kw.setdefault('request',self.request) 
        # removed 20120702 because i don't want to inherit quick_search from spawning request
        # and because i couldn't remember why 'request' was passed to the spawned request.
        if actor is None:
            actor = self.actor
        return self.ui.request(actor,**kw)
        
    #~ def decide_response(self,*args,**kw): return self.ui.decide_response(self,*args,**kw)
    #~ def prompt(self,*args,**kw): return self.ui.prompt(self,*args,**kw)
    def summary_row(self,*args,**kw): return self.actor.summary_row(self,*args,**kw)
    def instance_handler(self,*args,**kw): return self.renderer.instance_handler(self,*args,**kw)
    def href_to(self,*args,**kw): return self.renderer.href_to(self,*args,**kw)
    def pk2url(self,*args,**kw): return self.renderer.pk2url(self,*args,**kw)
    def get_request_url(self,*args,**kw): return self.renderer.get_request_url(self,*args,**kw)
    def obj2html(self,*args,**kw): return self.renderer.obj2html(self,*args,**kw)
    def href_to_request(self,*args,**kw): return self.renderer.href_to_request(self,*args,**kw)
    def row_action_button(self,obj,a,*args,**kw): return self.renderer.row_action_button(obj,self.request,a,*args,**kw)
    def as_html(self,*args,**kw): return self.bound_action.action.as_html(self,*args,**kw)
        
    def absolute_uri(self,*args,**kw):
        ar = self.spawn(*args,**kw)
        location = ar.renderer.get_request_url(ar)
        return self.request.build_absolute_uri(location)
        
            
    def to_rst(self,column_names=None):
        """
        Returns a string representing this request in reStructuredText markup.
        """
        raise NotImplementedError()
            
            
        
