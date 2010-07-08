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

from django.db import models
from lino.utils.instantiator import make_converter
#~ from lino import reports
from lino.core.coretools import get_data_elem
import lino
  
  
class BaseChooser:
    def __init__(self,field):
        self.field = field
        
class ChoicesChooser(BaseChooser):
    def __init__(self,field):
        BaseChooser.__init__(self,field)
        self.simple_values = type(field.choices[0])
  
class Chooser(BaseChooser):
    def __init__(self,model,field,meth):
        BaseChooser.__init__(self,field)
        self.model = model
        #~ self.field = model._meta.get_field(fldname)
        self.meth = meth
        self.simple_values = getattr(meth,'simple_values',False)
        self.context_params = meth.func_code.co_varnames[1:meth.func_code.co_argcount]
        #~ lino.log.warning("20100527 %s %s",self.context_params,meth)
        self.context_values = []
        self.context_fields = []
        for name in self.context_params:
            f = self.get_data_elem(name)
            self.context_fields.append(f)
            self.context_values.append(name+"Hidden")
            #~ if isinstance(f,models.ForeignKey):
                #~ self.context_values.append(name+"Hidden")
            #~ else:
                #~ self.context_values.append(name)
        self.converters = []
        try:
            for f in self.context_fields:
                cv = make_converter(f)
                if cv is not None:
                    self.converters.append(cv)
        except models.FieldDoesNotExist,e:
            print e
            
    def get_data_elem(self,name):
        for vf in self.model._meta.virtual_fields:
            if vf.name == name:
                return vf
        return self.model._meta.get_field(name)
            
    def get_choices(self,**context):
        args = []
        for varname in self.context_params:
            args.append(context.get(varname,None))
            return self.meth(*args)
      
    def get_request_choices(self,request):
        kw = {}
        for k,v in request.GET.items():
            kw[str(k)] = v
        for cv in self.converters:
            kw = cv.convert(**kw)
        return self.get_choices(**kw)
        
    def get_text_for_value(self,value,obj):
        raise NotImplementedError

def discover():
    lino.log.info("Discovering choosers...")
    #~ lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        for field in model._meta.fields:
            methname = field.name + "_choices"
            m = getattr(model,methname,None)
            if m is not None:
                setattr(field,'_lino_chooser',Chooser(model,field,m))
                #~ lino.log.info("Chooser for %s.%s",model,field.name)
            #~ else:
                #~ lino.log.info("No chooser for %s.%s",model,field.name)

def get_for_field(fld):
    return getattr(fld,'_lino_chooser',None)

def uses_simple_values(fld):
    if isinstance(fld,models.ForeignKey):
        return False
    ch = get_for_field(fld)
    if ch is not None:
        return ch.simple_values
    if fld.choices and type(fld.choices[0]) in (list,tuple):
        return False
    return True

#~ def get_for_field(fieldspec):
    #~ fld = resolve_field(fieldspec)
    #~ return get_for_field()
