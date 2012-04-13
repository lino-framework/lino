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
from lino.utils import babel

from lino.ui import requests as ext_requests

from lino.tools import resolve_model




class VirtualRow(object):
    def __init__(self,**kw):
        self.update(**kw)
        
    def update(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)
            
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

#~ class SimpleException(Exception): 
class Warning(Exception): 
    """
    An Exception whose string is meant to be 
    understandable by the user.
    """


class Action(object): 
    """
    Abstract base class for all Actions
    """
    sort_index = 99
    opens_a_slave = False
    label = None
    name = None
    key = None
    callable_from = None
    default_format = 'html'
    readonly = True
    hide_top_toolbar = False
    hide_navigator = False
    actor = None
    opens_a_window = False
    #~ can_view = perms.always
    
    
    def __init__(self,actor=None,name=None,label=None,**kw):
        #~ self.actor = actor # actor who offers this action
        if actor is not None:
            self.actor = actor # actor who offers this action
            #~ self.can_view = report.can_view
            if actor.hide_top_toolbar:
                self.hide_top_toolbar = True
        
        if name is None:
            if self.name is None:
                self.name = self.__class__.__name__ 
        else:
            self.name = name 
        if not isinstance(self.name,basestring):
            raise Exception("%s name %r is not a string" % (self.__class__,self.name))
        if label is None:
            label = self.label or self.name 
        self.label = label
        assert self.callable_from is None or isinstance(self.callable_from,(tuple,type)), "%s" % self
        for k,v in kw.items():
            if not hasattr(self,k):
                raise Exception("Invalid keyword %s" % k)
            setattr(self,k,v)
        
    def __str__(self):
        if self.actor is None:
            raise Exception("tried to call str() on general action %s" % self.name)
        return str(self.actor) + '.' + self.name
        
    def __unicode__(self):
        return force_unicode(self.label)
        
    def get_button_label(self):
        if self.actor is None:
            return self.label 
        if self is self.actor.default_action:
            return self.label 
        else:
            return u"%s %s" % (self.label,self.actor.label)
            
        
    def run(self,ar,**kw):
        """
        Execute the action. `ar` is an :class:`ActionRequest` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run() method" % self.__class__)


class TableAction(Action):
  
    def get_action_title(self,rr):
        return rr.get_title()
        

class RowAction(Action):
    """
    Base class for actions that are executed server-side on an individual row.
    """
    
    def run(self,rr,elem,**kw):
        raise NotImplementedError("%s has no run() method" % self.__class__)




#~ class OpenWindowAction(Action):
    #~ pass
    #~ action_type = 'open_window'
    
    
class RedirectAction(Action):
    #~ mimetype = None
    def get_target_url(self,elem):
        raise NotImplementedError
        



class GridEdit(TableAction):
  
    opens_a_window = True

    callable_from = tuple()
    name = 'grid'
    
    def __init__(self,rpt):
        self.label = rpt.button_label or rpt.label
        TableAction.__init__(self,rpt)


class ShowDetailAction(RowAction):
    opens_a_window = True
  
    #~ sort_index = 1
    callable_from = (GridEdit,)
    #~ show_in_detail = False
    #~ needs_selection = True
    name = 'detail'
    label = _("Detail")
    
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
        

RowAction.callable_from = (GridEdit,ShowDetailAction)


class InsertRow(TableAction):
    opens_a_window = True
    sort_index = 2
    hide_top_toolbar = True
    readonly = False
    callable_from = (GridEdit,ShowDetailAction)
    name = 'insert'
    #~ label = _("Insert")
    label = _("New")
    key = INSERT # (ctrl=True)
    #~ needs_selection = False
    hide_navigator = True
    
    def get_action_title(self,rr):
        return _("Insert into %s") % force_unicode(rr.get_title())

class DuplicateRow(RowAction):
    opens_a_window = True
  
    readonly = False
    callable_from = (GridEdit,ShowDetailAction)
    name = 'duplicate'
    label = _("Duplicate")


#~ class ShowEmptyTable(InsertRow):
class ShowEmptyTable(ShowDetailAction):
    callable_from = tuple()
    name = 'show' 
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    def __init__(self,actor,*args,**kw):
        #~ self.actor = actor # actor who offers this action
        self.label = actor.label
        #~ self.can_view = perms.always # actor.can_view
        super(ShowEmptyTable,self).__init__(actor,*args,**kw)
        
    def get_action_title(self,rr):
        return rr.get_title()
    #~ def __str__(self):
        #~ return str(self.actor)+'.'+self.name
        
class Calendar(Action):
    opens_a_window = True
    label = _("Calendar")
    name = 'grid' # because...
    default_format = 'html'
    
    def __init__(self,actor,*args,**kw):
        self.actor = actor # actor who offers this action
        #~ self.can_view = perms.always # actor.can_view
        super(Calendar,self).__init__(*args,**kw)
        
    def __str__(self):
        return str(self.actor) + '.' + self.name


    

class UpdateRowAction(RowAction):
    readonly = False
    

class ListAction(Action):
    """
    Base class for actions that are executed server-side on an individual row.
    """
    callable_from = (GridEdit,)
    

class DeleteSelected(Action):
    sort_index = 3
    readonly = False
    callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    name = 'delete'
    key = DELETE # (ctrl=True)
    #~ client_side = True
    
        
class SubmitDetail(Action):
    readonly = False
    #~ name = 'submit'
    label = _("Save")
    callable_from = (ShowDetailAction,)
    
class SubmitInsert(SubmitDetail):
    #~ name = 'submit'
    label = _("Save")
    #~ label = _("Insert")
    callable_from = (InsertRow,)


"""
"General actions" don't need to know their actor, so we can have 
the same instance for all actors.
"""
CREATE = SubmitInsert(sort_index=1)
UPDATE = SubmitDetail(sort_index=1)
DELETE = DeleteSelected(sort_index=5)





#~ class ActionRequest(object):
    #~ def __init__(self,ui,action):
        #~ self.ui = ui
        #~ self.action = action
        
    #~ def get_status(self,ui,**kw):
        #~ return kw

#~ class ActorRequest(ActionRequest):
class ActionRequest(object):
    """
    Deserves more documentation.
    """
    create_kw = None
    renderer = None
    
    def __init__(self,ui,report,request,action,renderer=None,**kw):
        #~ ActionRequest.__init__(self,ui,action)
        self.ui = ui
        self.renderer = renderer
        self.action = action
        self.step = 0 # confirmation counter
        self.report = report
        self.ah = report.get_handle(ui)
        self.request = request
        if request is not None:
            if request.method == 'PUT':
                rqdata = http.QueryDict(request.raw_post_data)
            else:
                rqdata = request.REQUEST
            kw = self.parse_req(request,rqdata,**kw)
        self.setup(**kw)
        
    #~ def confirm(self,step,*messages):
        #~ if self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,None) == str(step):
            #~ return
        #~ raise ConfirmationRequired(step,messages)

    def parse_req(self,request,rqdata,**kw):
        if self.report.parameters:
            kw.update(param_values=self.ui.parse_params(self.ah,request))
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
        #~ self.param_values = param_values
        if self.report.parameters:
            self.param_values = AttrDict()
            for k,pf in self.report.parameters.items():
                v = param_values.get(k,None)
                if v is None:
                    v = pf.get_default()
                self.param_values.define(k,v)
                
        
        if param_values:
            #~ logger.info("20120122 param_values is %s",param_values)
            for k,v in param_values.items():
                self.param_values.define(k,v)
        self.subst_user = subst_user
        #~ 20120111 
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        for k,v in self.report.known_values.items():
            kw.setdefault(k,v)
        if known_values:
            kw.update(known_values)
        #~ if self.report.__class__.__name__ == 'SoftSkillsByPerson':
            #~ logger.info("20111223 %r %r", kw, self.report.known_values)
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
        obj = PhantomRow(self,**kw)
        return obj
      
    def create_instance(self,**kw):
        if self.create_kw:
            kw.update(self.create_kw)
        #logger.debug('%s.create_instance(%r)',self,kw)
        if self.known_values:
            kw.update(self.known_values)
        obj = self.report.create_instance(self,**kw)
        #~ if self.known_values is not None:
            #~ self.ah.store.form2obj(self.known_values,obj,True)
            #~ for k,v in self.known_values:
                #~ field = self.model._meta.get_field(k) ...hier
                #~ kw[k] = v
        return obj
        
    def get_data_iterator(self):
        raise NotImplementedError
        
    def get_base_filename(self):
        return str(self.report)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')
        
    #~ def __iter__(self):
        #~ return self._sliced_data_iterator.__iter__()
        
    #~ def __getitem__(self,*args):
        #~ return self._data_iterator.__getitem__(*args)
        
    #~ def __len__(self):
        #~ return self._data_iterator.__len__()
        
    def get_user(self):
        return self.subst_user or self.user
        
    def get_action_title(self):
        return self.action.get_action_title(self)
        
    def get_title(self):
        return self.report.get_title(self)
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    #~ def row2dict(self,row,d):
        #~ # overridden in extjs.ext_requests.ViewReportRequest
        #~ return self.report.row2dict(row,d)

    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)

    def get_status(self,ui,**kw):
        if self.report.parameters:
            #~ pv = kw.setdefault('param_values',{})
            #~ kw.update(param_values=self.ah.store.pv2list(self.param_values))
            kw.update(param_values=self.ah.store.pv2dict(ui,self.param_values))
            #~ kw[ext_requests.URL_PARAM_PARAM_VALUES] = self.ah.store.pv2list(self.param_values)
        return kw
        

    def spawn_request(self,rpt,**kw):
        #~ rh = rpt.get_handle(self.ui)
        kw.update(user=self.user)
        kw.update(renderer=self.renderer)
        #~ kw.update(request=self.request)
        #~ return ViewReportRequest(None,rh,rpt.default_action,**kw)
        return self.__class__(self.ui,rpt,self.request,rpt.default_action,**kw)
        
