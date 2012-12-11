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
        
class DialogRequired(Exception):
    """
    This is the special exception risen when an Action calls 
    :meth:`ActionRequest.dialog`.
    """
    def __init__(self,step,dlg):
        self.step = step
        self.dialog = dlg
        Exception.__init__(self)
        


class Permittable(object):
    """
    Base class for objects that have view permissions control.
    
    :class:`lino.core.actors.Actor` would be a subclass, 
    but is a special case since actors never get instantiated.
    
    """
    
    #~ required = None # not {}, see blog/2012/0923
    #~ required = dict()
    required = {}
    """
    A dict with permission requirements.
    See :func:`lino.utils.jsgen.make_permission_handler`.
    """
    
    workflow_state_field = None # internally needed for make_permission_handler
    workflow_owner_field = None # internally needed for make_permission_handler
    #~ readonly = True
    
    debug_permissions = False
    
    def add_requirements(self,**kw):
        return add_requirements(self,**kw)
        
    def get_view_permission(self,profile):
        raise NotImplementedError()
        

def add_requirements(obj,**kw):
    """
    Add the specified requirements to `obj`.
    `obj` can be an 
    :class:`lino.core.actors.Actor` or any 
    :class:`lino.core.actions.Permittable`.
    Application code uses this indirectly through the shortcut methods
    :meth:`lino.core.actors.Actor.add_view_requirements` or a 
    :meth:`lino.core.actions.Permittable.add_requirements`.
    
    """
    #~ logger.info("20120927 perms.set_required %r",kw)
    new = dict()
    #~ new.update(getattr(obj,'required',{}))
    new.update(obj.required)
    new.update(kw)
    obj.required = new



def register_params(cls):
    if cls.parameters:
        for k,v in cls.parameters.items():
            v.set_attributes_from_name(k)
            v.table = cls
        if cls.params_layout is None:
            cls.params_layout = cls._layout_class.join_str.join(cls.parameters.keys())
        if isinstance(cls.params_layout,basestring):
            cls.params_layout = cls._layout_class(cls.params_layout,cls)
        elif isinstance(cls.params_layout,layouts.Panel):
            cls.params_layout = cls._layout_class(cls.params_layout.desc,cls,**cls.params_layout.options)

def setup_params_choosers(self):
    if self.parameters:
        from lino.utils.choosers import check_for_chooser
        for k,fld in self.parameters.items():
            if isinstance(fld,models.ForeignKey):
                fld.rel.to = resolve_model(fld.rel.to)
            check_for_chooser(self,fld)

def make_params_layout_handle(self,ui):
    return self.params_layout.get_layout_handle(ui)


class Parametrizable(object):        
    """
    Base class for both Actors and Actions.
    """
    active_fields = None # 20121006
    master_field = None
    
    parameters = None
    """
    User-definable parameter fields for this table.
    Set this to a `dict` of `name = models.XyzField()` pairs.
    """
    
    #~ params_template = None # no longer used
    
    params_layout = None
    """
    If this table has parameters, specify here how they should be 
    laid out in the parameters panel.
    """
    
    params_panel_hidden = False
    """
    If this table has parameters, set this to True if the parameters 
    panel should be initially hidden when this table is being displayed.
    """
    
    _layout_class = NotImplementedError
    
            
    #~ @classmethod
    #~ def install_params_on_actor(cls):
        #~ for k in ('get_window_layout', 'after_site_setup',
          #~ 'make_params_layout_handle','get_param_elem'):
            #~ um = getattr(cls,k)
            #~ setattr(cls,k,classmethod(um))
        
        
    @classmethod
    def get_param_elem(self,name):
        if self.parameters:
            return self.parameters.get(name,None)
        #~ for pf in self.params:
            #~ if pf.name == name:  return pf
        return None
      
    #~ @classmethod
    def get_window_layout(self,actor):
        return self.params_layout
        
        
#~ class ActionMetaClass(type):
    #~ def __new__(meta, classname, bases, classDict):
        #~ cls = type.__new__(meta, classname, bases, classDict)
        #~ cls.register_params()
        #~ return cls
      


