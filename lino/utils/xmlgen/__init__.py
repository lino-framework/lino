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
This adds some more luxus to lxml's `E-factory
<http://lxml.de/tutorial.html#the-e-factory>`
and is used by modules 
:mod:`lino.utils.xmlgen.odf`,
:mod:`lino.utils.xmlgen.bcss` or
:mod:`lino.utils.xmlgen.intervat`.

"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import datetime

from lxml import etree
from lxml.builder import ElementMaker # lxml only !


class SimpleException(Exception): 
    """
    An Exception whose string is meant to be 
    understandable by the user.
    """


TYPEMAP = {
  #~ datetime.datetime: py2str,
  #~ IncompleteDate : lambda e,v : str(v),
  datetime.datetime: lambda e,v : v.strftime("%Y%m%dT%H%M%S"),
  datetime.date: lambda e,v : v.strftime("%Y-%m-%d"),
  int: lambda e,v : str(v),
}


class Namespace(object):
    """
    A Namespace is a wrapper around an etree.ElementTree.
    """
    #~ rng_filename = None
    xsd_filename = None
    xsd_tree = None
    targetNamespace = None
    used_namespaces = None
    
    def __init__(self,prefix=None,targetNamespace=None,
          used_namespaces=None,
          validator=None,**kw):
        self.prefix = prefix
        kw.setdefault('typemap',TYPEMAP)
        #~ kw.setdefault('makeelement',self.makeelement)
        nsmap = kw.setdefault('nsmap',{})
        if self.xsd_filename:
            self.xsd_tree = etree.parse(self.xsd_filename) 
        if self.xsd_tree is not None:
            if targetNamespace is None:
                root = self.xsd_tree.getroot()
                targetNamespace = str(root.get('targetNamespace'))
            #~ elif self.rng_filename:
                #~ tree = etree.parse(self.rng_filename) 
                #~ rng = etree.RelaxNG(tree)
                #~ # tree = etree.RelaxNG(file=self.rng_filename)
                #~ e = tree.getroot()
                #~ nsmap.update(e.nsmap)
                #~ # raise Exception("20120310")
            if validator is None:
                validator = etree.XMLSchema(self.xsd_tree)
                
          
        self.validator = validator
        
        if targetNamespace is not None:
            kw.update(namespace=targetNamespace)
            #~ if prefix:
            nsmap[prefix] = targetNamespace
            self.targetNamespace = targetNamespace
        if used_namespaces is not None:
            self.used_namespaces = used_namespaces
        if self.used_namespaces is not None:
            for ns in self.used_namespaces:
                nsmap[ns.prefix] = ns.targetNamespace
        #~ self._element_maker = ElementMaker(namespace=url,nsmap={prefix:url})
        self._element_maker = ElementMaker(**kw)
        self._source_elements = {}
        if self.xsd_tree is not None:
            #~ self.targetNamespace = str(root.get('targetNamespace'))
            #~ root = self.xsd_tree.getroot()
            self.define_names_from(self.xsd_tree.getroot())
        self.setup_namespace()
        
    def setup_namespace(self):
        pass
        
    def makeattribs(self,*args,**kw):
        xkw = dict()
        for k,v in kw.items():
            e = getattr(self,k)()
            xkw[e.tag] = v
        return xkw
        
    def unused_makeelement(self,*args,**kw):
        xkw = dict()
        for k,v in kw.items():
            e = getattr(self,k,None)
            if e is None:
                raise Exception("%s has no name %s" % (self.__class__.__name__,k))
                xkw[k] = v
            else:
                xkw[e().tag] = v
        return etree.Element(*args,**xkw)
        
    
        
    def define_names(self,names):
        for name in names.split():
            iname = name.replace("-","_")
            if self.xsd_tree is None:
                #~ assert not hasattr(self,name)
                if hasattr(self,iname):
                    raise Exception("%s has attribute %s" % (self.__class__.__name__,name))
                setattr(self,iname,getattr(self._element_maker,name))
            else:
                if not hasattr(self,iname):
                    raise Exception("%s has no attribute %s" % (self.__class__.__name__,name))

    def update_attribs(self,root,**kw):
        for k,v in kw.items():
            e = getattr(self,k)()
            #~ e = self.__getattr__(k)()
            root.set(e.tag,v)
        
        
    def define_names_from(self,e):
        name = e.get('name',None)
        if name is not None:
            cv = self._source_elements.get(name,None)
            #~ cv = getattr(self,name,None)
            if cv is None:
                iname = name.replace("-","_")
                setattr(self,iname,getattr(self._element_maker,name))
                self._source_elements[name] = e
            #~ else:
                #~ logger.warning(
                  #~ "20120309 %s name %r is already used by %s",
                  #~ e,name,cv)
        
        for ee in e:
            self.define_names_from(ee)

    #~ def __getattr__(self,name):
        #~ return self._element_maker.__getattr__(name)
        #~ # return self._element_maker(*args,**kw)
        #~ # return self._element_maker(name,*args,**kw)

    def validate_root(self,root):
        self.validate_doc(etree.ElementTree(root))
        
    def validate_doc(self,doc):
        if self.validator is not None:
            self.validator.assertValid(doc)
        
        


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

