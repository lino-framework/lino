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

import os
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
#~ from lino.utils import AttrDict
#~ from lino.utils import curry
#~ from lino.utils import jsgen
#~ from lino.utils import Warning
from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.core import constants

from lino.core.dbutils import resolve_model
from lino.core.dbutils import navinfo
from lino.core import layouts
#~ from lino.core import changes
from lino.core import fields

#~ from lino.core.perms import UserLevels
#~ from lino.core import perms 


PLAIN_PAGE_LENGTH = 15


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
    See :func:`lino.core.auth.make_permission_handler`.
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
    #~ if cls.__class__.__name__ == 'Merge':
        #~ print("20130121 register_params",cls.parameters)
        #~ assert cls.parameters is not None
    if cls.parameters:
        for k,v in cls.parameters.items():
            v.set_attributes_from_name(k)
            v.table = cls
            #~ v._datasource = cls
        if cls.params_layout is None:
            cls.params_layout = cls._layout_class.join_str.join(cls.parameters.keys())
        if isinstance(cls.params_layout,basestring):
            cls.params_layout = cls._layout_class(cls.params_layout,cls)
        elif isinstance(cls.params_layout,layouts.Panel):
            cls.params_layout = cls._layout_class(cls.params_layout.desc,cls,**cls.params_layout.options)
        
    elif cls.params_layout is not None:
        raise Exception("params_layout but no parameters ?!")

def setup_params_choosers(self):
    if self.parameters:
        from lino.utils.choosers import check_for_chooser
        for k,fld in self.parameters.items():
            if isinstance(fld,models.ForeignKey):
                fld.rel.to = resolve_model(fld.rel.to)
                from lino.core.kernel import set_default_verbose_name
                set_default_verbose_name(fld)
                #~ if fld.verbose_name is None:
                    #~ fld.verbose_name = fld.rel.to._meta.verbose_name
                
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
    If this table or action has parameters, specify here how they should be 
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
        
        
    #~ @classmethod
    #~ def get_param_elem(self,name):
        #~ if self.__name__ == 'Merge':
            #~ if not isinstance(self.params_layout,self._layout_class):
                #~ raise Exception("20130121 self.params_layout is a %s" % self.params_layout.__class__)
            #~ print("20130121 get_param_elem",self.params_layout._datasource)

        #~ if self.parameters:
            #~ return self.parameters.get(name,None)
        #~ return None
      
    #~ @classmethod
    def get_window_layout(self,actor):
        return self.params_layout
        
    def get_window_size(self,actor):
        wl = self.get_window_layout(actor)
        if wl is not None:
            return wl.window_size
        
        
#~ class ActionMetaClass(type):
    #~ def __new__(meta, classname, bases, classDict):
        #~ cls = type.__new__(meta, classname, bases, classDict)
        #~ cls.register_params()
        #~ return cls
      
#~ class ActionRunner(object):
class InstanceAction(object):
    """
    Wrapper object used to run actions from Python code.
    """
    def __init__(self,action,actor,instance,owner):
        #~ print "Bar"
        #~ self.action = action
        self.bound_action = actor.get_action_by_name(action.action_name)
        self.instance = instance
        self.owner = owner
        
    def run_from_code(self,ar,**kw):
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_code(ar)
        
    def run_from_ui(self,ar,**kw):
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_ui(ar)
        
        
    def run_from_session(self,ses,**kw):
        #~ print self,args, kw
        ar = self.bound_action.request(**kw)
        ar.setup_from(ses)
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_code(ar)

    #~ def as_button(self,obj,request,label=None):
        #~ print "Foo"
        #~ ba = self.defining_actor.get_url_action(self.action_name)
        #~ btn = settings.SITE.ui.row_action_button(obj,request,ba,label)
        #~ return E.tostring(btn)
        
    def as_button_elem(self,request,label=None):
        return settings.SITE.ui.row_action_button(self.instance,request,self.bound_action,label)
        
    #~ def as_button(self,request,label=None):
    def as_button(self,*args,**kw):
        """
        Return a HTML chunk with a "button" which, when clicked, will 
        execute this action on this instance.
        This is being used in the :ref:`lino.tutorial.polls`.
        """
        #~ btn = settings.SITE.ui.row_action_button(self.instance,request,self.bound_action,label)
        return E.tostring(self.as_button_elem(*args,**kw))

