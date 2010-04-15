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

import traceback
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

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
    
class ActionEvent(Exception):
    pass
    
class ValidationError(Exception):
    pass
    
#~ class MustConfirm(ActionEvent):
    #~ pass
    
    
class Action:
    action_type = 'open_window'
    label = None
    name = None
    key = None
    needs_selection = False
    needs_validation = False
    
    def __init__(self,actor):
        #~ self.ah = ah # actor handle of the actor who offers this action
        self.actor = actor # actor who offers this action
        if self.name is None:
            self.name = self.__class__.__name__ # label
        if self.label is None:
            self.label = self.name #self.__class__.__name__
        
    def __str__(self):
        return self.name
        
    def run_action(self,act):
        raise NotImplementedError
        
    def before_run(self,act):
        pass
        
    def get_queryset(self,ar):
        return self.actor.get_queryset(ar)
        
    def get_title(self,ar):
        return self.actor.get_title(ar)
        
        
        

class RowsAction(Action):
    needs_selection = False
    needs_validation = False
    
    def before_run(self,ar):
        if self.needs_selection and len(ar.selected_rows) == 0:
            return _("No selection. Nothing to do.")


class ToggleWindowAction(Action):
    action_type = 'toggle_window'
    
class Cancel(Action):
    label = _("Cancel")
    name = 'cancel'
    key = ESCAPE 
    
    def run_in_dlg(self,dlg):
        yield dlg.close_caller().over()

class OK(Action):
    needs_validation = True
    label = _("OK")
    name = "ok"
    key = RETURN

    def run_in_dlg(self,dlg):
        yield dlg.close_caller().over()