class Action(Parametrizable,Permittable):
    """
    Abstract base class for all Actions
    """
    
    #~ __metaclass__ = ActionMetaClass
    
    debug_permissions = False
    
    icon_name = None 
    """
    The class name of an icon to be used for this action.
    """
    
    icon_file = None
    """
    The file name of an icon to be used for this action.
    """
    
    _layout_class = layouts.ActionParamsLayout
    
    sort_index = 90
    """
    
    Predefined sort_index values are:
    
    ===== =================================
    value action
    ===== =================================
    10    :class:`insert <InsertRow>`
    11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate_row>`
    20    :class:`detail <ShowDetailAction>`
    30    :class:`delete <DeleteSelected>`
    50    :class:`Print <lino.mixins.printable.BasePrintAction>`
    51    :class:`Clear Cache <lino.mixins.printable.ClearCacheAction>`
    90    default for all custom row actions created using :func:`@dd.action <action>`
    ===== =================================
    
    """
    
    label = None
    """
    The text to appear on the button.
    """
    
    help_text = None
    """
    A help text that shortly explains what this action does.
    ExtJS uses this as tooltip text.
    """
    
    auto_save = True
    """
    What to do when this action is being called while the user is on a dirty record.
    
    - `False` means: forget any changes in current record and run the action.
    - `True` means: save any changes in current record before running the action.
    - `None` means: ask the user.
    """
    
    #~ required = {}
    #~ """
    #~ A dict with permission requirements.
    #~ See :func:`lino.utils.jsgen.make_permission_handler`.
    #~ """
    
    action_name = None
    """
    Internally used to store the name of this action within the defining Actor's namespace.
    """
    
    #~ url_action_name = None
    #~ """
    #~ """
    
    use_param_panel = False
    """
    Used internally. This is True for window actions whose window 
    use the parameter panel: grid and emptytable (but not showdetail)
    """
    
    
    defining_actor = None
    """
    Internally used to store the :class:`lino.core.actors.Actor` 
    who defined this action.
    """
    
    key = None
    """
    The hotkey. Currently not used.
    """
    
    callable_from = None
    """
    Either `None`(default) or a tuple of class 
    objects (subclasses of :class:`Action`).
    If specified, this action is available only within a window 
    that has been opened by one of the given actions.
    """
    
    default_format = 'html'
    """
    Used internally.
    """
    
    readonly = True
    """
    Whether this action possibly modifies data *in the given object*.
    
    This means that :class:`InsertRow` is a `readonly` action.
    Actions like :class:`InsertRow` and :class:`Duplicable <lino.mixins.duplicable.Duplicate>` 
    which do not modify the given object but *do* modify the database,
    must override their `get_action_permission`::
    
      def get_action_permission(self,ar,obj,state):
          if user.profile.readonly: 
              return False
          return super(Duplicate,self).get_action_permission(ar,obj,state)
        
    
    """
    
    opens_a_window = False
    """
    Used internally to say whether this action opens a window.
    """
    
    hide_top_toolbar = False
    """
    Used internally if :attr:`opens_a_window` to say whether 
    the window has a top toolbar.
    """
    
    hide_navigator = False
    """
    Used internally if :attr:`opens_a_window` to say whether the window has a navigator.
    """
    
    show_in_bbar = True
    """
    Used internally.
    Whether this action should be displayed as a button in the bottom toolbar and the context menu.
    """
    
    show_in_workflow = False
    """
    Used internally.
    Whether this action should be displayed 
    as the :meth:`workflow_buttons <lino.core.model.Model.workflow_buttons>`.
    """
    
    custom_handler = False
    """
    Whether this action is implemented as Javascript function call.
    (...)
    """
    
    
    #~ def __init__(self,label=None,url_action_name=None,required={},**kw):
    def __init__(self,label=None,**kw):
        """
        The first argument is the optional `label`,
        other arguments should be specified as keywords and can be 
        any of the existing class attributes.
        """
        #~ if url_action_name is not None:
            #~ if not isinstance(url_action_name,basestring):
                #~ raise Exception("%s name %r is not a string" % (self.__class__,url_action_name))
            #~ self.url_action_name = url_action_name
        if label is not None:
            self.label = label
            
        register_params(self)
        #~ setup_params_choosers(self.__class__)
            
        #~ if label is None:
            #~ label = self.label or self.url_action_name 
        for k,v in kw.items():
            if not hasattr(self,k):
                raise Exception("Invalid keyword %s" % k)
            setattr(self,k,v)
        #~ self.add_requirements()
        
        if self.show_in_workflow:
            self.custom_handler = True
            self.show_in_bbar = False
        else:
            self.show_in_bbar = True
        
        
        #~ self.set_required(**required)
        assert self.callable_from is None or isinstance(
            self.callable_from,(tuple,type)), "%s" % self
            

    def make_params_layout_handle(self,ui):
        #~ return self.action.params_layout.get_layout_handle(ui)
        return make_params_layout_handle(self,ui)
        
    #~ def add_requirements(self,**kw):
        #~ """
        #~ Override existing permission requirements.
        #~ Arguments: see :func:`lino.utils.jsgen.make_permission_handler`.
        #~ """
        #~ Permittable.add_requirements(self,**kw)
        #~ logger.info("20120628 set_required %s(%s)",self,kw)
        #~ new = dict()
        #~ new.update(self.required)
        #~ new.update(kw)
        #~ self.required = new
        #~ if self.required.has_key('states'):
            #~ self.show_in_workflow = True
            #~ self.custom_handler = True
            #~ self.show_in_bbar = False
        #~ else:
            #~ self.show_in_workflow = False
            #~ self.show_in_bbar = True
        
    def get_button_label(self,actor):
        if actor is None:
            return self.label 
        if self is actor.default_action.action:
            return actor.label 
        else:
            return u"%s %s" % (self.label,actor.label)
            
    def full_name(self,actor):
        if self.action_name is None:
            raise Exception("Tried to full_name() on %r" % self)
            #~ return repr(self)
        if self.parameters:
            return self.defining_actor.actor_id + '.' + self.action_name
        return str(actor) + '.' + self.action_name
        
    def as_button(self,obj,request,label):
        ba = self.defining_actor.get_url_action(self.action_name)
        btn = settings.LINO.ui.row_action_button(obj,request,ba,label)
        return xghtml.E.tostring(btn)
        
        
        
    def __repr__(self):
        return "%s %s.%s" % (self.__class__.__name__,self.defining_actor,self.action_name)
        
    def __str__(self):
        if self.defining_actor is None:
            return repr(self)
        return unicode(self.defining_actor.label).encode('ascii','replace') + ' : ' + unicode(self.label).encode('ascii','replace')
        
    def unused__str__(self):
        raise Exception("20121003 Must use full_name(actor)") 
        if self.defining_actor is None:
            return repr(self)
        if self.action_name is None:
            return repr(self)
        return str(self.defining_actor) + ':' + self.action_name
        
    #~ def set_permissions(self,*args,**kw)
        #~ self.permission = perms.factory(*args,**kw)
        
    def attach_to_workflow(self,wf,name):
        assert self.action_name is None
        self.action_name = name
        self.defining_actor = wf
        #~ logger.info("20121009 %r attach_to_workflow(%s)",self,self.full_name(wf))
        setup_params_choosers(self.__class__)
        
    def attach_to_actor(self,actor,name):
        #~ if self.name is not None:
            #~ raise Exception("%s tried to attach named action %s" % (actor,self))
        #~ if actor == self.defining_actor:
            #~ raise Exception('20121003 %s %s' % (actor,name))
        if self.defining_actor is not None:
            # already defined in another actor
            return
        if self.action_name is not None:
            raise Exception("tried to attach named action %s.%s" % (actor,self.action_name))
        self.action_name = name
        self.defining_actor = actor
        if self.label is None:
            self.label = name
        #~ if actor.hide_top_toolbar:
            #~ self.hide_top_toolbar = True
        #~ if self.help_text is None \
            #~ and name == actor.get_default_action():
            #~ self.help_text  = actor.help_text
        #~ if name == 'default_action':
            #~ print 20120527, self
        setup_params_choosers(self.__class__)
            
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
        
    def get_action_permission(self,ar,obj,state):
        """
        Derived Action classes may override this to add vetos.
        E.g. DispatchAction is not available for a User with empty partner.
        """
        return True
        
    def get_view_permission(self,profile):
        """
        Overridden by :class:`lino_welfare.modlib.pcsw.models.BeIdReadCardAction`
        to make it available only when :attr:`lino.Lino.use_eid_jslib` is True.
        """
        return True
        
    #~ def run(self,elem,ar,**kw):
        #~ raise NotImplementedError("%s has no run() method" % self.__class__)

    #~ def request(self,*args,**kw):
        #~ kw.update(action=self)
        #~ return self.defining_actor.request(*args,**kw)
        
    def action_param_defaults(self,ar,obj,**kw):
        """
        Same as Actor.param_defaults, except that here it is a instance method
        """
        for k,pf in self.parameters.items():
            kw[k] = pf.get_default()
        return kw
        
    def setup_action_request(self,actor,ar):
        pass
        

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
    TODO: rename RowAction to ServerSideAction or AjaxAction
    Base class for actions that are executed server-side, 
    either on an individual row (if `single_row` is True) 
    or on a list.
    """
    single_row = True
    preprocessor = None
    http_method = 'GET'
    
    def get_panel_btn_handler(self,actor,renderer):
        if self.single_row:
            h  = 'Lino.row_action_handler('
        else:
            h  = 'Lino.list_action_handler('
            ls_url = '/' + actor.app_label + '/' + actor.__name__
            h += "%r," % ls_url
        h += "%r" % self.action_name
        h += ",%r" % self.http_method
        if self.preprocessor:
            h += "," + self.preprocessor
        h += ")"
        return h 
        
    def run(self,row,ar,**kw):
        """
        Execute the action on the given `row`. `ar` is an :class:`ActionRequest` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run() method" % self.__class__)

    #~ def get_action_permission(self,user,obj):
        #~ return self.actor.get_row_permission(self,ar,obj)
            
    #~ def attach_to_actor(self,actor,name):
        #~ super(RowAction,self).attach_to_actor(actor,name)
        #~ if not self.url_action_name:
            #~ self.url_action_name = name 



