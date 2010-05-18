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

import types
import datetime

from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

import lino
from lino.utils import menus


def dict2js(d):
    return ", ".join(["%s: %s" % (k,py2js(v)) for k,v in d.items()])

CONVERTERS = []

def register_converter(func):
    CONVERTERS.append(func)


def py2js(v):
    #~ lino.log.debug("py2js(%r)",v)
    for cv in CONVERTERS:
        v = cv(v)
        
    #~ if isinstance(v,menus.Menu):
        #~ if v.parent is None:
            #~ return py2js(v.items)
            #~ #kw.update(region='north',height=27,items=v.items)
            #~ #return py2js(kw)
        #~ kw.update(text=v.label,menu=dict(items=v.items))
        #~ return py2js(kw)
        
    #~ if isinstance(v,menus.MenuItem):
        #~ from lino.lino_site import lino_site
        #~ handler = "function(btn,evt){Lino.do_action(undefined,%r,{})}" % v.actor.get_url(lino_site.ui)
        #~ return py2js(dict(text=v.label,handler=js_code(handler)))
        #~ if v.args:
            #~ handler = "function(btn,evt) {%s.show(btn,evt,%s);}" % (
                #~ id2js(v.actor.actor_id),
                #~ ",".join([py2js(a) for a in v.args]))
        #~ else:
            #~ handler = "function(btn,evt) {%s.show(btn,evt);}" % id2js(v.actor.actor_id)
        #~ return py2js(dict(text=v.label,handler=js_code(handler)))
    #~ assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
    if isinstance(v,Value):
        return v.as_ext()
        
    if type(v) is types.GeneratorType:
        raise Exception("Please don't call the generator function yourself")
        #~ return "\n".join([ln for ln in v])
    if callable(v):
        #~ raise Exception("Please call the function yourself")
        return "\n".join([ln for ln in v()])

    if isinstance(v,js_code):
        return v.s
    if v is None:
        #~ return 'undefined'
        return 'null'
    if isinstance(v,(list,tuple)): # (types.ListType, types.TupleType):
        return "[ %s ]" % ", ".join([py2js(x) for x in v])
    if isinstance(v,dict): # ) is types.DictType:
        #~ print 20100226, repr(v)
        return "{ %s }" % ", ".join([
            "%s: %s" % (key2js(k),py2js(v)) for k,v in v.items()])
    if isinstance(v,bool): # types.BooleanType:
        return str(v).lower()
    if isinstance(v, (int, long)):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    #return simplejson.encoder.encode_basestring(v)
    #print repr(v)
    return simplejson.dumps(v,cls=DjangoJSONEncoder) # http://code.djangoproject.com/ticket/3324
    

"""
The following works only for Python 2.6 and above, which is not available on Lenny.
Siehe auch http://code.google.com/p/lino/wiki/20100215

class LinoJSONEncoder(DjangoJSONEncoder):
    def _iterencode_default(self, o, markers=None):
        if type(o) is types.GeneratorType:
            #~ for ln in o: yield ln+'\n'
            return "\n".join([ln for ln in o])
        if isinstance(o,js_code):
            return o.s
        if isinstance(o,Variable):
            return o.as_ext()
        return super(LinoJSONEncoder, self)._iterencode_default(o,markers)
        #~ for chunk in super(LinoJSONEncoder, self)._iterencode(o,markers):
            #~ yield chunk

    def default(self, o):
      
        if isinstance(o,menus.Menu):
            if o.parent is None:
                return o.items
            return dict(text=o.label,menu=dict(items=o.items))
            
        if isinstance(o,menus.MenuItem):
            from lino.lino_site import lino_site
            url = lino_site.ui.get_action_url(o.actor)
            handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (url,id2js(o.actor.actor_id))
            return dict(text=o.label,handler=js_code(handler))
            
        return super(LinoJSONEncoder, self).default(o)




def py2js(v,**kw):
    # lino.log.debug("py2js(%r,%r)",v,kw)
    if isinstance(v,Variable):
        return v.as_ext(**kw)
    assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
    return simplejson.dumps(v,cls=LinoJSONEncoder) # http://code.djangoproject.com/ticket/3324
    
"""

def key2js(s):
    if isinstance(s,str):
        return s
    return simplejson.dumps(s,cls=DjangoJSONEncoder)
    
def id2js(s):
    return s.replace('.','_')
  
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    #~ def __repr__(self):
        #~ return self.s
  

DECLARE_INLINE = 0
DECLARE_VAR = 1
DECLARE_THIS = 2

class Value(object):
  
    declare_type = DECLARE_INLINE
    value_template = "%s"
    
    def __init__(self,value):
        self.value = value
        
    def js_declare(self):
        return []
    
    def subvars(self):
        return []
            
    #~ def js_before_body(self):
        #~ for v in self.subvars():
            #~ for ln in v.js_before_body():
                #~ yield ln
    def js_body(self):
        for v in self.subvars():
            for ln in v.js_body():
                yield ln
                
    #~ def js_after_body(self):
        #~ for v in self.subvars():
            #~ for ln in v.js_after_body():
                #~ yield ln
        
    def as_ext(self):
        return self.value_template % py2js(self.value)
        
class Variable(Value):
    declare_type = DECLARE_INLINE
    ext_suffix = ''
    name = None
    ext_name = None
    
    def __init__(self,name,value):
        Value.__init__(self,value)
        #~ assert self.declare_type != DECLARE_INLINE
        if name is None:
            self.declare_type = DECLARE_INLINE
        else:
            self.name = name
            self.ext_name = id2js(name) + self.ext_suffix
        
    def js_declare(self):
        yield "// begin js_declare %s" % self
        yield "// declare subvars of %s" % self
        for v in self.subvars():
            for ln in v.js_declare():
                yield ln
        yield "// end declare subvars of %s" % self
        value = '\n'.join(self.js_value())
        if self.declare_type == DECLARE_INLINE:
            pass
        elif self.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (self.ext_name,value)
        elif self.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (self.ext_name,value)
        yield "// end js_declare %s" % self
            
    #~ def js_column_lines(self):
        #~ return []
        
                
    def as_ext(self):
        if self.declare_type == DECLARE_INLINE:
            return '\n'.join(self.js_value())
        if self.declare_type == DECLARE_THIS:
            return "this." + self.ext_name
        return self.ext_name

    def js_value(self):
        yield self.value_template % py2js(self.value)
        
class Component(Variable): 
    
    def __init__(self,name=None,**options):
        Variable.__init__(self,name,options)
        
    def js_value(self):
        value = self.ext_options(**self.value)
        yield self.value_template % py2js(value)
        
    def ext_options(self,**kw):
        kw.update(self.value)
        return kw
        
    def update(self,**kw):
        self.value.update(**kw)
      
class Function(Variable):
  
    def __init__(self,name=None):
        Variable.__init__(self,name,None)
        
    def js_value(self):
        for ln in self.js_render():
            yield ln
        
    
      
class Object(Function):
    def __init__(self,name,params='this'):
        assert isinstance(params,basestring)
        self.params = params
        Function.__init__(self,name)
        
    def js_value(self):
        yield "new " 
        for ln in self.js_render():
            yield "  " + ln
        yield "(" + self.params + ")"
    
      