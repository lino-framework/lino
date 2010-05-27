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
  
            
class Chooser:
    def __init__(self,model,field,meth):
        self.model = model
        #~ self.field = model._meta.get_field(fldname)
        self.field = field
        self.meth = meth
        self.context_params = meth.func_code.co_varnames[1:meth.func_code.co_argcount]
        #~ lino.log.warning("20100527 %s %s",self.context_params,meth)
        self.context_values = []
        self.context_fields = []
        for name in self.context_params:
            f = get_data_elem(self.model,name)
            if f is None:
                lino.log.warning("Model %s has no field %s as asked by %s",self.model,name,meth)
            else:
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

def discover():
    lino.log.info("Discovering choosers...")
    #~ lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        for field in model._meta.fields:
            methname = field.name + "_choices"
            m = getattr(model,methname,None)
            if m is not None:
                setattr(field,'_lino_chooser',Chooser(model,field,m))

def get_for_field(field):
    return getattr(field,'_lino_chooser',None)
