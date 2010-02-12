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

import lino

from lino.utils import perms, menus, actors
from lino import actions, layouts

class Input:
    def __init__(self,**kw):
        self.options = kw

class ViewForm(actions.Action):
    def run(self,context):
        return context.ui.view_form(context)

class Form(actors.Actor): # actions.Action):
    layout = None
    title = None
    
    cancel = actions.CancelDialog()
    
    default_action = ViewForm()

    def __init__(self):
        #actions.Action.__init__(self)
        actors.Actor.__init__(self)
        self._handles = {}
        
    def run(self,context):
        return context.ui.view_form(self,context)
        
    def get_url(self,ui,**kw):
        h = self.get_handle(ui)
        return h.get_absolute_url(**kw)
        
    def get_handle(self,ui):
        return ui.get_form_handle(self)
        
    def setup(self):
        pass


class FormHandle(layouts.DataLink):
    content_type = None
    def __init__(self,ui,form):
        lino.log.debug('FormHandle.__init__(%s)',form)
        layouts.DataLink.__init__(self,ui,form.actor_id)
        assert isinstance(form,Form)
        self.actor = self.form = form
        self.elements = SortedDict() # datalink elements
        self.inputs = []
        
        for n in dir(form):
            v = getattr(form,n)
            if isinstance(v,Input):
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
        lino.log.debug("%s handle : %s",form,self.elements.keys())
                
    def setup(self):
        self.lh = layouts.LayoutHandle(self,self.form.layout(),1)

    def get_title(self,context):
        return self.form.title or self.form.layout.label
        
    def data_elems(self):
        for k in self.elements.keys(): yield k
          
          
    def get_data_elem(self,name):
        return getattr(self.form,name,None)
                
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_form_url(self,*args,**kw)


    def get_actions(self):
        return []
        
    def get_details(self):
        return []

    def get_slaves(self):
        return []
      
        
    #~ def get_fields(self):
        #~ return self._fields
          
    #~ def get_slave(self,name):
        #~ return None
        
    #~ def try_get_action(self,name):
        #~ return self._actions.get(name,None)
        
    #~ def try_get_meth(self,name):
        #~ return self._methods.get(name,None)
        #~ v = getattr(self.form,name,None)
        #~ if v is None:
            #~ return None
        #~ print type(v)
        #~ raise NotImplementedError
        
    #~ def try_get_field(self,name):
        #~ return self._fields.get(name,None)
        #~ try:
            #~ v = getattr(self.form,name,None)
            #~ if v is None:
                #~ return None
            #~ if not isinstance(v,Input):
                #~ return None
            #~ return v
            #~ #return self.form.fields[name]
        #~ except KeyError,e:
            #~ pass



