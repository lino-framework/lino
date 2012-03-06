# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

This module is deprecated. 
Lino now uses http://www.lxml.de instead.
See :doc:`/blog/2012/0301` and :doc:`/blog/2012/0302`

This is a simplistic method for generating XML strings.

The basic idea is to represent an XML schema in Python code.
Unlike generateDS, we do not read an existing XSD and generate 
Python code from it. With xmlgen you write yourself a Python 
equivalent of an XSD.

Primary design goal is to avoid redundancy and to allow for 
concise code.

There are probably still important lacks. Some known issues:

- to be implemented: structure checking and more validation.
  The current implementation is useful for generating XML destinated 
  to a partner who will himself validate your result and give you 
  feedback.
  
- to be implemented: generate an XSD from an xmlgen tree

- it is not possible to generate XML strings with tags or attributes 
  consisting of non-asci characters

Usage example
-------------

For more concrete examples, see the modules that implement existing XML schemas:

- :mod:`lino.utils.xmlgen.xhtml`
- :mod:`lino.utils.xmlgen.bcss`


Define the equivalent of an XML Schema by creating a set 
of Namespace classes.

>>> class common(Namespace): 
...   prefix = None # hide this namespace
...   class NameType(String):
...       def validate(self):
...           String.validate(self)
...           if len(self.value) < 3:
...               self.badValue("Less than 3 chars long")

>>> class foo(Namespace):
...     url = "http://foobar.baz"
...     class Foo(Container): pass
...     class Bar(Container):
...         class Name(common.NameType): pass
...     class Baz(Bar):
...         class Period(String): pass


So the following instantiation should fail since the name is too short:

>>> node = foo.Foo(foo.Baz.Name("X"))
Traceback (most recent call last):
...
Exception: Bad value 'X' for Name : Less than 3 chars long

Here is a longer name:

>>> node = foo.Foo(foo.Baz.Name("Luc"))

Now we can render it 
using :meth:`Element.tostring()`
(we also say `pretty=True` 
in these examples to make the result more readable):

>>> print node.tostring(True)
<foo:Foo xmlns:foo="http://foobar.baz">
<foo:Name>Luc</foo:Name>
</foo:Foo>

Another node:

>>> node = foo.Foo(foo.Baz(
...   foo.Baz.Name("Luc"),
...   foo.Baz.Period("1968-2011")))

>>> print node.tostring(True)
<foo:Foo xmlns:foo="http://foobar.baz">
<foo:Baz>
<foo:Name>Luc</foo:Name>
<foo:Period>1968-2011</foo:Period>
</foo:Baz>
</foo:Foo>

Specifying a `namespace` to :meth:`Element.tostring()` 
means that the generated XML should consider this 
as the default namespace and 
will look as follows:

>>> print node.tostring(True,namespace=foo)
<Foo xmlns="http://foobar.baz">
<Baz>
<Name>Luc</Name>
<Period>1968-2011</Period>
</Baz>
</Foo>




Older examples
--------------

For example, here is the definition of a SOAP envelope:

>>> class soap(Namespace):
...     url = "http://schemas.xmlsoap.org/soap/envelope/"
...     class Envelope(Container): pass
...     class Body(Container): pass

And here the definition of a :term:`BCSS` connector:

>>> class bcss(Namespace):
...     url = "http://ksz-bcss.fgov.be/connectors/WebServiceConnector"
...     class xmlString(Container): pass
...

Then we instantiate these classes to create our XML tree:

>>> anyBody = bcss.xmlString(CDATA("FooBar")).tostring(pretty=True)
>>> print anyBody
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</bcss:xmlString>

>>> env = soap.Envelope(soap.Body(ANY(anyBody))) 

We render the XML string by calling the :meth:`Element.tostring` 
method on the root element:

>>> print env.tostring(pretty=True)
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body>
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</bcss:xmlString>
</soap:Body>
</soap:Envelope>

Specifying a `namespace` to :meth:`Element.tostring()` 
means that the generated XML should consider this 
as the default namespace and 
will look as follows:

>>> print env.tostring(pretty=True,namespace=soap)
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
<Body>
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</bcss:xmlString>
</Body>
</Envelope>

The prefix of a Namespace is the class's name by default, 
but it is possible to give another value:

>>> soap.set_prefix('foo')
>>> print env.tostring(pretty=True)
<foo:Envelope xmlns:foo="http://schemas.xmlsoap.org/soap/envelope/">
<foo:Body>
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</bcss:xmlString>
</foo:Body>
</foo:Envelope>

