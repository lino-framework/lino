## Copyright 2003-2005 Luc Saffre

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


def setdefaults(d,f):
    for k,v in f.items():
        d.setdefault(k,v)

class Configurable:
    
##     def __init__(self,*args,**kw):
##         self.configure(*args,**kw)

    def configure(self,**kw):
        "make sure that no new attribute gets created"
        for k,v in kw.items():
            assert self.__dict__.has_key(k), \
                   "invalid keyword "+k
            self.__dict__[k] = v
            # setattr(self,k,v)


class Describable(Configurable):

    def __init__(self,parent=None,name=None,label=None,doc=None):
        
        if name is None:
            if parent is None:
                name=self.__class__.__name__
            else:
                name=parent.name+'+'
        else:
            assert not " " in name
            
        if parent is not None:
            assert isinstance(parent,self.__class__)
            if label is None:
                label=parent.label
            if doc is None:
                label=parent.doc
            
        # place them directly to __dict__ in case that __setattr__ is
        # also defined
        
        self.__dict__['name'] = name
        self.__dict__['label'] = label
        self.__dict__['doc'] = doc

    def child(self,*args,**kw):
        return self.__class__(self,*args,**kw)
            
        
    def getLabel(self):
        if self.label is None: return self.name
        return self.label

    def hasLabel(self):
        return (self.label is not None)
    
    def setLabel(self,label):
        self.__dict__['label'] = label

    def getDoc(self):
        return self.doc
    
    def setDoc(self,doc):
        self.doc = doc

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name 

    def __str__(self):
        if self.name.startswith(self.__class__.__name__):
            return self.name
        return self.__class__.__name__ + " " + str(self.name) 

    def __repr__(self):
        return self.__class__.__name__ + " " + str(self.name) 