class Action(Parametrizable,Permittable):
    """
    Abstract base class for all Actions
    """
    
    #~ __metaclass__ = ActionMetaClass
    
    debug_permissions = False
    
    icon_name = None 
    """
    The class name of an icon to be used for this action
    when rendered as toolbar button.
    """
    
    #~ icon_file = None
    #~ """
    #~ The file name of an icon to be used for this action
    #~ when rendered by quick_add_buttons.
    #~ """
    
    _layout_class = layouts.ActionParamsLayout
    
    hidden_elements = frozenset()
    
    combo_group = None
    """
    The name of another action to which to "attach" this action.
    Both actions will then be rendered as a single combobutton.
    """
    
    sort_index = 90
    """
    Determins the sort order in which the actions will be presented to 
    the user.
    
    List actions are negative and come first.
    
    Predefined `sort_index` values are:
    
    ===== =================================
    value action
    ===== =================================
    -1    :class:`as_pdf <lino.utils.appy_pod.PrinttableAction>`
    10    :class:`insert <InsertRow>`, SubmitDetail
    11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate>`
    20    :class:`detail <ShowDetailAction>`
    30    :class:`delete <DeleteSelected>`
    31    :class:`merge <lino.mixins.mergeable.Merge>`
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
    
    def is_callable_from(self,caller):
        return isinstance(caller,(GridEdit,ShowDetailAction))
        #~ if self.select_rows:
            #~ return isinstance(caller,(GridEdit,ShowDetailAction))
        #~ return isinstance(caller,GridEdit)
    
    #~ callable_from = None
    #~ """
    #~ Either `None`(default) or a tuple of class 
    #~ objects (subclasses of :class:`Action`).
    #~ If specified, this action is available only within a window 
    #~ that has been opened by one of the given actions.
    #~ """
    
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
    
    show_in_row_actions = False
    """
    No longer used.
    Whether this action should be displayed as a button in the 
    :meth:`action_buttons <lino.core.model.Model.action_buttons>`    
    column.
    """
    
    show_in_workflow = False
    """
    Used internally.
    Whether this action should be displayed 
    as the :meth:`workflow_buttons <lino.core.model.Model.workflow_buttons>` column.
    """
    
    custom_handler = False
    """
    Whether this action is implemented as Javascript function call.
    (...)
    """
    
    select_rows = True
    """
    Set this to False if this action is a list action, not a row action.
    """
    
    http_method = 'GET'
    """
    HTTP method to use when this action is called using an AJAX call.
    """
    
    preprocessor = 'null' # None
    """
    Name of a Javascript function to be invoked on the web client when
    this action is called.
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
            
            
        #~ if label is None:
            #~ label = self.label or self.url_action_name 
        for k,v in kw.items():
            if not hasattr(self,k):
                raise Exception("Invalid action keyword %s" % k)
            setattr(self,k,v)
        #~ self.add_requirements()
        
        if self.show_in_workflow:
            self.custom_handler = True
            self.show_in_bbar = False
        else:
            self.show_in_bbar = True
            
        if self.show_in_row_actions:
            self.custom_handler = True
        
        
        #~ self.set_required(**required)
        #~ assert self.callable_from is None or isinstance(
            #~ self.callable_from,(tuple,type)), "%s" % self
            
        #~ if self.parameters is None:
            #~ assert self.params_layout is None
        #~ else:
            #~ assert self.params_layout is not None
            
        register_params(self)
        #~ setup_params_choosers(self.__class__)
        
        if self.parameters is not None:
            if not isinstance(self.params_layout,self._layout_class):
                raise Exception("20130121 %s" % self)
            #~ assert isinstance(self.params_layout,self._layout_class)
            
        if hasattr(self,'run'):
            raise Exception(str(self))
            
      
    def __get__(self, instance, owner):
        """
        When a model has an action "foo", then getting an attribute
        "foo" of a model instance will return an :class:`InstanceAction`.
        """
        if instance is None:
            return self
        return InstanceAction(self,instance.get_default_table(),instance,owner)
        
        
    def as_html(self,ar):
        return "Oops, no as_html method for %s" % self

    def make_params_layout_handle(self,ui):
        #~ return self.action.params_layout.get_layout_handle(ui)
        return make_params_layout_handle(self,ui)
        
    #~ @classmethod
    def get_param_elem(self,name):
        # same as in Actor but here it is an instance method
        if self.parameters:
            return self.parameters.get(name,None)
        return None
        
        
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
        
    #~ def as_button(self,obj,request,label=None):
        #~ """
        #~ Return 
        #~ This is being used in the :ref:`lino.tutorial.polls`.
        #~ """
        #~ ba = self.defining_actor.get_url_action(self.action_name)
        #~ btn = settings.SITE.ui.row_action_button(obj,request,ba,label)
        #~ return E.tostring(btn)
        
    def get_action_title(self,ar):
        return ar.get_title()
        
    def __repr__(self):
        #~ return "<%s %s.%s>" % (self.__class__.__name__,self.defining_actor,self.action_name)
        if self.label is None:
            return "<%s %s>" % (self.__class__.__name__,self.action_name)
        return "<%s %s (%r)>" % (self.__class__.__name__,self.action_name,unicode(self.label))
        
    #~ def __str__(self):
        #~ if self.defining_actor is None:
            #~ return repr(self)
        #~ return unicode(self.defining_actor.label).encode('ascii','replace') + ' : ' + unicode(self.label).encode('ascii','replace')
        
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
            return True
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
        return True
            
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
        E.g. DispatchAction is not available for a User with empty 
        partner.
        Or MoveUp action of a Sequenced is not available on the first 
        row of given `ar`.
        """
        return True
        
    def get_view_permission(self,profile):
        """
        Overridden e.g. by :class:`lino.mixins.beid.BeIdReadCardAction`
        to make it available only when :attr:`lino.Lino.use_eid_jslib` is True.
        """
        return True
        
        
    def run_from_code(self,ar,**kw):
        return self.run_from_ui(ar,**kw)
        
    def run_from_ui(self,ar,**kw):
        """
        Execute the action on the given `row`. 
        `ar` is an :class:`ActionRequest <lino.core.requests.ActionRequest>` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run_from_ui() method" % self.__class__)

    def run_from_session(self,ses,obj,*args,**kw): # 20130820
        #~ ba = action.defining_actor.get_action_by_name(action.action_name)
        ia = InstanceAction(self,self.defining_actor,obj,None)
        return ia.run_from_session(ses,*args,**kw)
        
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
    
    def get_action_title(self,ar):
        return ar.get_title()


