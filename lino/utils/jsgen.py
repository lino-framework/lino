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
Example:

>>> class TextField(Component):
...    declare_type = DECLARE_VAR
>>> class Panel(Component):
...    declare_type = DECLARE_VAR
>>> fld1 = TextField(fieldLabel="Field 1",name='fld1',xtype='textfield')
>>> fld2 = TextField(fieldLabel="Field 2",name='fld2',xtype='textfield')
>>> fld3 = TextField(fieldLabel="Field 3",name='fld3',xtype='textfield')
>>> p1 = Panel(title="Panel",name='p1',xtype='panel',items=[fld2,fld3])
>>> main = Component(title="Main",name='main',xtype='form',items=[fld1,p1])
>>> d = dict(main=main,wc=[1,2,3])

>>> for ln in declare_vars(d):
...   print ln
var fld11 = { "fieldLabel": "Field 1", "xtype": "textfield" };
var fld22 = { "fieldLabel": "Field 2", "xtype": "textfield" };
var fld33 = { "fieldLabel": "Field 3", "xtype": "textfield" };
var p14 = { "items": [ fld22, fld33 ], "xtype": "panel", "title": "Panel" };

>>> print py2js(d)
{ "main": { "items": [ fld11, p14 ], "xtype": "form", "title": "Main" }, "wc": [ 1, 2, 3 ] }
  
Another example...

>>> def onReady(name):
...     yield js_line("hello = function() {")
...     yield js_line("console.log(%s)" % py2js("Hello, " + name + "!"))
...     yield js_line("}")
>>> print py2js(onReady("World"))
hello = function() {
console.log("Hello, World!")
}
<BLANKLINE>



