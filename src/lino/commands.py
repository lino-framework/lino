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
from lino import actions
from lino import datalinks
from lino.ui import base

class RunCommand(actions.Action):
  
    def run_in_dlg(self,dlg):
        return dlg.ah.actor.run_in_dlg(dlg)

class CommandHandle(datalinks.DataLink):
  
    #~ def __init__(self,ui,command):
        #~ assert isinstance(command,Command)
        #~ datalinks.DataLink.__init__(self,ui,command)
        #~ self.form_handles = {}
        #~ for frm in command.forms.values():
            #~ self.form_handles[frm._actor_name] = frm.get_handle(self)
            
    #~ def get_form_handle(self,name):
        #~ return self.form_handles[name]
        
    def setup(self):
        #~ self.lh = layouts.LayoutHandle(self,self.form.layout(),1)
        self.ui.setup_command(self)
      
class Command(actors.HandledActor):
    cancel = actions.Cancel()
    ok = actions.OK()
    default_action = RunCommand()
    _handle_class = CommandHandle
    _handle_selector = base.UI
    
    #~ def __init__(self):
        #~ actors.HandledActor.__init__(self)
        #~ self.forms = {} # will be filled by lino.layouts.FormLayout.setup()
        
    def run_in_dlg(self,dlg):
        raise NotImplementedError
      
