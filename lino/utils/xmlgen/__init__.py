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


#~ def py2str(value):
#~ def py2str(*args):
    #~ raise Exception("20120301 %r" % (args,))

#~ def py2str(elem,value):
    #~ if isinstance(value,int):
        #~ return str(value)
    #~ if isinstance(value,datetime.datetime):
        #~ return value.strftime("%Y%m%dT%H%M%S")
    #~ if isinstance(value,datetime.date):
        #~ return value.strftime("%Y-%m-%d")
    #~ if isinstance(value,IncompleteDate):
        #~ if self.year == 0:
            #~ raise Exception("%s : Year may not be 0" % elem)
        #~ return str(value)
    #~ raise Exception("%s : don't know how to format %r" % (elem,value))
        
    #~ if isinstance(value,basestring):
        #~ return value
    #~ return unicode(value)


TYPEMAP = {
  #~ datetime.datetime: py2str,
  #~ IncompleteDate : lambda e,v : str(v),
  datetime.datetime: lambda e,v : v.strftime("%Y%m%dT%H%M%S"),
  datetime.date: lambda e,v : v.strftime("%Y-%m-%d"),
  int: lambda e,v : str(v),
}


class Namespace(object):
  
    xsd_filename = None
    targetNamespace = None
    used_namespaces = None
    
    def __init__(self,prefix=None,targetNamespace=None,**kw):
        self.prefix = prefix
        if targetNamespace is None and self.xsd_filename:
            tree = etree.parse(self.xsd_filename) 
            root = tree.getroot()
            targetNamespace = str(root.get('targetNamespace'))
        
        if targetNamespace is not None:
            kw.update(namespace=targetNamespace)
            #~ if prefix:
            nsmap = kw.setdefault('nsmap',{})
            nsmap[prefix] = targetNamespace
            self.targetNamespace = targetNamespace
            if self.used_namespaces:
                for ns in self.used_namespaces:
                    nsmap[ns.prefix] = ns.targetNamespace
        kw.setdefault('typemap',TYPEMAP)
        #~ self._element_maker = ElementMaker(namespace=url,nsmap={prefix:url})
        self._element_maker = ElementMaker(**kw)
        self._source_elements = {}
        
    def __getattr__(self,name):
        return self._element_maker.__getattr__(name)
        #~ return self._element_maker(*args,**kw)
        #~ return self._element_maker(name,*args,**kw)

    #~ def define(self,names):
        #~ for name in names.split():
            #~ assert not hasattr(self,name)
            #~ setattr(self,name,getattr(self._element_maker,name))

    def validate_root(self,root):
        self.validate_doc(etree.ElementTree(root))
        
    def validate_doc(self,doc):
        if self.xsd_filename:
            xmlschema_doc = etree.parse(self.xsd_filename)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            xmlschema.assertValid(doc)
        return 
        
        
    def unused_discover_from_xsd(self):
        
        #~ XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
        #~ XSD = "{%s}" % XSD_NAMESPACE
        #~ NSMAP = dict(xsd=XSD_NAMESPACE)

        tree = etree.parse(self.xsd_filename) 
        root = tree.getroot()
        self.targetNamespace = str(root.get('targetNamespace'))
        self.define_names_from(root)
        
    def unused_define_names_from(self,e):
        name = e.get('name',None)
        if name is not None:
            cv = self._source_elements.get(name,None)
            #~ cv = getattr(self,name,None)
            if cv is None:
                setattr(self,name,getattr(self._element_maker,name))
                self._source_elements[name] = e
            else:
                logger.warning(
                  "20120309 %s name %r is already used by %s",
                  e,name,cv)
        
        for ee in e:
            self.define_names_from(ee)
                

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

