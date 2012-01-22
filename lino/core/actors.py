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

from django.db import models

import lino
from lino.ui import base

from lino.ui.base import Handled
from lino.core import fields
from lino.utils import curry

actor_classes = []
#~ actors_dict = None
actors_list = None

ACTOR_SEP = '.'

class CreatePermission: pass
          


#~ from lino.core import actions

def unused_resolve_action(spec,app_label=None):
    if spec is None: return None
    if isinstance(spec,actions.Action): return spec
    s = spec.split('.')
    if len(s) == 1:
        if not app_label:
            return None
        actor = get_actor2(app_label,spec)
    elif len(s) == 3:
        actor = get_actor('.'.join(s[0:2]))
        if actor is None:
            model = models.get_model(s[0],s[1],False)
            #~ print "20110712 actor is None, model is", model, s
            if model is None:
                return None
            actor = model._lino_model_report
        #~ print 20110627, actor, s, actor._actions_dict
        return actor.get_action(s[2])
    else:
        actor = get_actor(spec)
    if actor is None:
        return None
        #~ raise Exception("Actor %r does not exist" % spec)
    return actor.default_action
  
def register_actor(a):
    logger.debug("register_actor %s",a.actor_id)
    #~ old = actors_dict.get(a.actor_id,None)
    #~ if old is not None:
        #~ logger.debug("register_actor %s : %r replaced by %r",a.actor_id,old,a)
        #~ actors_list.remove(old)
    #~ actors_dict[a.actor_id] = a
    actors_list.append(a)
    return a
  
    #~ actor.setup()
    #~ assert not actors_dict.has_key(actor.actor_id), "duplicate actor_id %s" % actor.actor_id
    #~ actors_dict[actor.actor_id] = actor
    #~ return actor

def discover():
    global actor_classes
    #~ global actors_dict
    global actors_list
    #~ assert actors_dict is None
    assert actors_list is None
    #~ actors_dict = {}
    actors_list = []
    logger.debug("actors.discover() : setting up %d actors",len(actor_classes))
    for cls in actor_classes:
        cls.class_init()
        register_actor(cls)
    actor_classes = None
    
    #~ logger.debug("actors.discover() : setup %d actors",len(actors_list))
    #~ for a in actors_list:
        #~ a.setup()
        
    #~ logger.debug("actors.discover() done")
        #~ a = cls()
        #~ old = actors_dict.get(a.actor_id,None)
        #~ if old is not None:
            #~ logger.debug("Actor %s : %r replaced by %r",a.actor_id,old.__class__,a.__class__)
        #~ actors_dict[a.actor_id] = a
    #~ for a in actors_dict.values():
        #~ a.setup()

def setup_actors():
    for cls in actors_list:
        #~ if not cls.__name__.startswith('unused_'):
        cls.setup()
        
def unused_add_virtual_field(cls,name,v):
    cls.virtual_fields[name] = v
    v.name = name
    #~ vf.lino_kernel_setup(cls,name)
    v.get = curry(v.get,cls)

