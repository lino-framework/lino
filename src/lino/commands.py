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

import lino
from lino.utils import actors
#~ from lino import forms
from lino import actions
from lino import datalinks
from lino.ui import base

class Input:
    def __init__(self,**kw):
        self.options = kw

class List(Input):
    pass

  
class CommandHandle(datalinks.DataLink,actors.ActorHandle):
#~ class CommandHandle(datalinks.FormHandle):
  
    def __init__(self,ui,command):
        assert isinstance(command,Command)
        datalinks.DataLink.__init__(self,ui,command.actions)
        actors.ActorHandle.__init__(self,command)
        self.command = command
        self.elements = [] # datalink elements
        self.inputs = []
        for n in dir(command):
            v = getattr(command,n)
            if isinstance(v,Input):
                v.name = n
                self.elements.append(n)
                #~ self.elements[n] = v
                self.inputs.append(v)
            #~ elif isinstance(v,actions.Action):
                #~ self.define_action(v)
                #~ self.elements.append(n)
                #~ self.elements[n] = v
            elif callable(v):
                #~ self.elements[n] = v
                self.elements.append(n)
            else:
                #lino.log.debug("ignored %s attribute %r=%r",self.form,n,v)
                pass
                
        #~ self.form_handles = {}
        #~ for frm in command.forms.values():
            #~ self.form_handles[frm._actor_name] = frm.get_handle(self)
                
    def data_elems(self):
        return self.elements
        #~ for k in self.elements.keys(): yield k
          
    def get_data_elem(self,name):
        return getattr(self.command,name,None)
        
    def before_step(self,dlg):
        for i in self.inputs:
            if isinstance(i,List):
                v = dlg.request.POST.getlist(i.name)
            else:
                v = dlg.request.POST.get(i.name)
            dlg.params[i.name] = v
        #~ for k,v in request.POST.iterlists():
            #~ params[k] = v
        #~ params = dict(request.POST.iterlists())
        #~ print 20100318, self.params
        
    #~ def get_form_handle(self,name):
        #~ return self.form_handles[name]
        
    def setup(self):
        #~ self.lh = layouts.LayoutHandle(self,self.form.layout(),1)
        self.ui.setup_command(self)
        
    def get_title(self,dlg):
        return self.command.title # or self.lh.layout.label
        
    def submit_elems(self):
        for i in self.inputs: yield i.name
        
      
class RunCommand(actions.Action):
  
    def run_in_dlg(self,dlg):
        return dlg.ah.command.run_in_dlg(dlg)

class Command(actors.HandledActor):
    actions = [actions.Cancel(), actions.OK()]
    default_action = RunCommand()
    _handle_class = CommandHandle
    _handle_selector = base.UI
    
    #~ def __init__(self):
        #~ actors.HandledActor.__init__(self)
        #~ self.forms = {} # will be filled by lino.layouts.FormLayout.setup()
        
    def run_in_dlg(self,dlg):
        raise NotImplementedError
      