"""

import logging
logger = logging.getLogger(__name__)

import types
import datetime
import decimal

#~ from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.utils import simplejson
from django.utils.functional import Promise
from django.utils.encoding import force_unicode


import lino
from lino.utils import IncompleteDate


def dict2js(d):
    return ", ".join(["%s: %s" % (k,py2js(v)) for k,v in d.items()])

CONVERTERS = []

def register_converter(func):
    CONVERTERS.append(func)
    
def declare_vars(v):
    """
    Yield the Javascript lines that declare the passed :class:`Variable` `v`.
    If `v` is a :class:`Component`, `list`, `tuple` or `dict` which contains
    other variables yield also the lines to declare these.
    """
    if isinstance(v,(list,tuple)): 
        for sub in v:
            for ln in declare_vars(sub):
                yield ln
        return
    if isinstance(v,dict): 
        for sub in v.values():
            for ln in declare_vars(sub):
                yield ln
        return
    if isinstance(v,Component): 
        #~ for ln in declare_vars(v.value):
            #~ yield ln
        for sub in v.ext_options().values():
            for ln in declare_vars(sub):
                yield ln
        # DON'T return
    elif isinstance(v,Value): 
        #~ ok = True
        for ln in declare_vars(v.value):
            yield ln
        # DON'T return
    if isinstance(v,Variable):
        if v.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (v.ext_name,'\n'.join(v.js_value())) 
        elif v.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (v.ext_name,'\n'.join(v.js_value())) 


def py2js(v):
    """
    Note that None values are rendered as ``null`` (not ``undefined``.
    """
    #~ logger.debug("py2js(%r)",v)
    for cv in CONVERTERS:
        v = cv(v)
        
    if isinstance(v,Value):
        return v.as_ext()
        #~ v = v.as_ext()
        #~ if not isinstance(v, basestring):
            #~ raise Exception("20120121b %r is of type %s" % (v,type(v)))
        #~ return v
    if isinstance(v,Promise):
        #~ v = force_unicode(v)
        return simplejson.dumps(force_unicode(v))
        
    if isinstance(v,types.GeneratorType): 
        return "".join([py2js(x) for x in v])
        
    #~ if type(v) is types.GeneratorType:
        #~ raise Exception("Please don't call the generator function yourself")
        #~ return "\n".join([ln for ln in v])
    if callable(v):
        #~ print 20120114, repr(v)
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
            #~ "%s: %s" % (key2js(k),py2js(v)) for k,v in v.items()])
            "%s: %s" % (py2js(k),py2js(v)) for k,v in v.items()])
            #~ "%s: %s" % (k,py2js(v)) for k,v in v.items()])
    if isinstance(v,bool): # types.BooleanType:
        return str(v).lower()
    #~ if isinstance(v,CRL):
        #~ return str(v)
    if isinstance(v, (int, long, decimal.Decimal)):
        return str(v)
    if isinstance(v, IncompleteDate):
        return '"%s"' % v.strftime(settings.LINO.date_format_strftime)
        #~ return '"%s"' % v
    if isinstance(v, datetime.datetime):
        """20120120"""
        return '"%s"' % v.strftime(settings.LINO.datetime_format_strftime)
        #~ return '"%s"' % v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, datetime.time):
        return '"%s"' % v.strftime(settings.LINO.time_format_strftime)
    if isinstance(v, datetime.date):
        if v.year < 1900:
            v = IncompleteDate(v)
            return '"%s"' % v.strftime(settings.LINO.date_format_strftime)
        return '"%s"' % v.strftime(settings.LINO.date_format_strftime)
        #~ return 'new Date(%d,%d,%d)' % (v.year,v.month-1,v.day)
        #~ return repr('%d.%d.%d' % (v.day,v.month,v.year))
        #~ return repr(str(v))

    if isinstance(v, float):
        return repr(v)
    #return simplejson.encoder.encode_basestring(v)
    #print repr(v)
    # http://docs.djangoproject.com/en/dev/topics/serialization/
    if not isinstance(v, (str,unicode)):
        raise Exception("20120121 %r is of type %s" % (v,type(v)))
    return simplejson.dumps(v)
    #~ return simplejson.dumps(v,cls=DjangoJSONEncoder) # http://code.djangoproject.com/ticket/3324
    

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
            # from lino.lino_site import lino_site
            # todo: convert
            # url = lino_site.ui.action_url_http(o.actor)
            #handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (url,id2js(o.actor.actor_id))
            return dict(text=o.label,handler=js_code(handler))
            
        return super(LinoJSONEncoder, self).default(o)




def py2js(v,**kw):
    # logger.debug("py2js(%r,%r)",v,kw)
    if isinstance(v,Variable):
        return v.as_ext(**kw)
    assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
    return simplejson.dumps(v,cls=LinoJSONEncoder) # http://code.djangoproject.com/ticket/3324
    
"""

def key2js(s):
    if isinstance(s,str):
        return s
    return simplejson.dumps(s) # ,cls=DjangoJSONEncoder)
    
def id2js(s):
    return s.replace('.','_')
  
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    #~ def __repr__(self):
        #~ return self.s
  
def js_line(s,*args): return js_code(s+'\n',*args)

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
        
        
variable_counter = 0
        
class Variable(Value):
    declare_type = DECLARE_INLINE
    ext_suffix = ''
    name = None
    ext_name = None
    
    def __init__(self,name,value):
        Value.__init__(self,value)
        #~ assert self.declare_type != DECLARE_INLINE
        global variable_counter
        variable_counter += 1
        
        if name is None:
            self.ext_name = "var%s%d" % (self.ext_suffix,variable_counter)
        else:
            self.ext_name = "%s%s%d" % (id2js(name),self.ext_suffix,variable_counter)
            self.name = name
        #~ if name is None:
            #~ assert self.declare_type == DECLARE_INLINE
            #~ #self.name = "unnamed %s" % self.__class__.__name__
        #~ else:
            #~ self.name = name
            #~ self.ext_name = id2js(name) + self.ext_suffix
        #~ self.ext_name = id2js(name) + self.ext_suffix
        
    def __str__(self):
        #~ assert self.name is not None
        return self.ext_name
        
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
        #~ self.update(**self.ext_options())
        
    def js_value(self):
        value = self.ext_options()
        #~ value = self.ext_options(**self.value)
        yield self.value_template % py2js(value)
        
    def ext_options(self,**kw):
        kw.update(self.value)
        return kw
        
    def update(self,**kw):
        self.value.update(**kw)
        
    def remove(self,*keys):
        for k in keys:
            if self.value.has_key(k):
                del self.value[k]
        
    def walk(self):
        items = self.value['items']
        if not isinstance(items,(list,tuple)):
            items = [items]
        for i in items:
            for e in i.walk():
                yield e
      
#~ class Function(Variable):
  
    #~ def __init__(self,name=None):
        #~ Variable.__init__(self,name,None)
        
    #~ def js_value(self):
        #~ for ln in self.js_render():
            #~ yield ln
        
    
      
#~ class Object(Function):
    #~ def __init__(self,name,params='this'):
        #~ assert isinstance(params,basestring)
        #~ self.params = params
        #~ Function.__init__(self,name)
        
    #~ def js_value(self):
        #~ yield "new " 
        #~ for ln in self.js_render():
            #~ yield "  " + ln
        #~ yield "(" + self.params + ")"
    
      
      
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
