## Copyright 2003-2006 Luc Saffre.
## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
This is a replacement for PropertySet in reportlab.lib.styles.py

I rewrote it because I wanted "live inheritance": if, after creation
of a Style I modify the textColor attribute of Style "Normal" to blue,
then the behaviour should be that also all children of "Normal" change
their textColor to blue, except if they assigned themselves an
explicit textColor. This is the main reason for my change.

"""

import types

class PropertySet:

    defaults = {}

    def __init__(self, parent=None, **kw):
        if parent:
              assert issubclass(self.__class__,parent.__class__),\
                        "parent %s must have class %s" \
                        % (self.__class__.__name__,
                            parent.__class__.__name__)
        
        self.__dict__['_parent'] = parent

        """
        20040326 : inherit also defaults from base classes
        """
        assert hasattr(self.__class__,'defaults')
        defaults = self.__class__.defaults
        for bc in self.__class__.__bases__:
            defaults.update(bc.defaults)
                    
            
              
        """Disconnect ListType attributes from parent (or defaults)
        because appending to a child's ListType attribute must leave
        the parent (or defaults) unmodified.
        
        This is necessary because modifying a list is syntactically a
        getattr().
        
        """
        
        for k,v in self.defaults.items():
            if type(v) is types.ListType:
                if not kw.has_key(k):
                    if parent is None:
                        kw[k] = list(v)
                    else:
                        kw[k] = list(getattr(parent,k))
                      
              
        self.__dict__['_props'] = kw
                  
        # self.__dict__['_debug'] = debug
        self.__dict__['_name'] = None

    def __getattr__(self,name):
##          if self._debug:
##              print self.getName() + ".__getattr__(" + name +")"
        try:
            return self.__dict__["_props"][name]
        except KeyError,e:
            pass
          
        if self.__dict__["_parent"] is not None:
            try:
                return getattr(self.__dict__["_parent"],name)
            except KeyError,e:
                pass
        try:
            return self.defaults[name]
        except KeyError,e:
            raise AttributeError, \
                    "%s has no property %s" % (self.getName(), name)

    def __setattr__(self, name, value):
        assert hasattr(self,name),\
                 "invalid property %s for %s" % \
                 (name,self.__class__.__name__)
        self.__dict__["_props"][name] = value
##          if self._debug:
##              print self.getName() + ".__setattr__(" + name \
##                      + "," + repr(value)+")"
        
    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self,key,value):
        return self.__setattr__(key,value)

    def items(self):
        return self._props.items()
    
    def update(self,**kw):
        return self._props.update(kw)
    
    def values(self):
        return self._props.values()

    def listAttrs(self, indent=''):
          print indent + 'name =', self._name
          print indent + 'parent =', self._parent
          keylist = self._props.keys()
          keylist.sort()
          for key in keylist:
                value = self._props.get(key, None)
                print indent + '%s = %s' % (key, value)

    def child(self,**kw):
        # kw["name"]=name
        kw["parent"]=self
        return apply(self.__class__,[],kw)


    def getParent(self):
        return self._parent

    def getName(self):
        if self.hasName():
            return self._name
        return self.__class__.__name__

    
    def setName(self,name):
        self.__dict__['_name'] = name
    
    def hasName(self):
        return self.__dict__['_name'] != None
    
    def __repr__(self):
          return "<%s '%s'>" % ( self.getName(),
                                         self.__class__.__name__)

    def __str__(self):
        s = self.getName()
        if self._parent is None:
            s += " = "
        else:
            s += " = %s + " % self._parent.getName()
            
        return s + str(self._props)


class StyleSheet(PropertySet):
    def items(self):
        return self._props.items()
    
    def values(self):
        return self._props.values()

    def define(self,name,value):
        assert not hasattr(self,name),\
                 "%s has already an attribute %s" % (repr(self),name)
        self.__dict__["_props"][name] = value
        if hasattr(value,'setName'):
            value.setName(name)
    
    def redefine(self,name,value):
        assert hasattr(self,name),\
                 "%s has no attribute %s" % (repr(self),name)
        self.__dict__["_props"][name] = value
        if hasattr(value,'setName'):
            value.setName(name)
    