class RedirectAction(Action):
    
    def get_target_url(self,elem):
        raise NotImplementedError
        



class GridEdit(TableAction):
    
    #~ debug_permissions = 20130704 
  
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True
    #~ icon_file = 'application_view_list.png' # used e.g. by quick_add_buttons()

    #~ callable_from = tuple()
    action_name = 'grid'
    
    def is_callable_from(self,caller):
        return False
    
    def attach_to_actor(self,actor,name):
        #~ self.label = actor.button_label or actor.label
        self.label = actor.label
        return super(GridEdit,self).attach_to_actor(actor,name)

    def get_window_layout(self,actor):
        #~ return self.actor.list_layout
        return None
        
    def get_window_size(self,actor):
        return actor.window_size
        
    def as_html(self,ar):
        t = xghtml.Table()
        #~ settings.SITE.ui.ar2html(ar,t,ar.sliced_data_iterator)
        ar.dump2html(t,ar.sliced_data_iterator)
        #~ return t.as_element() # 20130418
        buttons = []
        if ar.limit is None:
            ar.limit = PLAIN_PAGE_LENGTH
        pglen = ar.limit 
        if ar.offset is None:
            page = 1
        else:
            """
            (assuming pglen is 5)
            offset page
            0      1
            5      2
            """
            page = int(ar.offset / pglen) + 1
        kw = dict()
        kw = {}
        if pglen != PLAIN_PAGE_LENGTH:
            kw[constants.URL_PARAM_LIMIT] = pglen
          
        if page > 1:
            kw[constants.URL_PARAM_START] = pglen * (page-2) 
            prev_url = ar.get_request_url(**kw)
            kw[constants.URL_PARAM_START] = 0
            first_url = ar.get_request_url(**kw)
        else:
            prev_url = None
            first_url = None
        buttons.append( ('<<',_("First page"), first_url ))
        buttons.append( ('<',_("Previous page"), prev_url ))
        
        next_start = pglen * page 
        if next_start < ar.get_total_count():
            kw[constants.URL_PARAM_START] = next_start
            next_url = ar.get_request_url(**kw)
            last_page = int((ar.get_total_count()-1) / pglen)
            kw[constants.URL_PARAM_START] = pglen * last_page
            last_url = ar.get_request_url(**kw)
        else:
            next_url = None 
            last_url = None 
        buttons.append( ('>',_("Next page"), next_url ))
        buttons.append( ('>>',_("Last page"), last_url ))
        
        items = []
        for symbol,label,url in buttons:
            if url is None:
                items.append(E.li(E.span(symbol,class_="disabled")))
            else:
                items.append(E.li(E.a(symbol,href=url)))
        pager = E.div(E.ul(*items),class_='pagination')
        
        return E.div(pager,t.as_element())
      
        





