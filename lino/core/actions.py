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

import logging
logger = logging.getLogger(__name__)

import traceback
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django import http


import lino
from lino.utils import AttrDict
from lino.utils import curry
from lino.utils import babel
from lino.utils import Warning

from lino.ui import requests as ext_requests

from lino.core.modeltools import resolve_model

#~ from lino.core.perms import UserLevels
#~ from lino.core import perms 


class VirtualRow(object):
    def __init__(self,**kw):
        self.update(**kw)
        
    def update(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)

    def get_row_permission(self,user,state,action):
        if action.readonly:
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









class Hotkey:
    keycode = None
    shift = False
    ctrl = False
    alt = False
    inheritable = ('keycode','shift','ctrl','alt')
    def __init__(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)
            
    def __call__(self,**kw):
        for n in self.inheritable:
            if not kw.has_key(n):
                kw[n] = getattr(self,n)
            return Hotkey(**kw)
      
# ExtJS src/core/EventManager-more.js
RETURN = Hotkey(keycode=13)
ESCAPE = Hotkey(keycode=27)
PAGE_UP  = Hotkey(keycode=33)
PAGE_DOWN = Hotkey(keycode=34)
INSERT = Hotkey(keycode=44)
DELETE = Hotkey(keycode=46)
    
    
class ConfirmationRequired(Exception):
    """
    This is the special exception risen when an Action calls 
    :meth:`ActionRequest.confirm`.
    """
    def __init__(self,step,messages):
        self.step = step
        self.messages = messages
        Exception.__init__(self)


class Action(object):
    """
    Abstract base class for all Actions
    """
    
    sort_index = 90
    """
    Predefined sort_index values are:
    
    value action
    ----- -----------
    20    :class:`Insert <InsertRow>`
    30    :class:`Delete <DeleteSelected>`
    50    :class:`Print <lino.mixins.printable.BasePrintAction>`
    60    :attr:`Duplicate <lino.mixins.duplicable.Duplicable.duplicate_row>`
    90    default for all custom row actions created using `@dd.action`
    
    """
    opens_a_slave = False
    label = None
    
    #~ ruled = False 
    #~ """
    #~ Whether this action is ruled by workflows.
    #~ """
    actor = None
    help_text = None
    #~ debug = False
    name = None
    url_action_name = None
    #~ inheritable = True
    key = None
    callable_from = None
    default_format = 'html'
    readonly = True
    hide_top_toolbar = False
    hide_navigator = False
    opens_a_window = False
    show_in_bbar = True
    """
    Whether this action should be displayed as a button in the bottom toolbar and the context menu.
    """
    
    show_in_workflow = False
    """
    Whether this action should be displayed 
    among the :meth:`workflow_buttons <lino.core.actors.Actor.workflow_buttons>`.
    """
    
    auto_save = True
    """
    What to do when this action is being called while the user is on a dirty record.
    - `False` means: forget any changes in current record and run the action.
    - `True` means: save any changes in current record before running the action.
    - `None` means: ask the user.
    """
    #~ can_view = perms.always
    
    #~ required_user_groups = None
    #~ required_user_level = None
    #~ required_states = None
    required = {}
    """
    A dict with conditions to specify permissions.
    #~ If this is set, the action is available only on rows 
    #~ that meet the specified conditions.
    
    """
    
    #~ owned_only = False
    #~ """
    #~ If this is `True` 
    #~ (and if :attr:`lino.core.actors.Actor.workflow_owner_field` is set),
    #~ the action will be available only on rows owned by the requesting user.
    #~ """
    
    
    
    
    #~ def __init__(self,actor=None,name=None,label=None,**kw):
    #~ def __init__(self,name=None,label=None,url_action_name=None,**kw):
    #~ def __init__(self,label=None,**kw):
    def __init__(self,label=None,url_action_name=None,required={},**kw):
        #~ self.actor = actor # actor who offers this action
        #~ if actor is not None:
            #~ self.actor = actor # actor who offers this action
            #~ if actor.hide_top_toolbar:
                #~ self.hide_top_toolbar = True
        
        if url_action_name is not None:
            if not isinstance(url_action_name,basestring):
                raise Exception("%s name %r is not a string" % (self.__class__,url_action_name))
            self.url_action_name = url_action_name
        #~ if name is None:
            #~ if self.name is None:
                #~ self.name = self.__class__.__name__ 
        #~ else:
            #~ self.name = name 
        #~ if not isinstance(self.name,basestring):
            #~ raise Exception("%s name %r is not a string" % (self.__class__,self.name))
        if label is None:
            label = self.label or self.url_action_name 
        self.label = label
        assert self.callable_from is None or isinstance(
            self.callable_from,(tuple,type)), "%s" % self
        for k,v in kw.items():
            if not hasattr(self,k):
                raise Exception("Invalid keyword %s" % k)
            setattr(self,k,v)
        self.set_required(**required)

        
    def set_required(self,**kw):
        #~ logger.info("20120628 set_required %s(%s)",self,kw)
        new = dict()
        new.update(self.required)
        new.update(kw)
        self.required = new
        #~ if isinstance(self,StateAction):
        if self.required.has_key('states'):
            self.show_in_bbar = False
            self.show_in_workflow = True
        else:
            self.show_in_workflow = False
            self.show_in_bbar = True
        
    def __str__(self):
        #~ raise Exception("Must use action2str(actor,action)")
        if self.actor is None:
            #~ raise Exception("tried to call str() on general action %s" % self.name)
            return repr(self)
            #~ raise Exception("Tried to call str() on shared action %r" % self)
        if self.name is None:
            return repr(self)
        return str(self.actor) + '.' + self.name
        
    #~ def set_permissions(self,*args,**kw)
        #~ self.permission = perms.factory(*args,**kw)
        
    def attach_to_actor(self,actor,name):
        if self.name is not None:
            raise Exception("%s tried to attach named action %s" % (actor,self))
        if self.actor is not None:
            raise Exception("%s tried to attach action %s of %s" % (actor,name,self.actor))
        self.name = name
        self.actor = actor
        if actor.hide_top_toolbar:
            self.hide_top_toolbar = True
        if self.help_text is None and self is actor.default_action:
            self.help_text  = actor.help_text
        #~ if name == 'default_action':
            #~ print 20120527, self
            
    #~ def contribute_to_class(self,model,name):
        #~ ma = model.__dict__.get('_lino_model_actions',None)
        #~ if ma is None:
            #~ ma = dict()
            #~ model._lino_model_actions = ma
            #~ # model.__dict__.set('_lino_model_actions',ma)
        #~ ma[name] = self
        #~ self.name = name
        #~ # model.__dict__['_lino_model_actions'] = d
        
    def __unicode__(self):
        return force_unicode(self.label)
        
    #~ def get_view_permission(self,user):
        #~ """
        #~ E.g. DispatchAction is not available for a User with empty partner
        #~ """
        #~ return True
        
    def get_button_label(self):
        if self.actor is None:
            return self.label 
        if self is self.actor.default_action:
            return self.label 
        else:
            return u"%s %s" % (self.label,self.actor.label)
            
    def get_action_permission(self,user,obj,state):
        """
        The default implementation simply calls this action's 
        permission handler.
        Derived Action classes may override this to add vetos.
        E.g. DispatchAction is not available for a User with empty partner.
        """
        #~ logger.info("20120622 Action.get_action_permission")
        return self.allow(user,obj,state)
        
    #~ def run(self,elem,ar,**kw):
        #~ raise NotImplementedError("%s has no run() method" % self.__class__)


