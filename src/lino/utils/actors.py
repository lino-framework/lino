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

actors_dict = None
actor_classes = []

ACTOR_SEP = '.'

def get_actor(actor_id):
    return actors_dict[actor_id]
    #~ return cls()
    
def get_actor2(app_label,name):
    k = app_label + ACTOR_SEP + name
    return actors_dict.get(k,None)
    #~ cls = actors_dict.get(k,None)
    #~ if cls is None:
        #~ return cls
    #~ return cls()
    
def setup():
    global actors_dict
    assert actors_dict is None
    actors_dict = {}
    for cls in actor_classes:
        a = cls()
        old = actors_dict.get(a.actor_id,None)
        if old is not None:
            lino.log.debug("Actor %s : %r replaced by %r",a.actor_id,old.__class__,a.__class__)
        actors_dict[a.actor_id] = a
            
        
class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        cls = type.__new__(meta, classname, bases, classDict)
        #lino.log.debug("actor(%s)", cls)
        if classname not in ('Report','Action','Actor','Form','Command'):
            #~ actors_dict[cls.actor_id] = cls
            actor_classes.append(cls)
        return cls

    def __init__(cls, name, bases, dict):
        type.__init__(cls,name, bases, dict)
        cls.instance = None 

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = type.__call__(cls,*args, **kw)
        return cls.instance


class Actor(object):
    __metaclass__ = ActorMetaClass
    app_label = None
    name = None
    label = None
    #default_action = 'view'

    def __init__(self):
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__
        if self.app_label is None:
            self.app_label = self.__class__.__module__.split('.')[-2]
        self.actor_id = self.app_label + ACTOR_SEP + self.name

    def get_label(self):
        #~ if self.label is None:
            #~ return self.__class__.__name__
        return self.label
        
    def __str__(self):
        #~ return '<' + self.actor_id + '>'
        return self.actor_id 
    
    def get_url(self,ui,**kw):
        return ui.get_action_url(self,**kw)

    def get_action(self,action_name=None):
        if action_name is None:
            return self.default_action
            #action_name = self.default_action
        return getattr(self,action_name,None)
        
    def setup(self):
        pass


def unused_get_actor(app_label,name):
    app = models.get_app(app_label)
    cls = getattr(app,name,None)
    if cls is None:
        return None
    return cls()