class ShowDetailAction(Action):
    """
    An action that opens the Detail Window of its actor.
    """
    icon_name = 'application_form'
    #~ icon_file = 'application_form.png'
    opens_a_window = True
    show_in_workflow = False
    #~ show_in_row_actions = True
    
    
    sort_index = 20
    #~ callable_from = (GridEdit,)
    
    def is_callable_from(self,caller):
        return isinstance(caller,GridEdit)
    
    #~ show_in_detail = False
    #~ needs_selection = True
    action_name = 'detail'
    label = _("Detail")
    help_text = _("Open a detail window on this record")
    
    def get_window_layout(self,actor):
        return actor.detail_layout
        
    def get_window_size(self,actor):
        wl = self.get_window_layout(actor)
        return wl.window_size
        
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
        
        
    def as_html(self,ar,pk):
        ah = ar.ah
        ba = ar.bound_action
        rpt = ar.actor

        
        navigator = None
        if pk and pk != '-99999' and pk != '-99998':
            elem = rpt.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
                #~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
            if ar.actor.show_detail_navigator:
              
                ni = navinfo(ar.data_iterator,elem)
                if ni:
                    buttons = []
                    buttons.append( ('*',_("Home"), '/' ))
                    
                    buttons.append( ('<<',_("First page"), ar.pk2url(ni['first']) ))
                    buttons.append( ('<',_("Previous page"), ar.pk2url(ni['prev']) ))
                    buttons.append( ('>',_("Next page"), ar.pk2url(ni['next']) ))
                    buttons.append( ('>>',_("Last page"), ar.pk2url(ni['last']) ))
                        
                    chunks = []
                    for text,title,url in buttons:
                        chunks.append('[')
                        if url:
                            chunks.append(E.a(text,href=url,title=title))
                        else:
                            chunks.append(text)
                        chunks.append('] ')
                    navigator = E.p(*chunks)
        else:
            elem = None
        
        
        wl = ar.bound_action.get_window_layout()
        #~ print 20120901, wl.main
        lh = wl.get_layout_handle(settings.SITE.ui)
        
        #~ items = list(render_detail(ar,elem,lh.main))
        items = list(lh.main.as_plain_html(ar,elem))
        #~ print E.tostring(E.div())
        #~ if len(items) == 0: return ""
        main = E.form(*items)
        #~ print 20120901, lh.main.__html__(ar)
        """
        The method="html" argument isn't available in Python 2.6, only 2.7
        It is useful to avoid side effects in case of empty elements:
        the default method (xml) writes an empty E.div() as "<div/>"
        while in HTML5 it must be "<div></div>" (the ending / is ignored)
        """
        #~ return E.tostring(main,method="html")
        #~ return E.tostring(main)
        return main
        
        