Or to hide it:

>>> soap.set_prefix(None)
>>> print env.tostring(pretty=True)
<Envelope>
<Body>
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</bcss:xmlString>
</Body>
</Envelope>


"""

unused = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Body>
<xmlString xmlns="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[FooBar]]>
</xmlString>
</soap:Body>
</soap:Envelope>

"""

import datetime
import types
from xml.dom.minidom import parseString
from lino.utils import isiterable

from django.utils.functional import Promise
from django.utils.encoding import force_unicode


#~ _default_namespace = None

#~ def set_default_namespace(ns):
    #~ """
    #~ Declares the specified namespace as default namespace.
    #~ """
    #~ global _default_namespace
    #~ _default_namespace = ns
    
    


class Writer(object):
#~ class Writer:
    
    def __init__(self,file=None,namespace=None,declare_namespaces=True):
        self._default_namespace = namespace
        self.declare_namespaces = declare_namespaces
        self.file = file
        
    def write(self,s):
        self.file.write(s)
        
    def writeln(self,s):
        self.file.write(s+'\n')
        
    def tostring(self,x):
        oldfile = self.file
        self.file = UniStringIO()
        #~ wr = cls(u)
        self.render(x)
        v = self.file.getvalue()
        self.file = oldfile
        return v
        
    def py2xml(self,value): # ,indent='',addindent='',newl=''
        #~ if isinstance(value,(list,tuple)):
        #~ print "20120223 py2xml(%r)" % value
        if isinstance(value,basestring):
            self.write(value)
        elif isinstance(value,Element):
            #~ print "20120223 %r is a Node" % value
            value.__xml__(self)
        elif isinstance(value,types.GeneratorType):
            for e in value:
                #~ self.write('\n')
                self.py2xml(e)
        elif isiterable(value):
            #~ print "20120223 iterable %r" % type(value)
            for e in value:
                self.py2xml(e)
        elif isinstance(value,Promise):
            self.write(force_unicode(value))
        else:
            #~ raise Exception("20120223 Invalid value %r of type %r, Node is %s" % (value,type(value),Node))
            self.write(str(value))
    render = py2xml





def assert_equivalent(s1,s2,write_diag_files=False):
    if s1 == s2:
        return
    dom1 = parseString(s1)
    dom2 = parseString(s2)
    if dom1 != dom2:
        s1 = s1.replace('><','>\n<')
        s2 = s2.replace('><','>\n<')
        l1 = s1.splitlines()
        l2 = s2.splitlines()
        if l1 == l2 : return
        from difflib import Differ
        d = Differ()
        result = list(d.compare(l1, l2))
        print '\n'.join(result)
        if write_diag_files:
            open('s1.xml','w').write(s1)
            open('s2.xml','w').write(s2)
        raise Exception("XML strings are different")



def quote(x):
    if isinstance(x,int):
        return '"'+str(x)+'"'
    if isinstance(x,bool):
        return '"'+str(x).lower()+'"'
    if isinstance(x,basestring):
        assert not '"' in x
        return '"' + x + '"'
    raise Exception("%s not handled" % str(type(x)))


class UniStringIO:
    def __init__(self,s=u''):
        self.buffer = s
    def write(self,s):
        #self.s += s.encode('utf-8')
        self.buffer += unicode(s)
    def getvalue(self):
        return self.buffer
    def __str__(self):
        return repr(self.buffer)


        
        
        
class Attribute(object):
    def __init__(self,name=None,**kw):
        self.name = name
        
#~ class Node(object):
    #~ def __xml__(self,wr):
        #~ raise NotImplementedError()
    #~ def __str__(self):
        #~ return "%s(%r)" % (self.__class__.__name__,self.data)
    

class ElementMetaClass(type):
    def __new__(meta, classname, bases, classDict):
      
        classDict.setdefault('elementname',classname)
        #~ classDict['allowedAttribs'] = allowedAttribs
        #~ classDict['used_namespaces'] = []
        cls = type.__new__(meta, classname, bases, classDict)
        allowedAttribs = {}
        def collect(cl,to):
            for b in cl.__bases__:
                collect(b,to)
            for k,v in cl.__dict__.items():
                if isinstance(v,Attribute):
                    to[k] = v
        collect(cls,allowedAttribs)                
        for k,v in cls.__dict__.items():
            if isinstance(v,Attribute):
                if not v.name:
                    v.name = k
                allowedAttribs[k] = v
        cls.allowedAttribs = allowedAttribs
        return cls
    