class TableAction(Action):
    """
    TODO: get_action_permission and required_states 
    are needed here because `disabled_actions` also asks InsertRow whether 
    it's permitted on that row. It's in fact not correct to ask this for 
    the Insert button. Has to do with the fact that the Insert button is 
    in the bottom toolbar though it should be in the top toolbar...
    """
  
    #~ required_states = None
    
    def get_action_title(self,rr):
        return rr.get_title()
        

class RowAction(Action):
    """
    Base class for actions that are executed on an individual row.
    """
    
    def run(self,row,ar,**kw):
        """
        Execute the action on the given `row`. `ar` is an :class:`ActionRequest` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run() method" % self.__class__)

    #~ def get_action_permission(self,user,obj):
        #~ return self.actor.get_row_permission(self,user,obj)
            
    def attach_to_actor(self,actor,name):
        super(RowAction,self).attach_to_actor(actor,name)
        if not self.url_action_name:
            self.url_action_name = name 


class StateAction(RowAction):
    
    def __init__(self,actor,target_state,**kw):
        self.target_state = target_state
        kw.update(label=target_state.text)
        required = getattr(target_state,'required',None)
        if required is not None:
            if target_state.name:
                m = getattr(actor.model,'allow_state_'+target_state.name,None)
                if m is not None:
                    def allow(action,user,obj,state):
                        return m(obj,user)
                    required.update(allow=allow)
            kw.update(required=required)
        help_text = getattr(target_state,'help_text',None)
        if help_text:
            kw.update(help_text=help_text)
        super(StateAction,self).__init__(**kw)
        #~ print 20120709, self, self.show_in_workflow
        
    #~ def get_action_permission(self,user,obj,state):
        #~ if state and not state.get_state_permission(self,user,obj):
            #~ return False
        #~ return self.allow(user,obj,state)
        
    def run(self,row,ar,**kw):
        row.before_state_change(ar,row.state,self.target_state)
        row.state = self.target_state
        row.save()
        return ar.ui.success_response(refresh=True)
        
    

class RedirectAction(Action):
    
    def get_target_url(self,elem):
        raise NotImplementedError
        



class GridEdit(TableAction):
  
    show_in_workflow = False
    opens_a_window = True

    callable_from = tuple()
    url_action_name = 'grid'
    
    #~ def __init__(self,*args,**kw):
        #~ TableAction.__init__(self,*args,**kw)
        
    def attach_to_actor(self,actor,name):
        #~ self.label = actor.button_label or actor.label
        self.label = actor.label
        super(GridEdit,self).attach_to_actor(actor,name)

    def get_window_layout(self):
        #~ return self.actor.list_layout
        return None


class ShowDetailAction(RowAction):
    """
    An action that opens the Detail Window of its actor.
    """
    opens_a_window = True
    show_in_workflow = False
    
    #~ sort_index = 1
    callable_from = (GridEdit,)
    #~ show_in_detail = False
    #~ needs_selection = True
    url_action_name = 'detail'
    label = _("Detail")
    
    def get_window_layout(self):
        return self.actor.detail_layout
        
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
        

RowAction.callable_from = (GridEdit,ShowDetailAction)

class InsertRow(TableAction):
    """
    Opens the Insert window filled with a blank row. 
    The new row will be actually created only when this 
    window gets submitted.
    """
    show_in_workflow = False
    opens_a_window = True
    sort_index = 20
    hide_top_toolbar = True
    readonly = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    url_action_name = 'insert'
    #~ label = _("Insert")
    label = _("New")
    key = INSERT # (ctrl=True)
    #~ needs_selection = False
    hide_navigator = True
    
    def get_action_title(self,rr):
        return _("Insert into %s") % force_unicode(rr.get_title())
        
    def get_window_layout(self):
        return self.actor.insert_layout or self.actor.detail_layout





class DuplicateRow(RowAction):
    opens_a_window = True
  
    readonly = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    url_action_name = 'duplicate'
    label = _("Duplicate")


#~ class ShowEmptyTable(InsertRow):
class ShowEmptyTable(ShowDetailAction):
    callable_from = tuple()
    url_action_name = 'show' 
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    
    def attach_to_actor(self,actor,name):
        self.label = actor.label
        ShowDetailAction.attach_to_actor(self,actor,name)
        #~ print 20120523, actor, name, 'setup', unicode(self.label)
        
    def get_action_title(self,rr):
        return rr.get_title()
    #~ def __str__(self):
        #~ return str(self.actor)+'.'+self.name
        
class Calendar(Action):
    opens_a_window = True
    label = _("Calendar")
    url_action_name = 'grid' # because...
    default_format = 'html'
    
    def get_window_layout(self):
        return None
        
    #~ def __init__(self,*args,**kw):
        #~ self.actor = actor # actor who offers this action
        #~ super(Calendar,self).__init__(*args,**kw)
        
    #~ def __str__(self):
        #~ return str(self.actor) + '.' + self.name


    

class UpdateRowAction(RowAction):
    show_in_workflow = False
    readonly = False
    required = dict(user_level='user')
    

class ListAction(Action):
    """
    Base class for actions that are executed server-side on an individual row.
    """
    callable_from = (GridEdit,)
    

class DeleteSelected(RowAction):
    """
    Delete the row.
    """
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    url_action_name = 'delete'
    key = DELETE # (ctrl=True)
    #~ client_side = True
    
        
class SubmitDetail(RowAction):
    auto_save = False
    show_in_workflow = False
    readonly = False
    required = dict(user_level='user')
    #~ url_action_name = 'SubmitDetail'
    label = _("Save")
    callable_from = (ShowDetailAction,)
    
class SubmitInsert(SubmitDetail):
    #~ url_action_name = 'SubmitInsert'
    label = _("Create")
    #~ label = _("Insert")
    callable_from = (InsertRow,)


"""
"General actions" don't need to know their actor, so we can have 
the same instance for all actors.
"""
#~ VIEW = ViewAction(sort_index=1)
#~ CREATE = SubmitInsert(sort_index=1)
#~ UPDATE = SubmitDetail(sort_index=1)
#~ DELETE = DeleteSelected(sort_index=5)





class ActionRequest(object):
    """
    Deserves more documentation.
    """
    create_kw = None
    renderer = None
    
    def __init__(self,ui,actor,request=None,action=None,renderer=None,**kw):
        #~ ActionRequest.__init__(self,ui,action)
        if ui is None:
            from lino.extjs import ui
        self.ui = ui
        self.error_response = ui.error_response
        self.success_response = ui.success_response
        self.renderer = renderer
        self.action = action or actor.default_action
        self.step = 0 # confirmation counter
        #~ self.report = actor
        self.actor = actor
        self.request = request
        if request is not None:
            if request.method == 'PUT':
                rqdata = http.QueryDict(request.raw_post_data)
            else:
                rqdata = request.REQUEST
            kw = self.parse_req(request,rqdata,**kw)
        #~ 20120605 self.ah = actor.get_handle(ui)
        self.setup(**kw)
        # 20120605 : Actor.get_request_handle() ar instead of ui
        self.ah = actor.get_request_handle(self)
        
        if self.actor.parameters and request is not None:
            param_values = self.ui.parse_params(self.ah,request)
                
            for k,pf in self.actor.parameters.items():
                v = param_values.get(k,None)
                if v is None:
                    v = pf.get_default()
                self.param_values.define(k,v)
            if param_values:
                #~ logger.info("20120608 param_values is %s",param_values)
                for k,v in param_values.items():
                    self.param_values.define(k,v)
                
        
    #~ def confirm(self,step,*messages):
        #~ if self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,None) == str(step):
            #~ return
        #~ raise ConfirmationRequired(step,messages)

    def parse_req(self,request,rqdata,**kw): 
        #~ if self.actor.parameters:
            #~ kw.update(param_values=self.ui.parse_params(self.ah,request))
        kw.update(user=request.user)
        
        #~ 20120111 kw.update(user=request.user)
        #~ user = request.user
        #~ if user is not None and user.is_superuser:
        #~ if True:
        if settings.LINO.user_model:
            username = rqdata.get(ext_requests.URL_PARAM_SUBST_USER,None)
            if username:
                try:
                    kw.update(subst_user=settings.LINO.user_model.objects.get(username=username))
                except settings.LINO.user_model.DoesNotExist, e:
                    pass
            #~ kw.update(user=user)
        return kw
      
    def setup(self,
            user=None,
            subst_user=None,
            param_values={},
            known_values=None,
            renderer=None,
            **kw):
        self.user = user
        if renderer is not None:
            self.renderer = renderer
        if self.actor.parameters:
            self.param_values = AttrDict(**param_values)
            #~ self.param_values = param_values
        self.subst_user = subst_user
        #~ 20120111 
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        for k,v in self.actor.known_values.items():
            kw.setdefault(k,v)
        if known_values:
            kw.update(known_values)
        self.known_values = kw
        
        
    def confirm(self,*messages):
        """
        Calling this from an Action's :meth:`Action.run`
        """
        assert len(messages) > 0 and messages[0], "At least one non-empty message required"
        self.step += 1
        if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            return
        raise ConfirmationRequired(self.step,messages)
        
    def create_phantom_row(self,**kw):
        if self.create_kw is None or not self.actor.editable:
            #~ logger.info('20120519 %s.create_phantom_row(), %r', self,self.create_kw)
            return 
        #~ if not self.actor.get_permission(self.get_user(),self.actor.create_action):
        #~ if not self.actor.allow_create(self.get_user(),None,None):
        if self.actor.create_action is not None:
            if not self.actor.create_action.allow(self.get_user(),None,None):
                return
        return PhantomRow(self,**kw)
      
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
        
    def get_user(self):
        return self.subst_user or self.user
        
    def get_action_title(self):
        return self.action.get_action_title(self)
        
    def get_title(self):
        return self.actor.get_title(self)
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    #~ def row2dict(self,row,d):
        #~ # overridden in extjs.ext_requests.ViewReportRequest
        #~ return self.report.row2dict(row,d)

    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)

    def get_status(self,ui,**kw):
        if self.actor.parameters:
            #~ pv = kw.setdefault('param_values',{})
            #~ kw.update(param_values=self.ah.store.pv2list(self.param_values))
            kw.update(param_values=self.ah.store.pv2dict(ui,self.param_values))
            #~ kw[ext_requests.URL_PARAM_PARAM_VALUES] = self.ah.store.pv2list(self.param_values)
        return kw
        

    def spawn(self,actor=None,**kw):
        """
        Create a new ActionRequest, taking default values from this one.
        """
        kw.setdefault('user',self.user)
        kw.setdefault('renderer',self.renderer)
        #~ kw.setdefault('request',self.request) 
        # removed 20120702 because i don't want to inherit quick_search from spawning request
        # and because i couldn't remember why 'request' was passed to the spawned request.
        if actor is None:
            actor = self.actor
        #~ kw.update(request=self.request)
        #~ return ViewReportRequest(None,rh,rpt.default_action,**kw)
        #~ return self.__class__(self.ui,actor,**kw)
        return self.ui.request(actor,**kw)
        

def action(*args,**kw):
    def decorator(fn):
        a = RowAction(*args,**kw)
        #~ a.run = curry(fn,a)
        a.run = fn
        return a
    return decorator
    
#~ def action2str(actor,action):
    #~ return str(actor) + '.' + action.name