#~ Action.callable_from = (GridEdit,ShowDetailAction)

class InsertRow(TableAction):
    """
    Opens the Insert window filled with a blank row. 
    The new row will be actually created only when this 
    window gets submitted.
    """
    #~ debug_permissions = 20130924

    label = _("New")
    #~ icon_name = 'x-tbar-new' # if action rendered as toolbar button
    icon_name = 'add' # if action rendered as toolbar button
    #~ icon_file = 'add.png' # if action rendered by quick_add_buttons
    show_in_workflow = False
    opens_a_window = True
    hide_navigator = True
    sort_index = 10
    hide_top_toolbar = True
    help_text = _("Insert a new record")
    #~ readonly = False # see blog/2012/0726
    required = dict(user_level='user')
    #~ callable_from = (GridEdit,ShowDetailAction)
    action_name = 'insert'
    #~ label = _("Insert")
    key = INSERT # (ctrl=True)
    #~ needs_selection = False
    
    def get_action_title(self,ar):
        return _("Insert into %s") % force_unicode(ar.get_title())
        
    def get_window_layout(self,actor):
        return actor.insert_layout or actor.detail_layout

    def get_window_size(self,actor):
        wl = self.get_window_layout(actor)
        return wl.window_size

    def get_action_permission(self,ar,obj,state):
        # see blog/2012/0726
        if ar.get_user().profile.readonly: 
            return False
        return super(InsertRow,self).get_action_permission(ar,obj,state)




#~ class DuplicateRow(Action):
    #~ opens_a_window = True
  #~ 
    #~ readonly = False
    #~ required = dict(user_level='user')
    #~ callable_from = (GridEdit,ShowDetailAction)
    #~ action_name = 'duplicate'
    #~ label = _("Duplicate")
#~ 

class ShowEmptyTable(ShowDetailAction):
    use_param_panel = True
    #~ callable_from = tuple()
    action_name = 'show' 
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    icon_name = None
    
    def is_callable_from(self,caller):
        return True
    
    def attach_to_actor(self,actor,name):
        self.label = actor.label
        return super(ShowEmptyTable,self).attach_to_actor(actor,name)
        
    def as_html(self,ar):
        return super(ShowEmptyTable,self).as_html(ar,'-99998')

class UpdateRowAction(Action):
    show_in_workflow = False
    readonly = False
    required = dict(user_level='user')
    
        
class DeleteSelected(Action):
    """
    Delete the row on which it is being executed.
    """
    #~ debug_permissions = "20130222"
    #~ icon_name = 'x-tbar-delete'
    icon_name = 'delete'
    help_text = _("Delete this record")
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    required = dict(user_level='user')
    #~ callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    #~ url_action_name = 'delete'
    key = DELETE # (ctrl=True)
    #~ client_side = True
    
        