class Element(object):
    __metaclass__ = ElementMetaClass
    elementname = None
    namespace = None
    parent = None
    allowedValues = None
    allowEmptyValue = True
    #~ is_root = False
    #~ default_namespace = None
    #~ used_namespaces = []
    declare_namespaces = False
    
    def __init__(self,value=None,**kw):
        #~ if self.elementname is None:
            #~ self.elementname = self.__class__.__name__
        self._attribs = {}
        self.value = value
        if self.value == '':
            self.value = None
        if self.value is None:
            if not self.allowEmptyValue:
                self.badValue("Empty value not allowed.")
        else:
            self.parse_value()
            self.validate()
        self.update(**kw)
        
    def __str__(self):
        return "%s" % self.__class__.__name__
        
    def parse_value(self):
        """
        Convert self.value from any allowed representation format
        to o Python object of proper type.
        """
        pass
        
    def validate(self):
        """
        Check self.value and raise an exception if necessary.
        """
        if self.allowedValues is not None and not self.value in self.allowedValues:
            self.badValue("Must be one of %s.",self.allowedValues)
        
    def badValue(self,msg,*args,**kw):
        """
        Raise an Exception of style "Bad value X for Y : (your given message)"
        """
        if args:
            msg = msg % args
        if kw:
            msg = msg % kw
        raise Exception("Bad value %r for %s : %s" % (self.value,self,msg))
        

    def update(self,**kw):
        for k,v in kw.items():
            #assert not k in self.defaultAttribs.keys()
            try:
                xmlname = self.allowedAttribs[k]
            except KeyError,e:
                raise Exception(
                    "%s attribute not allowed for %s (%s)." % (
                    repr(k), self.__class__.__name__,self.allowedAttribs))
            self._attribs[k] = v
            
    def __getattr__(self,name):
        try:
            return self._attribs[name]
        except KeyError:
            if self.allowedAttribs.has_key(name):
                return None
            raise AttributeError(
                "%s instance has no attribute '%s'" % (
                self.__class__.__name__, name))
        
    @classmethod
    def set_namespace(self,ns):
        self.namespace = ns
                
    def set_parent(self,p):
        self.parent = p
        
    def get_namespace(self):
        if self.namespace is not None:
            return self.namespace
        if self.parent is not None:
            return self.parent.get_namespace()
        return None
            
    def tag(self,wr):
        ns = self.get_namespace()
        if ns is None or ns.prefix is None or ns == wr._default_namespace:
            return self.elementname
            #~ if self.parent and self.parent.default_namespace != self.namespace:
            #~ if not self.namespace.isdefault:
        return ns.prefix+ ":" + self.elementname
    
    def used_namespaces(self,wr):
        if self.namespace is not None:
            yield self.namespace
            
    def writeAttribs(self,wr):
        #~ if self.parent is None: # it's the root element
        if self.declare_namespaces:
            nss = set()
            if self.namespace and self.namespace.prefix and self.namespace == wr._default_namespace:
                wr.write(' xmlns="%s"' % self.namespace.url)
            for ns in self.used_namespaces(wr):
                if ns.prefix and ns != wr._default_namespace:
                    nss.add(ns)
            for ns in nss:
                wr.write(' xmlns:%s="%s"' % (ns.prefix,ns.url))
        for k,v in self._attribs.items():
            a = self.allowedAttribs.get(k)
            wr.write(' %s=%s' % (a.name,quote(v)))
            
    def __xml__(self,wr):
        #~ print "20120223 Element.__xml__(%r)" % self.value
        wr.write("<" + self.tag(wr))
        if self.parent is None:
            self.declare_namespaces = wr.declare_namespaces
        self.writeAttribs(wr)
        
        if self.value is None:
            wr.write('/>')
        else:
            wr.write('>')
            wr.py2xml(self.value2string(self.value))
            wr.write("</"+self.tag(wr)+">" )
            
    def value2string(self,v):
        return v
        
        
    def tostring(self,pretty=False,**writer_kw):
        """
        Generate and return the XML string.
        """
        u = UniStringIO()
        wr = Writer(u,**writer_kw)
        #~ wr.py2xml(self)
        self.__xml__(wr)
        if pretty:
            return u.getvalue().replace("><",">\n<")
            #~ return parseString(u.getvalue()).toprettyxml()
        return u.getvalue()
        
#~ class Javascript(Element):
    #~ def __xml__(self,wr):
        #~ wr.write("<" + self.tag())
        #~ self.writeAttribs(wr)
        
        #~ if self.value is None:
            #~ wr.write('/>')
        #~ else:
            #~ wr.write('>')
            
            #~ wr.py2xml(self.value2string(self.value))
            #~ wr.write("</"+self.tag()+">" )
    