class RedirectAction(Action):
    
    def get_target_url(self,elem):
        raise NotImplementedError
        



class GridEdit(TableAction):
  
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True
    #~ icon_file = 'application_view_list.png' # used e.g. by quick_add_buttons()

    callable_from = tuple()
    action_name = 'grid'
    
    def attach_to_actor(self,actor,name):
        #~ self.label = actor.button_label or actor.label
        self.label = actor.label
        super(GridEdit,self).attach_to_actor(actor,name)

    def get_window_layout(self,actor):
        #~ return self.actor.list_layout
        return None


class BeIdReadCardAction(RowAction):
    preprocessor = 'Lino.beid_read_card_processor'
    http_method = 'POST'
    
    def get_button_label(self,actor):
        return self.label 
        
    def get_view_permission(self,profile):
        if not settings.LINO.use_eid_jslib:
            return False
        return super(BeIdReadCardAction,self).get_view_permission(profile)
  


class unused_ListAction(Action):
    """
    Base class for actions that are executed server-side on a set of rows.
    """
    callable_from = (GridEdit,)
    def get_panel_btn_handler(self,actor,renderer):
        assert self.action_name is not None
        return "Lino.list_action_handler(%r)" % self.action_name
        #~ url = ui.ext_renderer.get_actor_url(actor)
        #~ return "%s(%r,%r,%r)" % (self.js_handler,url,self.action_name,self.http_method)