class SubmitDetail(Action):
    #~ debug_permissions = 20130128
    sort_index = 10
    switch_to_detail = False
    #~ icon_name = 'x-tbar-save'
    icon_name = 'disk'
    help_text = _("Save changes in this form")
    label = _("Save")
    auto_save = False
    show_in_workflow = False
    #~ show_in_bbar = True
    action_name = 'put'
    readonly = False
    required = dict(user_level='user')
    #~ url_action_name = 'SubmitDetail'
    #~ callable_from = (ShowDetailAction,)
    
    def is_callable_from(self,caller):
        return isinstance(caller,ShowDetailAction)
    
    
class SubmitInsert(SubmitDetail):
    switch_to_detail = True
    icon_name = None # don't inherit 'x-tbar-save' from Submitdetail 
    #~ url_action_name = 'SubmitInsert'
    label = _("Create")
    action_name = 'post'
    help_text = _("Create the record and open a detail window on it")
    #~ label = _("Insert")
    #~ callable_from = (InsertRow,)
    
    def is_callable_from(self,caller):
        return isinstance(caller,InsertRow)
    
    
    
class SubmitInsertAndStay(SubmitInsert):
    sort_index = 11
    switch_to_detail = False
    action_name = 'poststay'
    label = _("Create without detail")
    help_text = _("Don't open a detail window on the new record")

    



class ShowSlaveTable(Action):
    TABLE2ACTION_ATTRS = tuple('sort_index help_text icon_name label'.split())
    #~ label = "ShowSlaveTable"
    #~ show_in_row_actions = True
    show_in_bbar = True
    
    def __init__(self,slave_table,**kw):
        self.slave_table = slave_table
        #~ kw.setdefault('label',slave_table.label)
        super(ShowSlaveTable,self).__init__(**kw)

    @classmethod
    def get_actor_label(self):
        return self._label or self.slave_table.label
        
    def attach_to_actor(self,actor,name):
        if isinstance(self.slave_table,basestring):
            self.slave_table = settings.SITE.modules.resolve(self.slave_table)
        for k in self.TABLE2ACTION_ATTRS:
            setattr(self,k,getattr(self.slave_table,k))
        #~ self.label = self.slave_table.label
        #~ self.help_text = self.slave_table.help_text
        #~ self.icon_name = self.slave_table.icon_name
        #~ self.icon_file = self.slave_table.icon_file
        return super(ShowSlaveTable,self).attach_to_actor(actor,name)
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        #~ ba = self.slave_table.default_action
        sar = ar.spawn(self.slave_table,master_instance=obj)
        js = ar.renderer.request_handler(sar)
        #~ js = ar.renderer.action_call(ar.requesting_panel,ba,{})
        kw.update(eval_js=js)
        return kw

    
class NotifyingAction(Action):
    
    show_in_row_actions = True
    
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
        if obj is not None:
            s = self.get_notify_subject(ar,obj)
            if s is not None: kw.update(notify_subject=s)
            s = self.get_notify_body(ar,obj)
            if s is not None: kw.update(notify_body=s)
        return kw
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        kw.update(message=ar.action_param_values.notify_subject)
        #~ kw.update(alert=True)
        kw.update(refresh=True)
        kw.update(success=True)
        #~ kw = super(NotifyingAction,self).run_from_ui(obj,ar,**kw)
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
        
    


        

def action(*args,**kw):
    """
    Decorator to define custom actions.
    Same signature as :meth:`Action.__init__`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required <Action.required>`.
    
    The decorated function must return a `dict` which allowed 
    keys are defined in :attr:`lino.ui.base.ACTION_RESPONSES`.
    """
    def decorator(fn):
        kw.setdefault('custom_handler',True)
        #~ kw.setdefault('show_in_row_actions',True)
        a = Action(*args,**kw)
        #~ a.run = curry(fn,a)
        def wrapped(ar):
            obj = ar.selected_rows[0]
            return fn(obj,ar)
        a.run_from_ui = wrapped
        return a
    return decorator
        
        