class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
            
        
        # attributes that are not inherited from base classes:
        #~ classDict.setdefault('name',classname)
        classDict.setdefault('label',None)
        classDict.setdefault('button_label',None)
        classDict.setdefault('title',None)
        
        cls = type.__new__(meta, classname, bases, classDict)
        
        
        if cls.parameters:
            for k,v in cls.parameters.items():
                v.set_attributes_from_name(k)
                v.table = cls
                
        cls.virtual_fields = {}
        for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
            #~ if isinstance(v,(models.Field,fields.VirtualField)):
            if isinstance(v,fields.VirtualField):
                cls.add_virtual_field(k,v)
                #~ add_virtual_field(cls,k,v)
                
                
        #~ cls.params = []
        #~ for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
                #~ v.set_attributes_from_name(k)
                #~ v.table = cls
                #~ cls.params.append(v)
                
        
        """
        On 20110822 I thought "A Table always gets the app_label of its model,
        you cannot set this yourself in a subclass
        because otherwise it gets complex when inheriting reports from other
        app_labels."
        On 20110912 I cancelled change 20110822 because PersonsByOffer 
        should clearly get app_label 'jobs' and not 'contacts'.
        
        """
        
        #~ if not 'app_label' in classDict.keys():
        #~ if cls.app_label is None:
        if classDict.get('app_label',None) is None:
            #~ if self.app_label is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            #~ m = sys.modules[self.__module__]
            #~ self.app_label = m.__name__.split('.')[-2]
            cls.app_label = cls.__module__.split('.')[-2]
            #~ self.app_label = self.model._meta.app_label
            
        #~ cls.app_label = cls.__module__.split('.')[-2]
            
        
        cls.actor_id = cls.app_label + '.' + cls.__name__
        cls._actions_list = []
        cls._actions_dict = {}
        cls._setup_done = False
        cls._setup_doing = False
        
        if classname not in (
            'Table','AbstractTable','CustomTable',
            'Action','HandledActor','Actor','Frame'):
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
        
  
class Actor(Handled):
    "Base class for Tables and Frames"
    
    __metaclass__ = ActorMetaClass
    
    app_label = None
    """
    The default value is deduced from the module where the 
    subclass is defined.
    Applications should not need to explicitly set this attribute, 
    but :func:`lino.core.table.table_factory`
    uses it to specify a value which overrides the default.
    """
    
    default_list_action_name = 'grid'
    default_elem_action_name =  'detail'

    
    disabled_fields = None
    """
    Return a list of field names that should not be editable 
    for the specified `obj` and `request`.
    
    If defined in the Table, this must be a method that accepts 
    two arguments `request` and `obj`::
    
      def disabled_fields(self,obj,request):
          ...
          return []
    
    If not defined in a subclass, the report will look whether 
    it's model has a `disabled_fields` method expecting a single 
    argument `request` and install a wrapper to this model method.
    See also :doc:`/tickets/2`.
    """
    
    disable_editing = None
    """
    Return `True` if the record as a whole should be read-only.
    Same remarks as for :attr:`disabled_fields`.
    """
    
    detail_action = None
    
    active_fields = []
    """A list of field names that are "active" (cause a save and 
    refresh of a Detail or Insert form).
    """
    
    has_navigator = True
    """
    Whether a Detail Form should have navigation buttons.
    This option is False in :class:`lino.SiteConfigs`.
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
    
    params_panel_hidden = True
    """
    If this table has parameters, set this to False if the parameters 
    panel should be hidden when the table is rendered in a grid widget.
    """
    
    
    
    #~ _actor_name = None
    title = None
    label = None
    #~ actions = []
    default_action = None
    actor_id = None

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
        
    @classmethod
    def debug_summary(self):
        return "%s (%s)" % (self.__class__,','.join([
            a.name for a in self._actions_list]))
        
    @classmethod
    def get_permission(self,p,user):
        return True
        
    @classmethod
    def get_detail_sets(self):
        """
        Yield a list of (app_label,name) tuples for which the kernel 
        should try to create a Detail Set.
        """
        yield self.app_label + '/' + self.__name__
            
    @classmethod
    def get_detail(self):
        return self._lino_detail
        
    #~ @classmethod
    #~ def add_virtual_field(cls,name,vf): 
        #~ add_virtual_field(cls,name,vf)
        
    @classmethod
    def add_virtual_field(cls,name,vf):
        cls.virtual_fields[name] = vf
        vf.name = name
        vf.get = curry(vf.get,cls)
        
    @classmethod
    def get_url(self,ui,**kw):
        return ui.action_url_http(self,self.default_action,**kw)

    @classmethod
    def setup(self):
        #~ raise "20100616"
        #~ assert not self._setup_done, "%s.setup() called again" % self
        if self._setup_done:
            return True
        if self._setup_doing:
            if True: # severe error handling
                raise Exception("%s.setup() called recursively" % self.actor_id)
            else:
                logger.warning("%s.setup() called recursively" % self.actor_id)
                return False
        #~ logger.debug("Actor.setup() %s", self)
        self._setup_doing = True
        
        #~ if self.label is None:
            #~ self.label = self.__name__
        #~ if self.title is None:
            #~ self.title = self.label
        
        self.do_setup()
        self._setup_doing = False
        self._setup_done = True
        logger.debug("20120103 Actor.setup() done: %s, default_action is %s", 
            self.actor_id,self.default_action)
        return True
        
    @classmethod
    def set_actions(self,actions):
        self._actions_list = []
        self._actions_dict = {}
        for a in actions:
            self.add_action(a)
            
    @classmethod
    def add_action(self,a):
        if hasattr(a,'actor') and a.actor is not self:
            raise Exception("20120103")
        if self._actions_dict.has_key(a.name):
            #~ logger.warning("%s action %r : %s overridden by %s",
              #~ self,a.name,self._actions_dict[a.name],a)
            raise Exception(
              "%s action %r : %s overridden by %s" %
              (self,a.name,self._actions_dict[a.name],a))
        self._actions_dict[a.name] = a
        self._actions_list.append(a)
            
    @classmethod
    def get_action(self,name):
        return self._actions_dict.get(name,None)
        
    @classmethod
    def get_actions(self,callable_from=None):
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
        #~ cc = self.computed_columns.get(name,None)
        #~ if cc is not None:
            #~ return cc
        vf = self.virtual_fields.get(name,None)
        if vf is not None:
            return vf
        return None
              
