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

from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _

import lino
from lino import actions

                
class DataLink:
    """
    A DataLink provides the columns of a tabular data view (or the fields of a form data view) and the row actions.
    Abstract base class for CommandHandle, ReportHandle and RowHandle.
    """
    
    content_type = None
    
    def __init__(self,ui,actions):
        self.ui = ui
        self._actions_list = actions
        self._actions_dict = {}
        for a in actions:
            self._actions_dict[a.name] = a
        
        #~ self.actor = actor
        #~ self.name = actor.actor_id
        #~ self.elements = SortedDict() # datalink elements
        #~ self.form_handles = {}
        
        #~ for frm in actor._forms.values():
            #~ self.form_handles[frm._actor_name] = frm.get_handle(self)
            
        #~ lino.log.debug("%s handle : %s",form,self.elements.keys())
        
    #~ def get_form_handle(self,name):
        #~ return self.form_handles[name]
        

    def try_get_virt(self,name):
        return None
        
    #~ def get_default_layout(self):
        #~ return self.lh
        
    def get_title(self,dlg):
        raise NotImplementedError
        
    def data_elems(self):
        raise NotImplementedError
        
    def get_data_elem(self,name):
        raise NotImplementedError
        
    def before_step(self,dlg):
        pass
        
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_actor_url(self,*args,**kw)

    def get_details(self):
        return []

    def get_slaves(self):
        return []
        
    def get_action(self,name):
        return self._actions_dict.get(name,None)
        
    def get_actions(self):
        return self._actions_list
    


class RowLink:
  
    def get_from_form(self,post_data):
        raise NotImplementedError()
        
    def update(self,**kw):
        raise NotImplementedError()
      