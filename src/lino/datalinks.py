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
from lino import forms
from lino import actions

class DataLink:
    "inherited by CommandHandle and ReportHandle"
    
    content_type = None
    
    def __init__(self,ui,actor):
        self.ui = ui
        self.actor = actor
        self.name = actor.actor_id
        self.elements = SortedDict() # datalink elements
        self.inputs = []
        self.form_handles = {}
        
        for n in dir(actor):
            v = getattr(actor,n)
            if isinstance(v,forms.Input):
                v.name = n
                self.elements[n] = v
                self.inputs.append(v)
            elif isinstance(v,actions.Action):
                #v.name = n
                self.elements[n] = v
            elif callable(v):
                self.elements[n] = v
            else:
                #lino.log.debug("ignored %s attribute %r=%r",self.form,n,v)
                pass
                
        for frm in actor._forms.values():
            self.form_handles[frm._actor_name] = frm.get_handle(self)
            
        #~ lino.log.debug("%s handle : %s",form,self.elements.keys())
        
    def get_form_handle(self,name):
        return self.form_handles[name]
        

    def try_get_virt(self,name):
        return None
        
    #~ def get_default_layout(self):
        #~ return self.lh
        
    def get_title(self,dlg):
        return self.actor.title # or self.lh.layout.label
        
    def data_elems(self):
        for k in self.elements.keys(): yield k
          
    def get_data_elem(self,name):
        return getattr(self.actor,name,None)
                
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_actor_url(self,*args,**kw)

    def get_actions(self):
        return []
        
    def get_details(self):
        return []

    def get_slaves(self):
        return []
        
      
