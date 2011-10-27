# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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
        
class ElementMetaClass(type):
    def __new__(meta, classname, bases, classDict):
      
        allowedAttribs = {}
        for k,v in classDict.items():
            if isinstance(v,Attribute):
                if not v.name:
                    v.name = k
                allowedAttribs[k] = v
        classDict['allowedAttribs'] = allowedAttribs
        cls = type.__new__(meta, classname, bases, classDict)
        return cls
    
    
class Element(object):
    __metaclass__ = ElementMetaClass
    elementname = None
    namespace = None
    
    def __init__(self,value=None,**kw):
        if self.elementname is None:
            self.elementname = self.__class__.__name__
        self.value = value
        self._attribs = {}
        self.update(**kw)

    def update(self,**kw):
        for k,v in kw.items():
            #assert not k in self.defaultAttribs.keys()
            try:
                xmlname = self.allowedAttribs[k]
            except KeyError,e:
                raise Exception(
                    "%s attribute not allowed for %s" % (
                    repr(k), self.__class__.__name__))
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
    def add_namespace(self,ns):
        if self.namespace:
            raise Exception("Element %s got duplicate namespace %r" % (
              self.__name__,ns.__name__))
        self.namespace = ns
        
    def tag(self):
        if not self.namespace.isdefault:
            return self.namespace.__name__+ ":" + self.elementname
        return self.elementname
    
    def writeAttribs(self,wr):
        for k,v in self._attribs.items():
            a = self.allowedAttribs.get(k)
            wr.write(' %s=%s' % (a.name,quote(v)))
            
    def __xml__(self,wr):
        wr.write("<" + self.tag())
        self.writeAttribs(wr)
        
        if self.value is None:
            wr.write('/>')
        else:
            wr.write('>')
            py2xml(wr,self.value)
            wr.write("</"+self.tag()+">" )
        
        
    def toxml(self):
        u = UniStringIO()
        self.__xml__(u)
        return u.getvalue()
        
def py2xml(wr,value): # ,indent='',addindent='',newl=''
    if isinstance(value,(list,tuple)):
        for e in value:
            py2xml(wr,e)
    elif isinstance(value,Element):
        value.__xml__(wr)
    else:
        wr.write(value)

class ContainerMetaClass(ElementMetaClass):
    def __new__(meta, classname, bases, classDict):
      
        allowedValues = {}
        for k,v in classDict.items():
            if isinstance(v,type) and issubclass(v,Element):
                allowedValues[k] = v
        classDict['allowedValues'] = allowedValues
        classDict['used_namespaces'] = []
        cls = ElementMetaClass.__new__(meta, classname, bases, classDict)
        return cls


class Container(Element):
    __metaclass__ = ContainerMetaClass
    """
    A Container is an Element whose `value` 
    is the list of the contained elements.
    """
    def __init__(self,*elements,**attribs):
        # note the '*'
        Element.__init__(self,elements,**attribs)
        
    #~ def __xml__(self,wr):
        #~ wr("<" + self.tag())
        #~ self.writeAttribs(wr)
        
        #~ if len(self.value) == 0:
            #~ wr('/>')
        #~ else:
            #~ wr('>')
            #~ for e in self.value:
                #~ e.__xml__(wr)
            #~ wr("</"+self.tag()+">" )





class RootContainer(Container):
  
    #~ used_namespaces = []
    default_namespace = None
    
    @classmethod
    def add_namespace(self,ns):
        super(RootContainer,self).add_namespace(ns)
        if ns.isdefault:
            self.default_namespace = ns
        elif not ns in self.used_namespaces:
            self.used_namespaces.append(ns)
            
    def writeAttribs(self,wr):
        if self.default_namespace:
            wr.write(' xmlns="%s"' % self.default_namespace.url)
        for ns in self.used_namespaces:
            wr.write(' xmlns:%s="%s"' % (ns.__name__,ns.url))
        for k,v in self._attribs.items():
            a = self.allowedAttribs.get(k)
            wr.write(' %s=%s' % (a.name,quote(v)))
        super(RootContainer,self).writeAttribs(wr)
  
class String(Element): pass
class EmailAddress(String): pass
  





def extract_containers(ns,d,add):
    for k,v in d.items():
        if isinstance(v,type) and issubclass(v,Element):
            if add:
                assert not ns.has_key(k)
                ns[k] = v
            extract_containers(ns,v.__dict__,True)
                
    
class NamespaceMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        ns = {}
        extract_containers(ns,classDict,False)
        
        for k,v in ns.items():
            if classDict.has_key(k):
                raise Exception("Duplicate name %r in Namespace %r" % (k,classname))
            classDict[k] = v
        
        cls = type.__new__(meta, classname, bases, classDict)
        
        for k,v in classDict.items():
            if isinstance(v,type) and issubclass(v,Element):
                v.add_namespace(cls)
          
                
        return cls
  

class Namespace(object):
    isdefault = False
    url = None
    __metaclass__ = NamespaceMetaClass
    
        
        

 
