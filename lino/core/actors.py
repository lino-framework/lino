# -*- coding: UTF-8 -*-
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
This defines the 
:class:`Actor` 
and
:class:`BoundAction` 
classes.

"""

import logging
logger = logging.getLogger(__name__)

import copy

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import lino
#~ from lino.ui import base

#~ from lino.ui.base import Handled
from lino.core import fields
from lino.core import actions
from lino.core import layouts
#~ from lino.core import changes
from lino.core.dbutils import resolve_model
from lino.core.requests import ActionRequest
from lino.core.constants import _handle_attr_name
from lino.utils import curry, AttrDict
#~ from lino.core import perms
from lino.utils import jsgen
from lino.utils import uncamel
from lino.utils import join_elems
#~ from lino.utils import class_dict_items
from lino.utils.xmlgen.html import E


actor_classes = []
actors_list = None

ACTOR_SEP = '.'

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
          

def register_actor(a):
    #~ logger.debug("register_actor %s",a)
    if not settings.SITE.is_installed(a.app_label):
        # happens when sphinx autodoc imports a non installed module
        return
    old = settings.SITE.modules.define(a.app_label,a.__name__,a)
    #~ old = actors_dict.get(a.actor_id,None)
    if old is not None:
        #~ logger.info("20121023 register_actor %s : %r replaced by %r",a,old,a)
        actors_list.remove(old)
        #~ old._replaced_by = a
    #~ actors_dict[a.actor_id] = a
    actors_list.append(a)
    return a


def get_default_required(**kw):
    #~ if not kw.has_key('auth'):
        #~ kw.update(auth=True)
    if settings.SITE.user_model is not None:
        kw.setdefault('auth',True)
    return kw
    


class ParameterPanel(object):
    def __init__(self,**kw):
        self.fields = kw
        #~ object.__init__(self,**kw)
        #~ for n in ('__getitem__','get','items','keys','values','__iter__','__len__'):
            #~ setattr(self,n,getattr(kw,n))
        
    def values(self,*args,**kw): return self.fields.values(*args,**kw)
    def keys(self,*args,**kw): return self.fields.keys(*args,**kw)
    def __iter__(self,*args,**kw): return self.fields.__iter__(*args,**kw)
    def __len__(self,*args,**kw): return self.fields.__len__(*args,**kw)
    def __getitem__(self,*args,**kw): return self.fields.__getitem__(*args,**kw)
    def get(self,*args,**kw):   return self.fields.get(*args,**kw)
    def items(self,*args,**kw):   return self.fields.items(*args,**kw)
        
class ObservedPeriod(ParameterPanel):
    def __init__(self,**kw):
        kw.update(
            start_date = models.DateField(_("Period from"),
                blank=True,null=True,
                help_text="""Start date of observed period"""),
            end_date = models.DateField(_("until"),
                blank=True,null=True,
                help_text="""End date of observed period"""),
            )
        super(ObservedPeriod,self).__init__(**kw)


    
    
class BoundAction(object):
    """
    An Action which is bound to an Actor.
    If an Actor has subclasses, each subclass "inherits" its actions.
    """
  
    def __init__(self,actor,action):

        if not isinstance(action,actions.Action):
            raise Exception("%s : %r is not an Action" % (actor,action))
        self.action = action
        self.actor = actor
        
        required = dict()
        if action.readonly:
            required.update(actor.required)
        #~ elif isinstance(action,InsertRow):
            #~ required.update(actor.create_required)
        elif isinstance(action,actions.DeleteSelected):
            required.update(actor.delete_required)
        else:
            required.update(actor.update_required)
        required.update(action.required)
        #~ print 20120628, str(a), required
        #~ def wrap(a,required,fn):
            #~ return fn
            
        debug_permissions = actor.debug_permissions and action.debug_permissions
        
        if debug_permissions:
            if settings.DEBUG:
                logger.info("debug_permissions for %r (required=%s)",self,required)
            else:
                raise Exception("debug_permissions for %r (required=%s)",self,required)
            
        from lino.core.auth import make_permission_handler, make_view_permission_handler
        self.allow_view = curry(make_view_permission_handler(
            self,action.readonly,debug_permissions,**required),action)
        self._allow = curry(make_permission_handler(
            action,actor,action.readonly,debug_permissions,**required),action)
        #~ if debug_permissions:
            #~ logger.info("20130424 _allow is %s",self._allow)
        #~ actor.actions.define(a.action_name,ba)
        
        
    def get_window_layout(self):
        return self.action.get_window_layout(self.actor)
        
    def get_window_size(self):
        return self.action.get_window_size(self.actor)
        
    def full_name(self):
        return self.action.full_name(self.actor)
        #~ if self.action.action_name is None:
            #~ raise Exception("%r action_name is None" % self.action)
        #~ return str(self.actor) + '.' + self.action.action_name
        
    def request(self,*args,**kw):
        kw.update(action=self)
        return self.actor.request(*args,**kw)
        
        
    def get_button_label(self,*args):
        return self.action.get_button_label(self.actor,*args)
        
    #~ def get_panel_btn_handler(self,*args):
        #~ return self.action.get_panel_btn_handler(self.actor,*args)
        
    def setup_action_request(self,*args):
        return self.action.setup_action_request(self.actor,*args)
        
    def get_row_permission(self,ar,obj,state):
        #~ if self.actor is None: return False
        return self.actor.get_row_permission(obj,ar,state,self)
        
    def get_bound_action_permission(self,ar,obj,state):
        if not self.action.get_action_permission(ar,obj,state):
            #~ if self.action.action_name == 'wf7':
                #~ logger.info("20130424 actors.BoundAction.get_bound_action_permission")
            return False
        return self._allow(ar.get_user(),obj,state)
        
    def get_view_permission(self,profile):
        """
        20130511
        """
        #~ if self.action.__class__.__name__ == 'ShowSlaveTable':
            #~ logger.info("20130820 BoundAction.get_view_permission()")
            #~ raise Exception(20130820)
        if not self.actor.get_view_permission(profile):
            return False
        if not self.action.get_view_permission(profile):
            return False
        return self.allow_view(profile)
        
    def __repr__(self):
        return "<%s(%s,%r)>" % (self.__class__.__name__,self.actor,self.action)
    
        
#~ class ClassProperty(property):
    #~ def __get__(self, cls, owner):
        #~ return self.fget.__get__(None, owner)()
#~ 


def field_getter(name):
    def func(cls,obj,ar):
        #~ print 20130910, repr(obj),name
        return getattr(obj,name)
    return func

class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
            
        
        """
        attributes that are never inherited from base classes:
        """
        # classDict.setdefault('name',classname)
        #~ classDict.setdefault('label',None) # 20130906
        #~ classDict.setdefault('related_name',None)
        #~ classDict.setdefault('button_label',None)
        classDict.setdefault('title',None)
        classDict.setdefault('help_text',None)
        classDict.setdefault('abstract',False)
        
        declared_label = classDict.pop('label',None)
        if declared_label is not None:
            classDict.update(_label=declared_label)
        declared_known_values = classDict.pop('known_values',None)
        if declared_known_values is not None:
            classDict.update(_known_values=declared_known_values)
        declared_editable = classDict.pop('editable',None)
        if declared_editable is not None:
            classDict.update(_editable=declared_editable)
        
        cls = type.__new__(meta, classname, bases, classDict)
        
        
        #~ if not classDict.has_key('label'):
            #~ cls.label = ClassProperty(cls.get_actor_label)
            #~ meta.label = property(cls.get_actor_label.im_func) # 20130906
        #~ if not classDict.has_key('known_values'):
            #~ cls.known_values = ClassProperty(cls.get_known_values)
            #~ meta.known_values = property(cls.get_known_values.im_func) # 20130906
        
        #~ if cls.is_abstract():
            #~ actions.register_params(cls)
        
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
            x = cls.__module__.split('.')
            if len(x) > 1:
                cls.app_label = x[-2]
        
        cls.actor_id = cls.app_label + '.' + cls.__name__
        cls._setup_done = False
        cls._setup_doing = False
                
        cls.virtual_fields = {}
        cls._constants = {}
        cls._actions_dict = AttrDict()
        #~ cls._actions_list = None # 20121129
        cls._actions_list = [] # 20121129
        #~ cls._replaced_by = None
        
        # inherit virtual fields defined on parent Actors
        for b in bases:
            bd = getattr(b,'virtual_fields',None)
            if bd:
                cls.virtual_fields.update(bd)
                
        if True: # (20130817) tried to move this to a later moment
            for k,v in classDict.items():
                cls.register_class_attribute(k,v)
                    
        #~ if classname == 'Tasks':
            #~ logger.info("20130817 no longer added actor vfs")
                
                
        #~ cls.params = []
        #~ for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
                #~ v.set_attributes_from_name(k)
                #~ v.table = cls
                #~ cls.params.append(v)
                
        
                
        #~ cls.install_params_on_actor()
        
        
        
                
        if classname not in (
            'Table','AbstractTable','VirtualTable',
            'Action','Actor','Frame',
            'ChoiceList','Workflow',
            'EmptyTable','Dialog'):
            if actor_classes is None:
                #~ logger.debug("%s definition was after discover",cls)
                pass
            elif not cls.__name__.startswith('unused_'):
                #~ logger.debug("Found actor %s.",cls)
                #~ cls.class_init() # 20120115
                actor_classes.append(cls)
            #~ logger.debug("ActorMetaClass.__new__(%s)", cls)
        return cls

    def __str__(cls):
        return cls.actor_id
  
    @property
    def label(cls):
        return cls.get_actor_label()
        
    @property
    def known_values(cls):
        return cls.get_known_values()
        
    @property
    def editable(cls):
        return cls.get_actor_editable()
        


class Actor(actions.Parametrizable):
    """
    Base class for 
    :class:`AbstractTable <lino.core.tables.AbstractTable>`, 
    :class:`ChoiceList <lino.core.choicelists.ChoiceList>` 
    and :class:`Frame <lino.core.frames.Frame>`.
    
    See :doc:`/dev/actors`.
    """
    
    __metaclass__ = ActorMetaClass
    
    _layout_class = layouts.ParamsLayout
    
    #~ @property
    #~ def known_values(cls):
        #~ return cls.get_known_values()
    
    
    
    sort_index = None 
    """
    The sort_index to be used for a ShowSlaveTable action on this actor.
    """
    
    icon_name = None 
    """
    The icon_name to be used for a ShowSlaveTable action on this actor.
    """
    
    #~ icon_file = None
    #~ """
    #~ The icon_file to be used for a ShowSlaveTable action on this actor.
    #~ """
    #~ 
    
    
    hidden_elements = frozenset()
    
    @classmethod
    def apply_cell_format(self,ar,row,col,recno,td):
        """
        Actor-level hook for overriding the formating when rendering 
        this table as plain html.
        
        For example :class:`lino.modlib.cal.models.Events`
        overrides this.
        """
        pass
        
    
    @classmethod
    def register_class_attribute(cls,k,v):
        if isinstance(v,fields.Constant):
            cls.add_constant(k,v)
        elif isinstance(v,fields.VirtualField): # 20120903b
            cls.add_virtual_field(k,v)
        elif isinstance(v,models.Field): # 20130910
            #~ print "20130910 add virtual field " ,k, cls
            vf = fields.VirtualField(v,field_getter(k))
            cls.add_virtual_field(k,vf)
    
    @classmethod
    def inject_field(cls,name,fld):
        # called from auth.add_user_group()
        setattr(cls,name,fld)
        cls.register_class_attribute(name,fld)
        
        
    get_welcome_messages = None
    """
    If not None, this must be a class method which takes an ActionRequest 
    and returns or yields a list of messages to displayed in the welcome 
    screen.
    """
    
    get_row_classes = None
    """
    If not None, this must be a class method which takes a table row
    and an ActionRequest and returns either None or a string 
    "red", "green" or "blue" (todo: add more colors 
    and styles). Example::
    
        @classmethod
        def get_row_classes(cls,obj,ar):
            if obj.client_state == pcsw.ClientStates.newcomer:
                return 'green'
    
    It will cause an additional special field RowClassStoreField
    
    """
    
    app_label = None
    """
    Specify this if you want to "override" an existing actor.
    
    The default value is deduced from the module where the 
    subclass is defined.
    
    Note that this attribute is not inherited from base classes.
    
    :func:`lino.core.table.table_factory` also uses this.
    """
    
    #~ related_name = None
    #~ """
    
    #~ """
    
    window_size = None
    """
    Set this to a tuple of (height, width) in pixels to have 
    this actor display in a modal non-maximized window.
    """
    
    default_list_action_name = 'grid'
    default_elem_action_name =  'detail'
    
    
    debug_permissions = False
    """
    When this is `True`, Lino logs an ``info`` message each time a permission handler 
    for an action on this actor is called. 
    Not to be used on a production site but useful for debugging.
    """
    
    #~ required = dict()
    required = get_default_required()
    
    #~ required = dict(auth=True) # 20121116
    
    #~ create_required = dict()
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
    Otherwise it will be set to `False` if the Actor 
    is a Table and has a `get_data_rows` method.
    
    Note that this attribute is not inherited to subclasses.
    (TODO: explain why... because at least for 
    `lino_faggio.models.InvoicingsByEnrolment` it is disturbing 
    to not inherit it.    
    Has to do with :class:`DistByBudget <lino_welfare.modellib.debts.models.DistByBudget>` 
    which defines its own `get_data_rows` but inherits from 
    :class:`EntriesByBudget
    <lino_welfare.modellib.debts.models.EntriesByBudget>` 
    which has no `get_data_rows`.)
    
    
    The :class:`lino.models.Changes` table is an example where this is being used: 
    nobody should ever edit something in the table of Changes. 
    The user interface uses this to generate optimized JS code for this case.
    """
    
    hide_sums = False
    """
    Set this to True if you don't want Lino to display sums in a table view.
    """
    
    insert_layout_width = 60
    """
    When specifying an :attr:`insert_layout` using a simple a multline 
    string, then Lino will instantiate a FormPanel with this width.
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
    
    
    @classmethod
    def get_pk_field(self):
        """Return the Django field object used to represent the primary key 
        when filling selected_pks
        """
        return None
        
    @classmethod
    def get_row_by_pk(self,pk):
        """
        REturn the data row identified by the given primary key.
        """
        return None
        
    
    
    
    #~ @classmethod
    #~ def get_default_table(cls):
        #~ "For InstanceAction "
        #~ return cls
        
    @classmethod
    def disabled_fields(cls,obj,ar):
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
        return []
    
    
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
    (e.g. :class:`lino_welfare.modlib.pcsw.models.Home`).
    """
    
    allow_create = True
    """
    If this is False, then then Actor won't have neither create_action nor insert_action.
    """

    hide_top_toolbar = False
    """
    Whether a Detail Window should have navigation buttons, 
    a "New" and a "Delete" buttons.
    In ExtJS UI also influences the title of a Detail Window to specify only 
    the current element without prefixing the Tables's title.
    
    This option is True in 
    :class:`lino.models.SiteConfigs`,
    :class:`lino_welfare.pcsw.models.Home`,
    :class:`lino.modlib.users.models.Mysettings`.
    """
    
    _label = None
    _editable = None
    _known_values = {}
    """
    A `dict` of `fieldname` -> `value` pairs that specify "known values".
    Requests will automatically be filtered to show only existing records 
    with those values.
    This is like :attr:`filter`, but 
    new instances created in this Table will automatically have 
    these values set.
    
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
    """
    Define the form layout to use for the detail window.
    Actors without `detail_layout` don't have a show_detail action.
    """
    
    insert_layout = None
    """
    Define the form layout to use for the insert window.
    If there's a detail_layout but no insert_layout, 
    Lino will use detail_layout for the insert window.
    """
    
    detail_template = None # deprecated: use detail_layout with a string value instead
    insert_template = None # deprecated: use insert_layout with a string value instead
    
    help_text = None
    
    detail_action = None
    update_action = None
    insert_action = None
    create_action = None
    delete_action = None
    
    
    _handle_class = None
    "For internal use"
    
        
    get_handle_name = None
    """
    Most actors use the same UI handle for each request. 
    But e.g. debts.PrintEntriesByBudget overrides this to 
    implement dynamic columns depending on it's master_instance.
    """
        
    @classmethod
    def get_request_handle(self,ar):
        # don't override
        if self.get_handle_name is None:
            return self._get_handle(ar,_handle_attr_name)
        return self._get_handle(ar,self.get_handle_name(ar))
        
    @classmethod
    def is_valid_row(self,row):
        return False
        
    @classmethod
    def make_params_layout_handle(self,ui):
        return actions.make_params_layout_handle(self,ui)
        
    abstract = False
    """
    Set this to True to prevent Lino from generating useless JavaScript 
    if this is just an abstract base class to be inherited by other actors.
    """
    
    @classmethod
    def is_abstract(cls):
        return cls.abstract
        
            
    @classmethod
    def has_handle(self,ui):
        #~ if ui is None:
            #~ hname = '_lino_console_handler'
        #~ else:
            #~ hname = _handle_attr_name
        #~ return self.__dict__.get(hname,False)
        return self.__dict__.get(_handle_attr_name,False)
        
    @classmethod
    def clear_handle(self):
        """
        When an actor has dynamic columns which depend on database 
        content, then its layout handle may not persist between 
        different Django test cases because a handle from a first
        test case may refer to elements which no longer exist in a 
        second test case.
        """
        setattr(self,_handle_attr_name,None)
        
    @classmethod
    def on_analyze(self,site):
        pass
        
    @classmethod
    def summary_row(cls,ar,obj,**kw): return obj.summary_row(ar,**kw)
    
    @classmethod
    def get_handle(self):
        #~ assert ar is None or isinstance(ui,UI), \
            #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        if self.get_handle_name is not None:
            raise Exception(
                "Tried to get static handle for %s (get_handle_name is %r)" 
                % (self,self.get_handle_name))
        #~ if ui is None:
            #~ hname = '_lino_console_handler'
        #~ else:
            #~ hname = _handle_attr_name
        return self._get_handle(None,_handle_attr_name)
        
    @classmethod
    def _get_handle(self,ar,hname):
        # don't inherit from parent!
        h = self.__dict__.get(hname,None)
        if h is None:
            #~ if self._replaced_by is not None:
                #~ raise Exception("Trying to get handle for %s which is replaced by %s" % (self,self._replaced_by))
            h = self._handle_class(self)
            setattr(self,hname,h)
            h.setup(ar)
        return h
        
        
    @classmethod
    def do_setup(cls):
        if False: # see :blogref:`20130327`
            if cls.master is not None:
                if not isinstance(cls.master,type):
                    raise Exception("%s.master is %r" % (cls,cls.master))
                if not issubclass(cls.master,models.Model):
                    raise Exception("%s.master is %r" % (cls,cls.master))
                name = cls.related_name or uncamel(cls.__name__)
                if cls.app_label == cls.master._meta.app_label:
                    if hasattr(cls.master,name):
                        logger.debug("Name %s.%s already defined",cls.master,name)
                    else:
                        #~ def m(obj,ar):
                            #~ return ar.spawn(cls,master_instance=obj,title=cls.label)
                        def m(obj):
                            return cls.request(master_instance=obj,title=cls.label)
                        setattr(cls.master,name,m)
                        
    
    
    #~ submit_action = actions.SubmitDetail()
    
    _class_init_done = False
    
    @classmethod
    def class_init(cls):
        """
        Called internally a site startup. Don't override.
        """
        #~ if str(cls) == 'contacts.Persons':
            #~ logger.info("20130804 Actor.class_init() %r",cls)
        #~ if cls.__name__ == 'Home':
            #~ print "20120524",cls, "class_init()", cls.__bases__
        #~ 20121008 cls.default_action = cls.get_default_action()
        
        #~ classDict = cls.__dict__
        
        #~ dt = classDict.get('detail_template',None)
        #~ dt = getattr(cls,'detail_template',None)
        #~ if dt is not None:
            #~ raise Exception("Please rename detail_template to detail_layout")
            #~ if dl is not None:
                #~ raise Exception("%r has both detail_template and detail_layout" % cls)
            #~ dl = dt
            
        #~ if cls.is_abstract() : return
        
        if False: # (20130817) tried to move this from an earlier moment
            for k,v in class_dict_items(cls):
            #~ for k,v in cls.__dict__.items():
                if isinstance(v,fields.Constant):
                    cls.add_constant(k,v)
                if isinstance(v,fields.VirtualField): # 20120903b
                    cls.add_virtual_field(k,v)

        #~ if str(cls) == 'cal.Tasks':
            #~ logger.info("20130817 gonna add actor vfs")


        master = getattr(cls,'master',None)
        if master is not None:
            cls.master = resolve_model(master)
                
        #~ dl = getattr(cls,'detail_layout',None) 
        dl = cls.__dict__.get('detail_layout',None) # see 20130804
        if dl is None and not cls._class_init_done:
            dl = cls.detail_layout
        if dl is not None:
            if isinstance(dl,basestring):
                cls.detail_layout = layouts.FormLayout(dl,cls)
            elif dl._datasource is None:
                dl.set_datasource(cls)
                cls.detail_layout = dl
            elif not issubclass(cls,dl._datasource):
                raise Exception("Cannot use detail_layout of %r for %r" % (dl._datasource,cls))
            
        #~ dl = getattr(cls,'insert_layout',None)
        dl = cls.__dict__.get('insert_layout',None)
        if dl is None and not cls._class_init_done:
            dl = cls.insert_layout
        if dl is not None:
            if isinstance(dl,basestring):
                cls.insert_layout = layouts.FormLayout(dl,cls,
                    window_size=(cls.insert_layout_width,'auto'))
            elif dl._datasource is None:
                dl.set_datasource(cls)
                cls.insert_layout = dl
            elif not issubclass(cls,dl._datasource):
                raise Exception("Cannot reuse %r insert_layout for %r" % (dl._datasource,cls))
                #~ logger.debug("Note: %s uses layout owned by %s",cls,dl._datasource)
                
        # 20130906
        #~ if cls.label is None: 
            #~ cls.label = cls.get_actor_label()
            
        #~ if cls.parameters is not None:
            #~ for name,f in cls.parameters.items():
                #~ if isinstance(f,models.ForeignKey):
                    #~ if f.verbose_name is None:
                        #~ f.rel.to = resolve_model(f.rel.to)
                        #~ f.verbose_name = f.rel.to._meta.verbose_name
          
          
                
        if False:
            #~ for b in cls.__bases__:
            for b in cls.mro():
                for k,v in b.__dict__.items():
                    if isinstance(v,actions.Action):
                      if v.parameters is not None:
                        #~ if not cls.__dict__.has_key(k):
                        #~ if cls.__name__ == 'Home':
                        if cls.__dict__.get(k,None) is None:
                            #~ logger.info("20120628 %s.%s copied from %s",cls,k,b)
                            #~ label = v.label
                            #~ 20130121 : removed two following lines 
                            #~ v = copy.deepcopy(v)
                            #~ v.name = None
                            setattr(cls,k,v)
                            #~ cls.define_action(k,v)
                            #~ if b is EmptyTable:
                                #~ print "20120523", classname, k, v
                #~ bd = getattr(b,'_actions_dict',None)
                #~ if bd:
                    #~ for k,v in bd.items():
                        #~ cls._actions_dict[k] = cls.add_action(copy.deepcopy(v),k)
                        
        _class_init_done = True
                        
    @classmethod
    def get_known_values(self):
        return self._known_values
        
    @classmethod
    def get_actor_label(self):
        """
        Compute the label of this actor. 
        """
        return self._label or self.__name__
                        
    @classmethod
    def get_actor_editable(self):
        return self._editable
                        
    @classmethod
    def hide_elements(self,*names):
        for name in names:
            if self.get_data_elem(name) is None:
                raise Exception("%s has no element '%s'" % self,name)
        self.hidden_elements = self.hidden_elements | set(names)
            
        
    @classmethod
    def add_view_requirements(cls,**kw):
        return actions.add_requirements(cls,**kw)
        
    
    @classmethod
    def get_view_permission(self,profile):
        #~ return self.default_action.action.allow(user,None,None)
        #~ return self.default_action.get_bound_action_permission(user,None,None)
        #~ 20130511 return self.default_action.get_view_permission(profile)
        #~ return self.allow_read(user,None,None)
        return True # 20130511 

    @classmethod
    def get_create_permission(self,ar):
        """
        Dynamic test per request. 
        This is being called only when `allow_create` is True.
        """
        return True

    @classmethod
    def get_row_permission(cls,obj,ar,state,ba):
        """
        Returns True or False whether the given action 
        is allowed for the given row instance `row` 
        and the user who issued the given ActionRequest `ar`.
        """
        if ba.action.readonly:
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
        #~ cls._actions_list = [] # 20121129
        
        #~ default_action = getattr(cls,cls.get_default_action())
        default_action = cls.get_default_action()
        cls.default_action = cls.bind_action(default_action)
        #~ print 20121010, cls, default_action
        #~ if default_action.help_text is None:
            #~ default_action.help_text = cls.help_text
            
        if cls.detail_layout or cls.detail_template:
            if default_action and isinstance(default_action,actions.ShowDetailAction):
                cls.detail_action = cls.bind_action(default_action)
            else:
                cls.detail_action = cls.bind_action(actions.ShowDetailAction())
        if cls.editable:
            if cls.allow_create:
                cls.create_action = cls.bind_action(actions.SubmitInsert())
                if cls.detail_action and not cls.hide_top_toolbar:
                    cls.insert_action = cls.bind_action(actions.InsertRow())
                    cls.create_edit_action = cls.bind_action(actions.SubmitInsertAndStay())
            cls.update_action = cls.bind_action(actions.SubmitDetail(sort_index=1))
            if not cls.hide_top_toolbar:
                cls.delete_action = cls.bind_action(actions.DeleteSelected())


        if isinstance(cls.workflow_owner_field,basestring):
            cls.workflow_owner_field = cls.get_data_elem(cls.workflow_owner_field)

        #~ if isinstance(cls.workflow_state_field,basestring):
            #~ fld = cls.get_data_elem(cls.workflow_state_field)
            #~ if fld is not None: # e.g. cal.Component
                #~ cls.workflow_state_field = fld
                #~ for name,a in cls.get_state_actions():
                    #~ print 20120709, cls,name,a
                    #~ setattr(cls,name,a)

        if isinstance(cls.workflow_state_field,basestring):
            cls.workflow_state_field = cls.get_data_elem(cls.workflow_state_field)
            #~ note that fld may be none e.g. cal.Component
        if cls.workflow_state_field is not None:
            #~ for name,a in cls.get_state_actions():
            for a in cls.workflow_state_field.choicelist.workflow_actions:
            #~ for a in cls.workflow_state_field.choicelist._actions_list: # 20130531 
                #~ print 20120709, cls,name,a
                #~ setattr(cls,name,fn())
                setattr(cls,a.action_name,a) 

        # bind all my actions, including those inherited from parent actors:
        for b in cls.mro():
            for k,v in b.__dict__.items():
                v = cls.__dict__.get(k,v) # 20130820 disable inherited actions
                if isinstance(v,actions.Action):
                    if not cls._actions_dict.has_key(k):
                        #~ cls._attach_action(k,v)
                        if v.attach_to_actor(cls,k):
                            cls.bind_action(v)
        
                        
                    
        #~ cls._actions_list = cls._actions_dict.values()
        #~ cls._actions_list += cls.get_shared_actions()
        def f(a,b):
            return cmp(a.action.sort_index,b.action.sort_index)
        cls._actions_list.sort(f)
        cls._actions_list = tuple(cls._actions_list)
        #~ if cls.__name__ == 'RetrieveTIGroupsRequest':
        #~ logger.info('20120614 %s : %s',cls, [str(a) for a in cls._actions_list])
        
        
    @classmethod
    def bind_action(self,a):
        #~ if a.action_name in self._actions_dict:
            #~ raise Exception("20130424 Attempt to re-bind %r to %r" % (a,self))
            #~ logger.warning("20130424 re-binding %r to %r",a,self)
        ba = BoundAction(self,a)
        if a.action_name is not None:
            self._actions_dict.define(a.action_name,ba)
        self._actions_list.append(ba)
        return ba
        
    #~ @classmethod
    #~ def unbind_action(self,k):
        #~ self._actions_dict.pop(k,None)
        #~ self._actions_list = [ba for ba in self._actions_list if ba.action.action_name != k]
        #~ logger.info("20130820 unbind_action %s",self._actions_list)

    #~ @classmethod
    #~ def get_row_actions(self,ar,obj):
        #~ state = self.get_row_state(obj)
        #~ profile = ar.get_user().profile
        #~ for ba in self.get_actions(ar.bound_action.action):
            #~ if ba.action.show_in_row_actions:
                    #~ if ba.get_view_permission(profile):
                        #~ if self.get_row_permission(obj,ar,state,ba):
                            #~ yield ba
                
    @classmethod
    def get_workflow_actions(self,ar,obj):
        """
        Return the actions to be displayed in a `workflow_buttons` field.
        """
        state = self.get_row_state(obj)
        #~ logger.info("20130424 get_workflow_actions() for %s (state is %s)",
            #~ obj,state)
        #~ u = ar.get_user()
        
        #~ for ba in self.get_actions(ar.bound_action.action):
        for ba in self.get_actions():
            if ba.action.show_in_workflow:
                #~ if obj.get_row_permission(ar,state,ba):
                if self.get_row_permission(obj,ar,state,ba):
                    yield ba
                #~ else:
                    #~ logger.info('20130424 [%s] is not allowed for %s',ba,ar.get_user())
            #~ else:
                #~ logger.info('20130424 [%s] has not show_in_workflow', ba)
        
    @classmethod
    def get_label(self):
        return self.label
        
    @classmethod
    def get_title(self,ar):
        """
        Return the title of this Table for the given request `ar`.
        Override this if your Table's title should mention for example filter conditions.
        """
        # NOTE: similar code in dbtables
        title = self.title or self.label
        tags = list(self.get_title_tags(ar))
        if len(tags):
            title += " (%s)" % (', '.join(tags))
        return title
        
        
        
        
    @classmethod
    def get_title_tags(self,ar):
        return []
        
    @classmethod
    def setup_request(self,req):
        pass
        
        
    @classmethod
    def get_param_elem(self,name):
        # same as in Action, but here it is a class method
        if self.parameters:
            return self.parameters.get(name,None)
        return None
        
            
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
        
        Application developers should not need to override this method.
        
        Default implementation returns an empty dictionary.
        Overridden by :class:`lino.core.dbtables.Table`
        """
        return {}
        
            
    @classmethod
    def override_column_headers(self,ar):
        return {}
        
    @classmethod
    def get_sum_text(self,ar):
        """
        Return the text to display on the totals row.
        """
        return unicode(_("Total (%d rows)") % ar.get_total_count())
        
        
    #~ @classmethod
    #~ def get_detail(self):
        #~ return self.detail_layout

        
    @classmethod
    def set_detail_layout(self,*args,**kw):
        """
        Update the :attr:`detail_layout` of this actor, 
        or create a new layout if there wasn't one before.
        
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
        Update the :attr:`insert_layout` of this actor, 
        or create a new layout if there wasn't one before.
        Otherwise same usage as :meth:`set_detail_layout`.
        """
        return self.set_form_layout('insert_layout',*args,**kw)
        
    @classmethod
    def set_form_layout(self,attname,dtl=None,**kw):
        if dtl is not None:
            existing = getattr(self,attname) # 20120914c
            if isinstance(dtl,basestring):
                if existing is None:
                    setattr(self,attname,layouts.FormLayout(dtl,self,**kw))
                    return
                if '\n' in dtl and not '\n' in existing.main:
                    name = 'general'
                else:
                    name = 'main'
                if kw.has_key(name):
                    raise Exception("set_detail() got two definitions for %r." % name)
                kw[name] = dtl
            else:
                assert isinstance(dtl,layouts.FormLayout)
                assert dtl._datasource is None
                if existing is not None: # added for 20120914c but it wasn't the problem
                    if not isinstance(dtl,existing.__class__):
                        raise NotImplementedError(
                            "Cannot replace existing %s %r by %r" % (attname,existing,dtl))
                    if existing._added_panels:
                        if '\n' in dtl.main:
                            raise NotImplementedError(
                                "Cannot replace existing %s with added panels %s" %(existing,existing._added_panels))
                        dtl.main += ' ' + (' '.join(existing._added_panels.keys()))
                        #~ logger.info('20120914 %s',dtl.main)
                        dtl._added_panels.update(existing._added_panels)
                    dtl._element_options.update(existing._element_options)
                dtl._datasource = self
                setattr(self,attname,dtl)
        if kw:
            getattr(self,attname).update(**kw)
                
    @classmethod
    def add_detail_panel(self,*args,**kw):
        """
        Adds a panel to the Detail of this actor.
        Arguments: see :meth:`lino.core.layouts.BaseLayout.add_panel`
        """
        self.detail_layout.add_panel(*args,**kw)
    
    @classmethod
    def add_detail_tab(self,*args,**kw):
        """
        Adds a tab panel to the Detail of this actor.
        See :meth:`lino.core.layouts.BaseLayout.add_tabpanel`
        """
        self.detail_layout.add_tabpanel(*args,**kw)

    @classmethod
    def add_virtual_field(cls,name,vf):
        if False: # disabled because UsersWithClients defines virtual fields on connection_created
            if cls.virtual_fields.has_key(name):
                raise Exception("Duplicate add_virtual_field() %s.%s" % (cls,name))
        cls.virtual_fields[name] = vf
        #~ vf.lino_resolve_type(cls,name)
        vf.name = name
        vf.get = curry(vf.get,cls)
        #~ for k,v in self.virtual_fields.items():
            #~ if isinstance(v,models.ForeignKey):
                #~ v.rel.to = resolve_model(v.rel.to)
        
    @classmethod
    def add_constant(cls,name,vf):
        cls._constants[name] = vf
        vf.name = name
        
    @classmethod
    def after_site_setup(self,site):
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
        #~ logger.info("20130219 Actor.after_site_setup() %s", self)
        self._setup_doing = True
        
        if not self.is_abstract():
            actions.register_params(self)
            
        self._collect_actions()
        
        #~ Parametrizable.after_site_setup(self)
        #~ super(Actor,self).after_site_setup(site)
        if not self.is_abstract():
            actions.setup_params_choosers(self)
            
        #~ logger.info("20130906 Gonna Actor.do_setup() on %s", self)
        self.do_setup()
        #~ self.setup_permissions()
        self._setup_doing = False
        self._setup_done = True
        #~ logger.info("20130906 Actor.after_site_setup() done: %s, default_action is %s", 
            #~ self.actor_id,self.default_action)
        return True
        
        
    @classmethod
    def get_action_by_name(self,name):
        return self._actions_dict.get(name,None)
        #~ a = self._actions_dict.get(name,None)
        #~ if a is not None:
            #~ return actions.BoundAction(self,a)
    get_url_action = get_action_by_name
        
    @classmethod
    def get_url_action_names(self):
        return self._actions_dict.keys()
        
    @classmethod
    def get_actions(self,callable_from=None):
        #~ if self._actions_list is None:
            #~ raise Exception("Tried to %s.get_actions() with empty _actions_list" % self)
        if callable_from is None:
            return self._actions_list
        #~ cf = ba.action.callable_from
        #~ return [ba for ba in self._actions_list 
            #~ if cf is None or isinstance(callable_from,cf)]
        return [ba for ba in self._actions_list if ba.action.is_callable_from(callable_from)]
    
    @classmethod
    def get_data_elem(self,name):
        """
        Find data element in this actor by name.
        """
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
            rpt = settings.SITE.modules[self.app_label].get(name,None)
        elif len(s) == 2:
            if True:
                return settings.SITE.modules.resolve(name)
            else: 
                """
                20130422
                Yes it was a nice feature to silently ignore non installed app_labels
                but mistakenly specifying "person.first_name" instead of "person__first_name"
                did not raise an error.
                """
                m = settings.SITE.modules.get(s[0],None)
                if m is None:
                    return fields.DummyField()
                return m.get(s[1],None)
            # 20121113
            # app = resolve_app(s[0])
            # rpt = getattr(app,s[1],None)
            # rpt = settings.SITE.modules[s[0]].get(s[1],None)
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
    def param_defaults(self,ar,**kw):
        """
        Return a dict with default values for the parameters of a request.
        
        Usage example. The Clients table has a parameter `coached_since` 
        whose default value is empty::
        
          class Clients(dd.Table):
              parameters = dd.ParameterPanel(
                ...
                coached_since=models.DateField(blank=True))
                
        But NewClients is a subclass of Clients with the only difference 
        that the default value is `amonthago`::
                
              
          class NewClients(Clients):
              @classmethod
              def param_defaults(self,ar,**kw):
                  kw = super(NewClients,self).param_defaults(ar,**kw)
                  kw.update(coached_since=amonthago())
                  return kw
        
        """
        for k,pf in self.parameters.items():
            #~ if not param_values.has_key(k):
            kw[k] = pf.get_default()
        return kw
              
    #~ @classmethod
    #~ def request(self,ui=None,request=None,action=None,**kw):
        #~ return ActionRequest(ui,self,request,action,**kw)

    @classmethod
    def request(self,*args,**kw):
        kw.update(actor=self)
        return ActionRequest(*args,**kw)

        
    @classmethod
    def slave_as_html_meth(self):
        """
        Creates and returns the method to be used when 
        :attr:`AbstractTable.slave_grid_format` is `html`.
        """
        def meth(master,ar):
            #~ ar = self.request(ui,request=ar.request,
                #~ master_instance=master,param_values={})
            ar = self.request(master,request=ar.request,param_values={})
            ar.renderer = settings.SITE.ui.default_renderer
            #~ s = ui.table2xhtml(ar).tostring()
            return ar.table2xhtml()
            #~ s = etree.tostring(ui.table2xhtml(ar))
            #~ return s
        return meth
        
    @classmethod
    def show(self,master_instance=None,column_names=None,**known_values):
        """
        Shortcut which creates an action request for this actor 
        and calls its :meth:`lino.core.actions.ActionRequest.to_rst` 
        method.
        """
        kw = dict()
        if master_instance is not None:
            kw.update(master_instance=master_instance)
        kw.update(actor=self)
        kw.update(known_values=known_values)
        kw.update(renderer=settings.SITE.ui.text_renderer)
        print self.request(**kw).to_rst(column_names)
        #~ return settings.SITE.ui.text_renderer.request(**kw).to_rst(column_names)
        #~ username = kw.pop('username',None)
        #~ if username and settings.SITE.user_model is not None:
            #~ kw['user'] = settings.SITE.user_model.objects.get(username=username)
        #~ kw.update(renderer=settings.SITE.ui.text_renderer)
        #~ return self.request(**kw).to_rst(column_names)
        
    @classmethod
    def to_html(self,**kw):
        """
        """
        #~ settings.SITE.startup()
        return E.tostring(self.request(**kw).table2xhtml())
        #~ return self.request(**kw).table2xhtml()
        
    #~ def show(self,*args,**kw):
        #~ print self.to_rst(*args,**kw)

    @classmethod
    def get_screenshot_requests(self,language):
        """
        Return or yield a list of screenshots to generate for this actor.
        Not yet stable. Don't override this. 
        Don't worry if you don't understand. 
        """
        return []


    @classmethod
    def get_choices_text(self,obj,request,field):
        """
        Return the text to be displayed in a combo box 
        for the field `field` of this actor to represent 
        the choice `obj`.
        Override this if you want a customized representation.
        For example :class:`lino_faggio.models.InvoiceItems`
        """
        return obj.get_choices_text(request,self,field)

    #~ @fields.displayfield(_("Actions"))
    #~ def action_buttons(self,obj,ar):
        #~ return E.p(*join_elems([
            #~ settings.SITE.ui.row_action_button(obj,ar.request,ba)
                #~ for ba in ar.actor.get_row_actions(ar,obj)]))
      
    @fields.displayfield(_("Workflow"))
    def workflow_buttons(self,obj,ar):
        """
        Displays the workflow buttons for the given row `obj` and the request `ar`.
        """
        #~ logger.info('20120930 workflow_buttons %r', obj)
        actor = ar.actor
        #~ print 20120621 , actor,  self
        #~ print 20120618, ar
        l = []
        state = actor.get_row_state(obj)
        if state:
            #~ l.append(E.b(unicode(state),style="vertical-align:middle;"))
            l.append(E.b(unicode(state)))
            #~ l.append(u" » ")
            #~ l.append(u" \u25b8 ")
            #~ l.append(u" \u2192 ")
        #~ sep = u" \u25b8 "
        sep = u" \u2192 "
        for ba in ar.actor.get_workflow_actions(ar,obj):
            l.append(sep)
            l.append(ar.action_button(ba,obj))
            sep = ' '
        return E.p(*l)
        
