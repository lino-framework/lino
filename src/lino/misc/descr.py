## Copyright Luc Saffre 2003-2005.

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


class Describable:
    """
    This interface is 
    - name should be a possibly valid Python identifier
    - label can be longer, but only one line
    - doc can be more than one line
    """

    def __init__(self,name=None,label=None,doc=None):
        if name is None:
            name = self.__class__.__name__
        self.__dict__['_name'] = name
            
        #if label is None:
        #    label = name
        #    #label = "Unlabeled %s instance" % self.__class__.__name__
        self.__dict__['_label'] = label
        
        if doc is None:
            #   doc = "(No docstring available for " + label+")"
            doc = self.__doc__
        else:
            assert type(doc)==type(""),repr(doc)
        self.__dict__['_doc'] = doc
            
        
    def getLabel(self):
        if self._label is None: return self._name
        return self._label
    
    def setLabel(self,label):
        self.__dict__['_label'] = label

    def getDoc(self):
        return self._doc
    
    def setDoc(self,doc):
        self._doc = doc

    def setName(self,name):
        self._name = name

    def getName(self):
        return self._name 

    def __str__(self):
        if self._name == self.__class__.__name__:
            return self._name
        return self.__class__.__name__ + " " + str(self._name) 

    def __repr__(self):
        return self.__class__.__name__ + " " + str(self._name) 



class Configurable:
    
    def configure(self,**kw):
        "make sure that no new attribute gets created"
        for k,v in kw.items():
            assert self.__dict__.has_key(k)
            self.__dict__[k] = v
            # setattr(self,k,v)
