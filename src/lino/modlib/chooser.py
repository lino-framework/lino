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

class Chooser:
  
    def __init__(self,model,fldname):
        methname = fldname + "_choices"
        meth = getattr(model,methname,None)
        self.model = model
        self.field = model._meta.get_field(fldname)
        self.meth = meth
        
        
    def get_choices(self,**data):
        if self.meth is not None:
            args = []
            for varname in self.meth.func_code.co_varnames[1:]:
                args.append(data.get(varname,None))
                return self.meth(*args)
        if isinstance(self.field,models.ForeignKey):
            return self.field.rel.to.objects.all()
        return self.field.choices

class FormChooser(Chooser):
    def __init__(self,*args):
        Chooser.__init__(self,*args)
        self.converters = []
        if self.meth is not None:
            for varname in self.meth.func_code.co_varnames[1:]:
                f = self.model._meta.get_field(varname)
                cv = make_converter(f)
                if cv is not None:
                    self.converters.append(cv)
                    
    def get_choices(self,**data):
        for cv in self.converters:
            data = cv.convert(**data)
        return Chooser.get_choices(self,**data)
    

#~ def get_chooser(model,fldname):
    #~ if meth is not None:
        #~ return Chooser(model,fldname,meth)

def unused_get_field_choices_meth(model,fldname):
    # used also in extjs to test whether this field does have context-sensitive choices
    methname = fldname + "_choices"
    return getattr(model,methname,None)


def unused_get_field_choices(model,fld,context):
    # context is a dict of field values in the receiving instance
    meth = get_field_choices_meth(model,fld.name)
    choices = None
    if meth is not None:
        args = [] 
        for varname in meth.func_code.co_varnames[1:]:
            args.append(context.get(varname,None))
            #~ context_field, remote, direct, m2m = self.model._meta.get_field_by_name(varname)
        choices = meth(*args)
    if choices is None:
        choices = fld.rel.to.objects.all()
    return choices
