## Copyright 2009 Luc Saffre
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

import traceback
from django.utils.translation import ugettext as _
from django.db import models

import lino

actors_dict = {}

class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        cls = type.__new__(meta, classname, bases, classDict)
        #lino.log.debug("actor(%s)", cls)
        if not classDict.has_key('app_label'):
            # dynamically created report classes must specify themselves their app_label,
            # otherwise the app_label will be 'utils' (from utils.report_factory()).
            cls.app_label = cls.__module__.split('.')[-2]
        actor_id = classDict.get('actor_id',None)
        if actor_id is None:
            actor_id = cls.app_label + "_" + cls.__name__
            cls.actor_id = actor_id
        old = actors_dict.get(cls.actor_id,None)
        if old is not None:
            lino.log.debug("ActorMetaClass %s : %r replaced by %r",cls.actor_id,old,cls)
        actors_dict[cls.actor_id] = cls
        #actors.append(cls)
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
    actor_id = None
    label = None
    def __init__(self):
        if self.label is None:
            self.label = self.__class__.__name__
        #~ if self.name is None:
            #~ self.name = self.__class__.__name__

    def get_label(self):
        #~ if self.label is None:
            #~ return self.__class__.__name__
        return self.label

def get_actor(actor_id):
    cls = actors_dict[actor_id]
    return cls()
    
def old_get_actor(app_label,name):
    k = app_label + "." + name
    cls = actors_dict[k]
    return cls()
    

def unused_get_actor(app_label,name):
    app = models.get_app(app_label)
    cls = getattr(app,name,None)
    if cls is None:
        return None
    return cls()