class ANY(Element):
    def validate(self):
        if not isinstance(self.value,basestring):
            self.badValue("not a string")
        
    def __xml__(self,wr):
        #~ print "20120223 ANY.__xml__(%r)" % self.data
        wr.write(self.value)
    
class CDATA(Element):
    def __xml__(self,wr):
        wr.write("<![CDATA[%s]]>" % self.value)
    
class TEXT(Element):
    def __xml__(self,r):
        r.py2xml(self.value)
        #~ wr.write(self.value)








        
class ContainerMetaClass(ElementMetaClass):
    def __new__(meta, classname, bases, classDict):
      
        if not classDict.has_key('allowedChildren'):
            allowedChildren = []
            for k,v in classDict.items():
                if isinstance(v,type) and issubclass(v,Element):
                    allowedChildren.append(v)
            classDict['allowedChildren'] = allowedChildren
        cls = ElementMetaClass.__new__(meta, classname, bases, classDict)
        return cls


class Container(Element):
    __metaclass__ = ContainerMetaClass
    """
    A Container is an Element whose `value` 
    is the list of the contained elements.
    """
    allowedChildren = None
    
    @classmethod
    def set_namespace(self,ns):
        self.namespace = ns
        for k,v in self.__dict__.items():
            if isinstance(v,type) and issubclass(v,Element):
                v.set_namespace(ns)
                
    def __init__(self,*elements,**attribs):
        #~ self.used_namespaces = []
        #~ if self.namespace is not None:
            #~ self.used_namespaces.append(self.namespace)
        for e in elements:
            if isinstance(e,Element):
                e.set_parent(self)
                #~ if e.namespace is None:
                    #~ for ns in e.used_namespaces:
                        #~ if not ns in self.used_namespaces:
                            #~ self.used_namespaces.append(ns)
        Element.__init__(self,list(elements),**attribs)
        
    def add_child(self,e):
        self.value.append(e)
        e.parent = self
        return e
        
            
    def used_namespaces(self,wr):
        if self.namespace is not None:
            if not self.declare_namespaces or self.namespace != wr._default_namespace:
                yield self.namespace
        for e in self.value:
            if isinstance(e,Element):
                for ns in e.used_namespaces(wr):
                    yield ns
        
    def find_node(self,cl):
        """
        Find the first child of specified class.
        """
        for n in self.value:
            if isinstance(n,cl): 
                return n
        return self.add_child(cl())
        




class NamespaceMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        if classname != 'Namespace':
          
            if not classDict.has_key('prefix'):
                classDict['prefix'] = classname
        
        cls = type.__new__(meta, classname, bases, classDict)
        
        for k,v in classDict.items():
            if isinstance(v,type) and issubclass(v,Element):
                v.set_namespace(cls)
                #~ assert v.namespace is None
                #~ if v.namespace is None:
          
        return cls
  

class Namespace(object):
    prefix = None
    url = None
    __metaclass__ = NamespaceMetaClass
    
    @classmethod
    def set_prefix(cls,prefix):
        cls.prefix = prefix
    

#~ # currently not used:
#~ class xsi(Namespace):
    #~ url = "http://www.w3.org/2001/XMLSchema-instance"
#~ class xsd(Namespace):
    #~ url = "http://www.w3.org/2001/XMLSchema"
    

class String(Element):
    pass
  

class Integer(Element):
  
    def validate(self):
        if not isinstance(self.value,int):
            self.badValue("Not an integer")
        Element.validate(self)
        
    def value2string(self,v):
        return str(v)
        
class DateTime(Element):
  
    def validate(self):
        if not isinstance(self.value,datetime.datetime):
            self.badValue("Not a datetime instance")
        Element.validate(self)
        
    def value2string(self,v):
        return v.strftime("%Y%m%dT%H%M%S")
        
class Date(Element):
    def validate(self):
        if not isinstance(self.value,datetime.date):
            self.badValue("not a datetime.date instance")
        Element.validate(self)
        
    def value2string(self,v):
        return v.strftime("%Y-%m-%d")


      
class EmailAddress(String): pass
  


#~ __all__ = [
    #~ 'Namespace', 
    #~ 'String', 'Integer', 
    #~ 'EmailAddress', 'Date',
    #~ 'CDATA', 'Container', 'Node', 'ANY', 'TEXT'
    #~ 'set_default_namespace',
    #~ 'assert_equivalent' ]

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