class unused_JavaScriptAction(Action):
    """
    Base class for actions that are executed server-side on an individual row.
    """
    callable_from = (GridEdit,)
    js_handler = None
    http_method = 'GET'
    
    def get_panel_btn_handler(self,actor,renderer):
        url = renderer.get_actor_url(actor)
        return "%s(%r,%r,%r)" % (self.js_handler,url,self.action_name,self.http_method)

    def run(self,row,ar,**kw):
        """
        Execute the action on the given `row`. `ar` is an :class:`ActionRequest` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run() method" % self.__class__)
        

class unused_BeIdReadCardAction(unused_JavaScriptAction):
    """
    Explore the data read from an eid card and decide what to do with it.
    
    The client browser reads a Belgian eId card using :attr:`lino.Lino.use_eid_jslib`,
    then sends the data to the server where this action's `run` method will 
    be called. Possible actions are to create a new client or to update data 
    in existing client.
    
    """
    js_handler = 'Lino.beid_read_card_handler'
    http_method = 'POST'
    
    def get_view_permission(self,profile):
        if not settings.LINO.use_eid_jslib:
            return False
        return super(BeIdReadCardAction,self).get_view_permission(profile)

        


class ShowDetailAction(RowAction):
    """
    An action that opens the Detail Window of its actor.
    """
    icon_name = 'x-tbar-detail'
    #~ icon_file = 'application_form.png'
    opens_a_window = True
    show_in_workflow = False
    
    sort_index = 20
    callable_from = (GridEdit,)
    #~ show_in_detail = False
    #~ needs_selection = True
    action_name = 'detail'
    label = _("Detail")
    help_text = _("Open a detail window on this record")
    
    def get_window_layout(self,actor):
        return actor.detail_layout
        
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
        

RowAction.callable_from = (GridEdit,ShowDetailAction)

class InsertRow(TableAction):
    """
    Opens the Insert window filled with a blank row. 
    The new row will be actually created only when this 
    window gets submitted.
    """
    label = _("New")
    icon_name = 'x-tbar-new' # if action rendered as toolbar button
    icon_file = 'add.png' # if action rendered by quick_add_buttons
    show_in_workflow = False
    opens_a_window = True
    hide_navigator = True
    sort_index = 10
    hide_top_toolbar = True
    help_text = _("Insert a new record")
    #~ readonly = False # see blog/2012/0726
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    action_name = 'insert'
    #~ label = _("Insert")
    key = INSERT # (ctrl=True)
    #~ needs_selection = False
    
    def get_action_title(self,rr):
        return _("Insert into %s") % force_unicode(rr.get_title())
        
    def get_window_layout(self,actor):
        return actor.insert_layout or actor.detail_layout

    def get_action_permission(self,ar,obj,state):
        # see blog/2012/0726
        if ar.get_user().profile.readonly: 
            return False
        return super(InsertRow,self).get_action_permission(ar,obj,state)




class DuplicateRow(RowAction):
    opens_a_window = True
  
    readonly = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    action_name = 'duplicate'
    label = _("Duplicate")


class ShowEmptyTable(ShowDetailAction):
    use_param_panel = True
    callable_from = tuple()
    action_name = 'show' 
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    icon_name = None
    
    def attach_to_actor(self,actor,name):
        self.label = actor.label
        ShowDetailAction.attach_to_actor(self,actor,name)
        #~ print 20120523, actor, name, 'setup', unicode(self.label)
        
    def get_action_title(self,rr):
        return rr.get_title()
    #~ def __str__(self):
        #~ return str(self.actor)+'.'+self.name
        
    

class UpdateRowAction(RowAction):
    show_in_workflow = False
    readonly = False
    required = dict(user_level='user')
    

class DeleteSelected(RowAction):
    """
    Delete the row.
    """
    icon_name = 'x-tbar-delete'
    help_text = _("Delete this record")
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    #~ url_action_name = 'delete'
    key = DELETE # (ctrl=True)
    #~ client_side = True
    
        
class SubmitDetail(RowAction):
    sort_index = 10
    switch_to_detail = False
    icon_name = 'x-tbar-save'
    help_text = _("Save changes in this form")
    label = _("Save")
    auto_save = False
    show_in_workflow = False
    #~ show_in_bbar = True
    action_name = 'put'
    readonly = False
    required = dict(user_level='user')
    #~ url_action_name = 'SubmitDetail'
    callable_from = (ShowDetailAction,)
    
class SubmitInsert(SubmitDetail):
    sort_index = 10
    switch_to_detail = True
    icon_name = None # don't inherit 'x-tbar-save' from Submitdetail 
    #~ url_action_name = 'SubmitInsert'
    label = _("Create")
    action_name = 'post'
    help_text = _("Create the record and open a detail window on it")
    #~ label = _("Insert")
    callable_from = (InsertRow,)
    
class SubmitInsertAndStay(SubmitInsert):
    sort_index = 11
    switch_to_detail = False
    action_name = 'poststay'
    label = _("Create without detail")
    help_text = _("Don't open an detail window on the new record")

    
    
class NotifyingAction(RowAction):
    
    parameters = dict(
        notify_subject = models.CharField(_("Summary"),blank=True,max_length=200),
        notify_body = fields.RichTextField(_("Description"),blank=True),
        notify_silent = models.BooleanField(_("Don't send email notification"),default=False),
    )
    
    params_layout = layouts.Panel("""
    notify_subject
    notify_body
    notify_silent
    """,window_size=(50,15))
    
    #~ def update_system_note_kw(self,ar,kw,obj):
        #~ pass
        
    def get_notify_subject(self,ar,obj):
        """
        Return the default value of the `notify_subject` field.
        """
        return None
        
    def get_notify_body(self,ar,obj):
        """
        Return the default value of the `notify_body` field.
        """
        return None
        
    def action_param_defaults(self,ar,obj,**kw):
        kw = super(NotifyingAction,self).action_param_defaults(ar,obj,**kw)
        s = self.get_notify_subject(ar,obj)
        if s is not None: kw.update(notify_subject=s)
        s = self.get_notify_body(ar,obj)
        if s is not None: kw.update(notify_body=s)
        return kw
        
    def run(self,obj,ar,**kw):
        kw.update(message=ar.action_param_values.notify_subject)
        kw.update(alert=True)
        kw = super(NotifyingAction,self).run(obj,ar,**kw)
        self.add_system_note(ar,obj)
        return kw
    
    def add_system_note(self,ar,owner,**kw):
        #~ body = _("""%(user)s executed the following action:\n%(body)s
        #~ """) % dict(user=ar.get_user(),body=body)
        ar.add_system_note(
            owner,
            ar.action_param_values.notify_subject,
            ar.action_param_values.notify_body,
            ar.action_param_values.notify_silent,**kw)
        
    


