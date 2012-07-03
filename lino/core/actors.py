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
This defines the :class:`Actor` class, the base class 
for 
:class:`dd.Table <lino.core.table.Table>`,
:class:`dd.VirtualTable <lino.utils.tables.VirtualTable>`
and :class:`dd.Frame <lino.core.frames.Frame>`.

"""

import logging
logger = logging.getLogger(__name__)

import copy

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

import lino
from lino.ui import base

#~ from lino.ui.base import Handled
from lino.core import fields
from lino.core import actions
from lino.core import layouts
from lino.core.modeltools import resolve_model
from lino.utils import curry, AttrDict
#~ from lino.utils.perms import ViewPermissionClass
from lino.utils import choicelists
from lino.utils import perms
#~ from lino.utils import jsgen

        


actor_classes = []
actors_list = None

ACTOR_SEP = '.'


MODULES = AttrDict()
  
def register_actor(a):
    #~ logger.debug("register_actor %s",a)
    old = MODULES.define(a.app_label,a.__name__,a)
    #~ old = actors_dict.get(a.actor_id,None)
    if old is not None:
        logger.debug("register_actor %s : %r replaced by %r",a,old,a)
        actors_list.remove(old)
    #~ actors_dict[a.actor_id] = a
    actors_list.append(a)
    return a
  
    #~ actor.setup()
    #~ assert not actors_dict.has_key(actor.actor_id), "duplicate actor_id %s" % actor.actor_id
    #~ actors_dict[actor.actor_id] = actor
    #~ return actor

def discover():
    global actor_classes
    global actors_list
    assert actors_list is None
    actors_list = []
    logger.debug("actors.discover() : setting up %d actors",len(actor_classes))
    for cls in actor_classes:
        register_actor(cls)
    actor_classes = None
    
    for a in actors_list:
        a.class_init()
        #~ a.collect_actions() # too early: e.g. Cities has no detail_layout yet, but pcsw.site_setup() defines one
        
        

class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
            
        
        """
        attributes that are not inherited from base classes:
        """
        # classDict.setdefault('name',classname)
        classDict.setdefault('label',None)
        #~ classDict.setdefault('button_label',None)
        classDict.setdefault('title',None)
        
        cls = type.__new__(meta, classname, bases, classDict)
        
        if cls.parameters:
            for k,v in cls.parameters.items():
                v.set_attributes_from_name(k)
                v.table = cls
                
        """
        On 20110822 I thought "A Table always gets the app_label of its model,
        you cannot set this yourself in a subclass
        because otherwise it gets complex when inheriting reports from other
        app_labels."
        On 20110912 I cancelled change 20110822 because PersonsByOffer 
        should clearly get app_label 'jobs' and not 'contacts'.
        
        """
        
        if classDict.get('app_label',None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            cls.app_label = cls.__module__.split('.')[-2]
        
        cls.actor_id = cls.app_label + '.' + cls.__name__
        cls._setup_done = False
        cls._setup_doing = False
                
        cls.virtual_fields = {}
        cls._constants = {}
        cls._actions_dict = {}
        cls._actions_list = None
        
        # inherit virtual fields defined on parent tables
        for b in bases:
            bd = getattr(b,'virtual_fields',None)
            if bd:
                cls.virtual_fields.update(bd)
            
        for k,v in classDict.items():
            if isinstance(v,fields.Constant):
                cls.add_constant(k,v)
            if isinstance(v,fields.VirtualField):
                cls.add_virtual_field(k,v)
                
                
        #~ cls.params = []
        #~ for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
                #~ v.set_attributes_from_name(k)
                #~ v.table = cls
                #~ cls.params.append(v)
                
        
        
        dt = classDict.get('detail_template',None)
        dl = classDict.get('detail_layout',None)
        if dt is not None:
            if dl is not None:
                raise Exception("%r has both detail_template and detail_layout" % cls)
            cls.detail_layout = layouts.FormLayout(cls,dt)
        elif dl is not None:
            assert dl._table is None
            dl._table = cls
            cls.detail_layout = dl
            
        # the same for insert_template and insert_layout:
        dt = classDict.get('insert_template',None)
        dl = classDict.get('insert_layout',None)
        if dt is not None:
            if not isinstance(dt,basestring):
                raise ValueError("%r : insert_template %r is not a string" % (cls,dt))
            if dl is not None:
                raise Exception("%r has both insert_template and insert_layout" % cls)
            cls.insert_layout = layouts.FormLayout(cls,dt)
        elif dl is not None:
            assert dl._table is None
            dl._table = cls
            cls.insert_layout = dl
                
        if classname not in (
            'Table','AbstractTable','VirtualTable',
            'Action','Actor','Frame',
            'EmptyTable'):
            if actor_classes is None:
                #~ logger.debug("%s definition was after discover",cls)
                pass
            elif not cls.__name__.startswith('unused_'):
                #~ logger.debug("Found actor %s.",cls)
                #~ cls.class_init() # 20120115
                actor_classes.append(cls)
            #~ logger.debug("ActorMetaClass.__new__(%s)", cls)
        return cls

    def __str__(self):
        return self.actor_id 
  

#~ class Actor(Handled,ViewPermission):
#~ class Actor(ViewPermissionClass):
class Actor(object):
    """
    Base class for Tables and Frames. 
    An alternative name for "Actor" is "Resource".
    """
    
    __metaclass__ = ActorMetaClass
    
    app_label = None
    """
    Specify this if you want to "override" an existing actor.
    
    The default value is deduced from the module where the 
    subclass is defined.
    
    Note that this attribute is not inherited from base classes.
    
    :func:`lino.core.table.table_factory` also uses this.
    """
    
    window_size = None
    """
    Set this to a tuple of (height, width) in pixels to have 
    this actor display in a modal non-maximized window.
    """
    
    default_list_action_name = 'grid'
    default_elem_action_name =  'detail'
    
    #~ hide_top_toolbar = False
    
    debug_permissions = False
    """
    When this is `True`, Lino logs an ``info`` message each time a permission handler 
    for an action on this actor is called. 
    Not to be used on a production site but useful for debugging.
    """
    
    required = dict()
    create_required = dict()
    update_required = dict()
    delete_required = dict()
    
    
    
    master_key = None
    """
    The name of the ForeignKey field of this Table's model that points to it's master.
    Setting this will turn the report into a slave report.
    """
    
    master = None
    """
    Automatically set to the model pointed to by the :attr:`master_key`.
    Used also in lino.models.ModelsBySite
    """
    
    master_field = None
    """
    For internal use. Automatically set to the field descriptor of the :attr:`master_key`.
    """
    
    editable = None
    """
    Set this explicitly to True or False to make the 
    Actor per se editable or not.
    Otherwise it will be set to `False` if the Actor is a Table has a `get_data_rows` method.
    """
    
    
    workflow_state_field = None 
    """
    The name of the field that contains the workflow state of an object.
    Subclasses may override this.
    """
    
    workflow_owner_field = None
    """
    The name of the field that contains the user who is 
    considered to own an object when `Rule.owned_only` is checked.
    """
    
    
    
    #~ workflow_actions = None
    #~ """
    #~ A list of action names to be governed by workflows.
    #~ """
      
    
    
    
    disabled_fields = None
    """
    Return a list of field names that should not be editable 
    for the specified `obj` and `request`.
    
    If defined in the Table, this must be a class method that accepts 
    two arguments `obj` and `ar` (an `ActionRequest`)::
    
      @classmethod
      def disabled_fields(cls,obj,ar):
          ...
          return []
          
    
    If not defined in the Table, Lino will look whether 
    the Table's model has a `disabled_fields` method 
    and install a wrapper to this model method. 
    When defined on the model, is must be an *instance* 
    method
    
      def disabled_fields(self,ar):
          ...
          return []
    
    See also :doc:`/tickets/2`.
    """
    
    #~ get_row_permission = None
    #~ """
    #~ Same remarks as for :attr:`disabled_fields`.
    #~ """
    
    #~ disable_editing = None
    #~ """
    #~ Return `True` if the record as a whole should be read-only.
    #~ Same remarks as for :attr:`disabled_fields`.
    #~ """
    
    active_fields = []
    """A list of field names that are "active" (cause a save and 
    refresh of a Detail or Insert form).
    """
    
    hide_window_title = False
    """
    This is set to `True` in home pages
    (e.g. :class:`lino.apps.pcsw.models.Home`).
    """

    #~ has_navigator = True
    hide_top_toolbar = False
    """
    Whether a Detail Window should have navigation buttons, a "New" and a "Delete" buttons.
    In ExtJS UI also influences the title of a Detail Window to specify only 
    the current element without prefixing the Tables's title.
    
    This option is True in 
    :class:`lino.models.SiteConfigs`.
    :class:`lino.apps.pcsw.model.Home`.
    """
    
    known_values = {}
    """
    A `dict` of `fieldname` -> `value` pairs that specify "known values".
    Requests will automatically be filtered to show only existing records 
    with those values.
    This is like :attr:`filter`, but 
    new instances created in this Table will automatically have 
    these values set.
    
    """
    
    parameters = None
    """
    User-definable parameter fields for this table.
    Set this to a `dict` of `name = models.XyzField()` pairs.
    """
    
    params_template = None
    """
    If this table has parameters, specify here how they should be 
    laid out in the parameters panel.
    """
    
    params_panel_hidden = False
    """
    If this table has parameters, set this to False if the parameters 
    panel should be visible when this table is being displayed.
    """
    
    
    
    title = None
    """
    The text to appear e.g. as window title when the actor's 
    default action has been called.
    If this is not set, Lino will use the :attr:`label` as title.
    """
    
    label = None
    """
    The text to appear e.g. on a button that will call 
    the default action of an actor.
    This attribute is *not* inherited to subclasses.
    For :class:`lino.core.table.Table` subclasses
    that don't have a label, 
    Lino will call 
    :meth:`get_actor_label <lino.core.table.Table.get_actor_label>`.
    """
    
    #~ actions = []
    default_action = None
    actor_id = None
    
    detail_layout = None
    detail_template = None
    
    insert_layout = None
    insert_template = None
    
    
    detail_action = None
    insert_action = None
    update_action = None
    create_action = None
    delete_action = None
    
    #~ required_user_level = None
    #~ """
    #~ The minimum :class:`lino.utils.choicelists.UserLevels` 
    #~ required to get permission to view this Actor.
    #~ The default value `None` means that no special UserLevel is required.
    #~ See also :attr:`required_user_groups`
    #~ """
    
    #~ required_user_groups = None
    #~ """
    #~ List of strings naming the user groups for which membership is required 
    #~ to get permission to view this Actor.
    #~ The default value `None` means
    #~ """
    
    @classmethod
    def set_required(self,**kw):
        new = dict()
        new.update(self.required)
        new.update(kw)
        self.required = new
        
    
    
    
    _handle_class = None
    "For internal use"
    
        
    get_handle_name = None
    """
    Most actors use the same UI handle for each request. 
    But debts.PrintEntriesByBudget overrides this to 
    implement dynamic columns depending on it's master_instance.
    """
        
    @classmethod
    def get_request_handle(self,ar):
        # don't override
        if self.get_handle_name is None:
            return self._get_handle(ar,ar.ui,ar.ui._handle_attr_name)
        return self._get_handle(ar,ar.ui,self.get_handle_name(ar))
      
        
    @classmethod
    def get_handle(self,ui):
        #~ assert ar is None or isinstance(ui,UI), \
            #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        if self.get_handle_name is not None:
            raise Exception(
                "Tried to get static handle for %s (get_handle_name is %r)" 
                % (self,self.get_handle_name))
        if ui is None:
            hname = '_lino_console_handler'
        else:
            hname = ui._handle_attr_name
        return self._get_handle(None,ui,hname)
        
    @classmethod
    def _get_handle(self,ar,ui,hname):
        # attention, don't inherit from parent!
        h = self.__dict__.get(hname,None)
        if h is None:
            h = self._handle_class(ui,self)
            setattr(self,hname,h)
            h.setup(ar)
        return h
        
        
    @classmethod
    def do_setup(self):
        pass
    
    
    
    #~ submit_action = actions.SubmitDetail()
    
    @classmethod
    def class_init(cls):
        #~ if cls.__name__ == 'Home':
            #~ print "20120524",cls, "class_init()", cls.__bases__
        #~ for b in cls.__bases__:
        
        for b in cls.mro():
            for k,v in b.__dict__.items():
                if isinstance(v,actions.Action):
                    #~ if not cls.__dict__.has_key(k):
                    #~ if cls.__name__ == 'Home':
                    if cls.__dict__.get(k,None) is None:
                        #~ logger.info("20120628 %s.%s copied from %s",cls,k,b)
                        v = copy.deepcopy(v)
                        v.name = None
                        setattr(cls,k,v)
                        #~ cls.define_action(k,v)
                        #~ if b is EmptyTable:
                            #~ print "20120523", classname, k, v
            #~ bd = getattr(b,'_actions_dict',None)
            #~ if bd:
                #~ for k,v in bd.items():
                    #~ cls._actions_dict[k] = cls.add_action(copy.deepcopy(v),k)
        
    @classmethod
    def get_view_permission(self,user):
        return self.default_action.allow(user,None,None)
        #~ return self.allow_read(user,None,None)

    @classmethod
    def get_row_permission(cls,obj,user,state,action):
        """
        Returns True or False whether the given action 
        is allowed for the given row instance `row` 
        and the user who issued the given ActionRequest `ar`.
        """
        if action.readonly:
            return True
        return cls.editable

    #~ 20120621 @classmethod
    #~ def get_permission(self,user,action):
        #~ return True
        
        
        
    @classmethod
    def _collect_actions(cls):
        """
        Loops through the class dict and collects all Action instances,
        calling `_attach_action` which will set their `actor` attribute.
        Before this we create `insert_action` and `detail_action` if necessary.
        Also fill _actions_list.
        """
        if cls.detail_layout or cls.detail_template:
            cls.detail_action = actions.ShowDetailAction()
        if cls.detail_action and cls.editable:
            cls.insert_action = actions.InsertRow()
            if not cls.hide_top_toolbar:
                cls.create_action = actions.SubmitInsert(sort_index=1)
        if cls.editable:
            cls.update_action = actions.SubmitDetail(sort_index=1)
        if cls.editable and not cls.hide_top_toolbar:
            cls.delete_action = actions.DeleteSelected(sort_index=5)
            
                
        #~ if cls.__name__.startswith('OutboxBy'):
            #~ print '20120524 collect_actions',cls, cls.insert_action, cls.detail_action, cls.editable
        """
        Note that Action instances on base classes have 
        been copied to this Actor's __dict__
        """
        cls._actions_list = []
        for k,v in cls.__dict__.items():
            if isinstance(v,actions.Action):
                cls._attach_action(k,v)
                
        #~ cls._actions_list = cls._actions_dict.values()
        #~ cls._actions_list += cls.get_shared_actions()
        def f(a,b):
            return cmp(a.sort_index,b.sort_index)
        cls._actions_list.sort(f)
        cls._actions_list = tuple(cls._actions_list)
        #~ if cls.__name__ == 'RetrieveTIGroupsRequest':
        #~ logger.info('20120614 %s : %s',cls, [str(a) for a in cls._actions_list])
        
        
    @classmethod
    def _attach_action(self,name,a):
        a.attach_to_actor(self,name)
        if a.url_action_name:
            if self._actions_dict.has_key(a.url_action_name):
                raise Exception(
                    "Duplicate url_action_name %s for %s" % (
                        a.url_action_name,a))
            self._actions_dict[a.url_action_name] = a
        elif a.show_in_workflow:
            raise Exception("Cannot show %s in workflow without url_action_name" % self)
        self._actions_list.append(a)
        return a
            

    @classmethod
    def get_label(self):
        return self.label
        
    @classmethod
    def get_title(self,rr):
        """
        Return the title of this Table for the given request `rr`.
        Override this if your Table's title should mention for example filter conditions.
        """
        return self.title or self.label
        
    @classmethod
    def setup_request(self,req):
        pass
        
        
        
    #~ @classmethod
    #~ def debug_summary(self):
        #~ return "%s (%s)" % (self.__class__,','.join([
            #~ a.name for a in self._actions_list]))
            
    @fields.displayfield(_("Workflows"))
    def workflow_buttons(self,obj,ar):
        """
        Displays the workflow buttons for this row and this user.
        """
        actor = ar.actor
        #~ print 20120621 , actor,  self
        #~ print 20120618, ar
        l = []
        state = actor.get_row_state(obj)
        for a in actor.get_actions(ar.action):
            #~ if a.show_in_workflow and a.get_action_permission(ar.get_user(),obj,state):
            if a.show_in_workflow and obj.get_row_permission(ar.get_user(),state,a):
                l.append(ar.renderer.row_action_button(obj,ar,a))
        return ', '.join(l)
        
    @classmethod
    def get_row_state(self,obj):
        if self.workflow_state_field is not None:
            return getattr(obj,self.workflow_state_field.name)
            #~ if isinstance(state,choicelists.Choice):
                #~ state = state.value
            
            
    @classmethod
    def disabled_actions(self,ar,obj):
        """
        Returns a dictionary containg the names of the actions 
        that are disabled  for the given object instance `obj` 
        and the user who issued the given ActionRequest `ar`.
        """
        d = dict()
        if obj is not None:
            state = self.get_row_state(obj)
            u = ar.get_user()
            for a in self.get_actions(ar.action):
                if a.show_in_bbar and not a.get_action_permission(ar.get_user(),obj,state):
                #~ if not obj.get_row_permission(a,u):
                #~ if not a.get_row_permission(u,obj):
                #~ if not self.get_permission(a,u,obj):
                    d[a.name] = True
        return d
        
            
    @classmethod
    def override_column_headers(self,ar):
        return {}
        
    #~ @classmethod
    #~ def get_detail(self):
        #~ return self.detail_layout

        
    @classmethod
    def set_detail_layout(self,*args,**kw):
        """
        Update the :attr:`detail_layout` 
        of this actor, or create a new layout if there wasn't one before.
        
        The first argument can be either a string or a
        :class:`FormLayout <lino.core.layouts.FormLayout>` instance.
        If it is a string, it will replace the currently defined 'main' panel.
        With the special case that if the current main panel is horizontal 
        (i.e. the layout has tabs) it replaces the 'general' tab.
        """
        return self.set_form_layout('detail_layout',*args,**kw)
        
    @classmethod
    def set_insert_layout(self,*args,**kw):
        """
        Update the :attr:`insert_layout`
        of this actor, or create a new layout if there wasn't one before.
        Otherwise same usage as :meth:`set_detail_layout`.
        """
        return self.set_form_layout('insert_layout',*args,**kw)
        
    @classmethod
    def set_form_layout(self,attname,dtl=None,**kw):
        if dtl is not None:
            if isinstance(dtl,basestring):
                if getattr(self,attname) is None:
                    setattr(self,attname,layouts.FormLayout(self,dtl,**kw))
                    return
                if '\n' in dtl and not '\n' in getattr(self,attname).main:
                    name = 'general'
                else:
                    name = 'main'
                if kw.has_key(name):
                    raise Exception("set_detail() got two definitions for %r." % name)
                kw[name] = dtl
            else:
                assert isintance(dtl,layouts.FormLayout)
                assert dtl._table is None
                dtl._table = self
                setattr(self,attname,dtl)
        if kw:
            getattr(self,attname).update(**kw)
                
    @classmethod
    def add_detail_panel(self,*args,**kw):
        """
        Adds a panel to the Detail of this actor.
        """
        self.detail_layout.add_panel(*args,**kw)
    
    @classmethod
    def add_detail_tab(self,*args,**kw):
        """
        Adds a tab panel to the Detail of this actor.
        """
        self.detail_layout.add_tabpanel(*args,**kw)
    
        

    @classmethod
    def add_virtual_field(cls,name,vf):
        cls.virtual_fields[name] = vf
        vf.name = name
        vf.get = curry(vf.get,cls)
        
    @classmethod
    def add_constant(cls,name,vf):
        cls._constants[name] = vf
        vf.name = name
        
    #~ @classmethod
    #~ def get_url(self,ui,**kw):
        #~ return ui.action_url_http(self,self.default_action,**kw)

    #~ @classmethod
    #~ def setup_permissions(self):
        #~ pass
        
    @classmethod
    def after_site_setup(self):
        #~ raise "20100616"
        #~ assert not self._setup_done, "%s.setup() called again" % self
        if self._setup_done:
            return True
        if self._setup_doing:
            if True: # severe error handling
                raise Exception("%s.setup() called recursively" % self)
            else:
                logger.warning("%s.setup() called recursively" % self)
                return False
        #~ logger.debug("Actor.setup() %s", self)
        self._setup_doing = True
        
        #~ if self.label is None:
            #~ self.label = self.__name__
        #~ if self.title is None:
            #~ self.title = self.label
            
        self._collect_actions()
            
        if self.parameters:
            from lino.utils.choosers import check_for_chooser
            for k,v in self.parameters.items():
                if isinstance(v,models.ForeignKey):
                    v.rel.to = resolve_model(v.rel.to)
                check_for_chooser(self,v)
        
        self.do_setup()
        #~ self.setup_permissions()
        self._setup_doing = False
        self._setup_done = True
        #~ logger.debug("20120103 Actor.setup() done: %s, default_action is %s", 
            #~ self.actor_id,self.default_action)
        return True
        
        
    @classmethod
    def get_url_action(self,name):
        return self._actions_dict.get(name,None)
        
    @classmethod
    def get_actions(self,callable_from=None):
        if self._actions_list is None:
            raise Exception("Tried to %s.get_actions() with empty _actions_list" % self)
        if callable_from is None:
            return self._actions_list
        return [a for a in self._actions_list 
          if a.callable_from is None or isinstance(callable_from,a.callable_from)]
    
    @classmethod
    def get_param_elem(self,name):
        if self.parameters:
            return self.parameters.get(name,None)
        #~ for pf in self.params:
            #~ if pf.name == name:  return pf
        return None
      
    @classmethod
    def get_data_elem(self,name):
        c = self._constants.get(name,None)
        if c is not None:
            return c
        #~ return self.virtual_fields.get(name,None)
        vf = self.virtual_fields.get(name,None)
        if vf is not None:
            #~ logger.info("20120202 Actor.get_data_elem found vf %r",vf)
            return vf
            
        a = getattr(self,name,None)
        if isinstance(a,actions.Action):
            return a
        
        #~ logger.info("20120307 lino.core.coretools.get_data_elem %r,%r",self,name)
        s = name.split('.')
        if len(s) == 1:
            #~ app_label = model._meta.app_label
            rpt = settings.LINO.modules[self.app_label].get(name,None)
        elif len(s) == 2:
            rpt = settings.LINO.modules[s[0]].get(s[1],None)
        else:
            raise Exception("Invalid data element name %r" % name)
        if rpt is not None: 
            #~ if rpt.master is not None and rpt.master is not ContentType:
                #~ ok = True
                #~ try:
                    #~ if not issubclass(model,rpt.master):
                        #~ ok = False
                #~ except TypeError,e: # e.g. issubclass() arg 1 must be a class
                    #~ ok = False
                #~ if not ok:
                    #~ raise Exception("%s.master is %r, must be subclass of %r" % (
                        #~ name,rpt.master,model))
            return rpt
        #~ logger.info("20120202 Actor.get_data_elem found nothing")
        return None
              
    @classmethod
    def request(self,ui=None,request=None,action=None,**kw):
        #~ self = cls
        #~ if action is None:
            #~ action = self.default_action
        return actions.ActionRequest(ui,self,request,action,**kw)

        

