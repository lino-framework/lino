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

actor_classes = []
#~ actors_dict = None
actors_list = None

ACTOR_SEP = '.'

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
    for cls in actor_classes:
        #~ if not cls.__name__.startswith('unused_'):
        cls.setup()
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
        
        cls.params = []
        for k,v in classDict.items():
            if isinstance(v,models.Field):
                v.set_attributes_from_name(k)
                v.table = cls
                cls.params.append(v)
                
        
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
                #~ cls.class_init()              
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
    def debug_summary(self):
        return "%s (%s)" % (self.__class__,','.join([
            a.name for a in self._actions_list]))
        
    @classmethod
    def get_url(self,ui,**kw):
        return ui.get_action_url(self,self.default_action,**kw)

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
    
        

