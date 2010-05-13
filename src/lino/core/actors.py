## Copyright 2009-2010 Luc Saffre
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

from django.utils.translation import ugettext as _
from django.db import models

import lino
from lino.ui import base
from lino import actions
from lino.ui.base import Handled

actor_classes = []
actors_dict = None
actors_list = None

ACTOR_SEP = '.'

def resolve_action(spec,app_label=None):
    if spec is None: return None
    if isinstance(spec,actions.Action): return spec
    s = spec.split(ACTOR_SEP)
    if len(s) == 1:
        actor = get_actor2(app_label,spec)
    elif len(s) == 3:
        actor = get_actor(ACTOR_SEP.join(s[0:2]))
        return actor.get_action(s[2])
    else:
        actor = get_actor(spec)
    if actor is None:
        raise Exception("Actor %r does not exist" % spec)
    return actor.default_action
  
def get_actor(actor_id):
    return actors_dict.get(actor_id,None)
    #~ return cls()
    
def get_actor2(app_label,name):
    k = app_label + ACTOR_SEP + name
    return actors_dict.get(k,None)
    #~ cls = actors_dict.get(k,None)
    #~ if cls is None:
        #~ return cls
    #~ return cls()
    
def resolve_actor(actor,app_label):
    if actor is None: return None
    if isinstance(actor,Actor): return actor
    s = actor.split(ACTOR_SEP)
    if len(s) == 1:
        return get_actor2(app_label,actor)
    return get_actor(actor)
        
def register_actor(a):
    old = actors_dict.get(a.actor_id,None)
    if old is None:
        lino.log.debug("register_actor %s = %r",a.actor_id,a.__class__)
    else:
        lino.log.debug("register_actor %s : %r replaced by %r",a.actor_id,old.__class__,a.__class__)
        actors_list.remove(old)
    actors_dict[a.actor_id] = a
    actors_list.append(a)
    return a
  
    #~ actor.setup()
    #~ assert not actors_dict.has_key(actor.actor_id), "duplicate actor_id %s" % actor.actor_id
    #~ actors_dict[actor.actor_id] = actor
    #~ return actor

def discover():
    global actor_classes
    global actors_dict
    global actors_list
    assert actors_dict is None
    assert actors_list is None
    actors_dict = {}
    actors_list = []
    lino.log.debug("actors.discover() : instantiating %d actors",len(actor_classes))
    for cls in actor_classes:
        register_actor(cls())
    actor_classes = None
    
    #~ lino.log.debug("actors.discover() : setup %d actors",len(actors_list))
    #~ for a in actors_list:
        #~ a.setup()
        
    lino.log.debug("actors.discover() done")
        #~ a = cls()
        #~ old = actors_dict.get(a.actor_id,None)
        #~ if old is not None:
            #~ lino.log.debug("Actor %s : %r replaced by %r",a.actor_id,old.__class__,a.__class__)
        #~ actors_dict[a.actor_id] = a
    #~ for a in actors_dict.values():
        #~ a.setup()


class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        cls = type.__new__(meta, classname, bases, classDict)
        #lino.log.debug("actor(%s)", cls)
        if classname not in ('Report','Action','HandledActor','Actor','Command',
              'Layout','ListLayout','DetailLayout','FormLayout',
              'ModelLayout'):
            #~ actors_dict[cls.actor_id] = cls
            if actor_classes is None:
                lino.log.debug("%s definition was after discover",cls)
            else:
                lino.log.debug("Found actor %s.",cls)
                actor_classes.append(cls)
        return cls

    def __init__(cls, name, bases, dict):
        type.__init__(cls,name, bases, dict)
        cls.instance = None 

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = type.__call__(cls,*args, **kw)
        return cls.instance

  
class Actor(Handled):
    "inherited by Report, Command, Layout"
    __metaclass__ = ActorMetaClass
    app_label = None
    _actor_name = None
    title = None
    label = None
    actions = []
    default_action = None

    def __init__(self):
        self._setup_done = False
        self._setup_doing = False
        if self.label is None:
            self.label = self.__class__.__name__
        if self.title is None:
            self.title = self.label
        if self._actor_name is None:
            self._actor_name = self.__class__.__name__
        else:
            assert type(self._actor_name) is str
        if self.app_label is None:
            #~ self.__class__.app_label = self.__class__.__module__.split('.')[-2]
            self.app_label = self.__class__.__module__.split('.')[-2]
        self.actor_id = self.app_label + ACTOR_SEP + self._actor_name
        self._forms = {} # will be filled by lino.layouts.FormLayout.setup()
        self._actions_list = []
        self._actions_dict = {}
        Handled.__init__(self)

        lino.log.debug("Actor.__init__() %s",self)

    def get_label(self):
        #~ if self.label is None:
            #~ return self.__class__.__name__
        return self.label
        
    def __str__(self):
        #~ return '<' + self.actor_id + '>'
        return self.actor_id 
        
    #~ def define_action(self,a):
        #~ self._actions_list.append(a)
        #~ self._actions_dict[a.name] = a
    
    def get_url(self,ui,**kw):
        return ui.get_action_url(self,self.default_action,**kw)

    #~ def get_action(self,action_name=None):
        #~ if action_name is None:
            #~ return self.default_action
            #~ #action_name = self.default_action
        #~ return getattr(self,action_name,None)
        
    def setup(self):
        assert not self._setup_done, "%s.setup() called again" % self
        if self._setup_done:
            return True
        if self._setup_doing:
            if True: # severe error handling
                raise Exception("%s.setup() called recursively" % self.actor_id)
            else:
                lino.log.warning("%s.setup() called recursively" % self.actor_id)
                return False
        lino.log.debug("Actor.setup() %s", self)
        self._setup_doing = True
        self.do_setup()
        self._setup_doing = False
        self._setup_done = True
        #~ lino.log.debug("Report.setup() done: %s", self.actor_id)
        return True
        
    def do_setup(self):
        pass
        
        
    def set_actions(self,actions):
        self._actions_list = actions
        self._actions_dict = {}
        for a in actions:
            self.add_action(a)
            
    def add_action(self,a):
        if self._actions_dict.has_key(a.name):
            lino.log.warning("%s action %r : %s overridden by %s",self,a.name,self._actions_dict[a.name],a)
        self._actions_dict[a.name] = a
            
    def get_action(self,name):
        return self._actions_dict.get(name,None)
        
    def get_actions(self):
        return self._actions_list
    
        