class BaseRequest(object):
    def __init__(self,ui,request=None,renderer=None,**kw):
        if ui is None:
            ui = settings.LINO.ui
            #~ from lino.ui.extjs3 import ui
        self.ui = ui
        self.error_response = ui.error_response
        self.success_response = ui.success_response
        if renderer is None:
            renderer = ui.text_renderer
        self.renderer = renderer
        self.step = 0 # confirmation counter
        #~ self.report = actor
        self.request = request
        if request is not None:
            if request.method == 'PUT':
                rqdata = http.QueryDict(request.raw_post_data)
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
        
        
    def dialog(self,dlg):
        # not finished
        self.step += 1
        if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            return
        raise DialogRequired(self.step,dlg)
        
    def confirm(self,*messages):
        """
        Calling this from an Action's :meth:`Action.run` method will
        interrupt the execution, send the specified message(s) back to 
        the user, waiting for confirmation before continuing.
        
        Note that this is implemented without any server sessions 
        and cookies. While this system is genial, it has one drawback 
        which you should be aware of: the code execution does not 
        *continue* after the call to `confirm` but starts again at the 
        beginning (with the difference that the client this time calls it with 
        an internal `step` parameter that tells Lino that this `confirm()` 
        has been answered and should no longer raise stop execution.
        """
        assert len(messages) > 0 and messages[0], "At least one non-empty message required"
        self.step += 1
        if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            return
        raise ConfirmationRequired(self.step,messages)
        
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
    - :meth:`confirm <lino.core.actions.ActionRequest.confirm>`
    - :meth:`success_response <lino.ui.base.UI.success_response>`
    - :meth:`error_response <lino.ui.base.UI.error_response>`
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
            
        if self.bound_action.action.parameters is not None:
            apv = self.bound_action.action.action_param_defaults(self,None)
            if request is not None:
                #~ pv.update(self.ui.parse_params(self.ah,request))
                #~ pv.update(self.ah.store.parse_params(request))
                apv.update(self.bound_action.action.params_layout.params_store.parse_params(request))
                
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
        
    def instance_handler(self,*args,**kw): return self.renderer.instance_handler(self,*args,**kw)
    def href_to(self,*args,**kw): return self.renderer.href_to(self,*args,**kw)
    def pk2url(self,*args,**kw): return self.renderer.pk2url(self,*args,**kw)
    def get_request_url(self,*args,**kw): return self.renderer.get_request_url(self,*args,**kw)
    def obj2html(self,*args,**kw): return self.renderer.obj2html(self,*args,**kw)
    def href_to_request(self,*args,**kw): return self.renderer.href_to_request(self,*args,**kw)
    def row_action_button(self,obj,a,*args,**kw): return self.renderer.row_action_button(obj,self.request,a,*args,**kw)
        
    def absolute_uri(self,*args,**kw):
        ar = self.spawn(*args,**kw)
        location = ar.renderer.get_request_url(ar)
        return self.request.build_absolute_uri(location)
        
            
    def to_rst(self,column_names=None):
        """
        Returns a string representing this request in reStructuredText markup.
        """
        raise NotImplementedError()
            
            
        
        

def action(*args,**kw):
    """
    Decorator to define custom actions.
    Same signature as :meth:`Action.__init__`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required <Action.required>`
    """
    def decorator(fn):
        kw.setdefault('custom_handler',True)
        a = RowAction(*args,**kw)
        #~ a.run = curry(fn,a)
        a.run = fn
        return a
    return decorator
        
        
