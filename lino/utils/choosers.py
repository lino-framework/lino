## Copyright 2009-2012 Luc Saffre
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

"""

The :mod:`lino.utils.choosers` extends the possibilities 
for defining choices for fields of a Django model.

- Context-sensitive choices
- Non-limiting choices 
  (specify a pick list of suggestions but leave the possibility to manually enter different values)
- Self-learning Combos
  (having new items automatically stored server-side)

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from lino.utils.instantiator import make_converter
#~ from lino import reports
from lino.core.coretools import get_data_elem # , get_unbound_meth
import lino
from lino.core import fields
from lino.utils import get_class_attr
from lino.ui import requests as ext_requests

class BaseChooser:
    pass
  
class FieldChooser(BaseChooser):
    def __init__(self,field):
        self.field = field
        
class ChoicesChooser(FieldChooser):
    def __init__(self,field):
        FieldChooser.__init__(self,field)
        self.simple_values = type(field.choices[0])
  

class Chooser(FieldChooser):
    #~ stored_name = None
    simple_values = False
    instance_values = True
    force_selection = True
    #~ force_selection = True
    #~ on_quick_insert = None
    #~ quick_insert_field = None
    can_create_choice = False
    def __init__(self,model,field,meth):
        FieldChooser.__init__(self,field)
        self.model = model
        #~ self.field = model._meta.get_field(fldname)
        self.meth = meth
        if not isinstance(field,models.ForeignKey):
            self.simple_values = getattr(meth,'simple_values',False)        
            self.instance_values = getattr(meth,'instance_values',False)
            self.force_selection = getattr(meth,'force_selection',self.force_selection)
        #~ self.context_params = meth.func_code.co_varnames[1:meth.func_code.co_argcount]
        self.context_params = meth.context_params
        #~ self.context_params = meth.func_code.co_varnames[:meth.func_code.co_argcount]
        #~ print '20100724', meth, self.context_params
        #~ logger.warning("20100527 %s %s",self.context_params,meth)
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
        #~ try:
        for f in self.context_fields:
            cv = make_converter(f)
            if cv is not None:
                self.converters.append(cv)
        #~ except models.FieldDoesNotExist,e:
            #~ print e
            
        #~ m = get_unbound_meth(model,field.name + "_display")
        #~ if m is not None:
            #~ self.display_meth
            
        if hasattr(model,"create_%s_choice" % field.name):
            self.can_create_choice = True
            
    def __str__(self):
        return "Chooser(%s.%s,%s)" % (
            self.model.__name__,self.field.name,
            self.context_params)
        
    def create_choice(self,obj,text):
        m = getattr(obj,"create_%s_choice" % self.field.name)
        return m(text)
        
    def get_data_elem(self,name):
        for vf in self.model._meta.virtual_fields:
            if vf.name == name:
                return vf
        return self.model._meta.get_field(name)
            
    def get_choices(self,**context):
        "Return a list of choices for this chooser, using keyword parameters as context."
        args = []
        for varname in self.context_params:
            args.append(context.get(varname,None))
        #~ print args
        return self.meth(*args)
      
    #~ def get_instance_choices(self,obj):
        #~ "Return a list of choices for this chooser, using `obj` as context."
        #~ args = []
        #~ for varname in self.context_params:
            #~ args.append(getattr(obj,varname,None))
        #~ return self.meth(*args)
      
    def get_request_choices(self,request,tbl):
        kw = {}
        
        # 20120202
        if tbl.master_field is not None:
            mt = request.REQUEST.get(ext_requests.URL_PARAM_MASTER_TYPE)
            try:
                master = ContentType.objects.get(pk=mt).model_class()
            except ContentType.DoesNotExist,e:
                pass
                
            pk = request.REQUEST.get(ext_requests.URL_PARAM_MASTER_PK,None)
            if pk:
                try:
                    kw[tbl.master_field.name] = master.objects.get(pk=pk)
                except ValueError,e:
                    raise Exception("Invalid primary key %r for %s",pk,master.__name__)
                except master.DoesNotExist,e:
                    # todo: ReportRequest should become a subclass of Dialog and this exception should call dlg.error()
                    raise Exception("There's no %s with primary key %r" % (master.__name__,pk))
      
        
        for k,v in request.GET.items():
            kw[str(k)] = v
        for cv in self.converters:
            kw = cv.convert(**kw)
        #~ logger.info("20111213 get_request_choices(%r) -> %r",self.converters,kw)
        return self.get_choices(**kw)
        
    def get_text_for_value(self,value,obj):
        m = getattr(self.field,'get_text_for_value',None)
        if m is not None:  # e.g. lino.utils.choicelist.ChoiceListField
            return m(value)
        #~ raise NotImplementedError
        #~ assert not self.simple_values
        m = getattr(obj,"get_" + self.field.name + "_display")
        return m(value)
        #~ raise NotImplementedError("%s : Cannot get text for value %r" % (self.meth,value))
        
def check_for_chooser(model,field):
    methname = field.name + "_choices"
    m = get_class_attr(model,methname)
    if m is not None:
        #~ n += 1
        ch = Chooser(model,field,m)
        setattr(field,'_lino_chooser',ch)
        #~ logger.debug("Installed %s",ch)
    #~ else:
        #~ logger.info("No chooser for %s.%s",model,field.name)


def discover():
    logger.info("Discovering choosers...")
    #~ logger.debug("Instantiate model reports...")
    for model in models.get_models():
        #~ n = 0
        for field in model._meta.fields + model._meta.virtual_fields:
            check_for_chooser(model,field)
        #~ logger.debug("Discovered %d choosers in model %s.",n,model)

def get_for_field(fld):
    return getattr(fld,'_lino_chooser',None)

def uses_simple_values(fld):
    "used by :class:`lino.ui.extjs.ext_store.Store`"
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


def chooser(**options):
    #~ options.setdefault('quick_insert_field',None)
    def chooser_decorator(fn):
        def wrapped(*args):
            #~ print 20101220, args
            return fn(*args)
        wrapped.context_params = fn.func_code.co_varnames[1:fn.func_code.co_argcount]
        for k,v in options.items():
            setattr(wrapped,k,v)
        return classmethod(wrapped)
    return chooser_decorator
    

