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

from lino.core import datalinks

class Input:
    def __init__(self,**kw):
        self.options = kw

class List(Input):
    pass

  


class FormHandle(datalinks.DataLink):
  
    def __init__(self,lh,dl):
        self.lh = lh
        self.dl = dl
        self._values = {}
        lh.ui.setup_form(self)
        
        
    def __init__(self,ui,lh):
        self.lh = lh
        self.elements = [] # datalink elements
        self.inputs = []
        for n in dir(lh.layout):
            v = getattr(lh.layout,n)
            if isinstance(v,Input):
                self.elements.append(n)
                v.name = n
                self.inputs.append(v)
            else:
                #lino.log.debug("ignored %s attribute %r=%r",self.form,n,v)
                pass
        datalinks.DataLink.__init__(self,ui,self.actions)
                
    def data_elems(self):
        return self.elements
        #~ for k in self.elements.keys(): yield k
          
    def get_data_elem(self,name):
        return getattr(self.lh,name,None)
        
    def get_title(self,dlg):
        return self.form.lh.title # or self.lh.layout.label
        
    
class Form:
    def __init__(self,lh):
        self.lh = lh
      
    def get_handle(self,ui):
        return FormLayout(self)
        
        
        
    def update(self,**kw):
        self._values.update(**kw)
        
    def get_value(self,name):
        return self._values.get(name)
    
    def form2dict(self,dlg,**kw):
        for i in self.inputs:
            if isinstance(i,List):
                v = dlg.request.POST.getlist(i.name)
            else:
                v = dlg.request.POST.get(i.name)
            kw[i.name] = v
        return kw
        
        