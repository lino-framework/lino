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

import logging
logger = logging.getLogger(__name__)

import traceback
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.conf import settings

import lino

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
    
    
class Action(object): 
    opens_a_slave = False
    label = None
    name = None
    key = None
    callable_from = None
    
    def __init__(self,name=None,label=None):
        #~ self.actor = actor # actor who offers this action
        if name is None:
            name = self.name or self.__class__.__name__ 
        elif not isinstance(name,basestring):
            raise Exception("%s name %r is not a string" % (self.__class__,name))
        self.name = name 
        if label is None:
            label = self.label or self.name 
        self.label = label
        assert self.callable_from is None or isinstance(self.callable_from,(tuple,type)), "%s" % self
        
        
class WindowAction(Action):
    pass
    #~ client_side = False
    #~ response_format = 'act' # ext_requests.FMT_RUN

    #~ def run_action(self,ar):
        #~ ar.show_action_window(self) 
        
                
class OpenWindowAction(WindowAction):
    pass
    #~ action_type = 'open_window'
    
    
class ToggleWindowAction(WindowAction):
    opens_a_slave = True
    #~ action_type = 'toggle_window'    
    
class unused_SlaveDetailAction(ToggleWindowAction):
    name = 'detail'
    def __init__(self,actor,layout):
        self.layout = layout
        self.label = layout.label
        #~ self.name = layout._actor_name
        ToggleWindowAction.__init__(self,actor)
        
                
class SlaveGridAction(ToggleWindowAction):
  
    def __init__(self,actor,slave):
        #~ assert isinstance(slave,Report)
        self.slave = slave # .get_handle(ah.ui)
        self.name = slave._actor_name
        #~ print 20100415,self.name
        self.label = slave.button_label
        ToggleWindowAction.__init__(self,actor)
        
        
    
                
class RedirectAction(Action):
    #~ mimetype = None
    def get_target_url(self,elem):
        raise NotImplementedError
        
        
class ImageAction(RedirectAction):
    name = 'image'
    callable_from = tuple()
    
    def get_target_url(self,elem):
        #~ return settings.MEDIA_URL + "/".join(elem.get_image_parts())
        return elem.get_image_url()
      
