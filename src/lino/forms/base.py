## Copyright 2005 Luc Saffre 

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

from lino.adamo.datatypes import STRING
from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict



class Component(Describable):
    def __init__(self,owner,*args,**kw):
        Describable.__init__(self,*args,**kw)
        self.owner = owner
        
class Button(Component):
    def __init__(self,owner,onclick=None,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self._onclick = onclick
        self._args = []
        self._kw = {}

    def setHandler(self,onclick,*args,**kw):
        self._onclick = onclick
        self._args = args
        self._kw = kw

    def setDefault(self):
        self.owner.defaultButton = self
        
    def click(self):
        self.owner.lastEvent = self
        self._onclick(self.owner,*(self._args),**(self._kw))
        


class Entry(Component):
    def __init__(self,owner,type,value=None,*args,**kw):
        Component.__init__(self,owner, *args,**kw)
        self.type = type
        self.value = value

    def get(self):
        return self.value
    
    def set(self,value):
        return self.value 
    


class Label(Component):
    def __init__(self,owner,*args,**kw):
        Component.__init__(self,owner,*args,**kw)

class Container:
    # either a Panel or a Form
    
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self):
        self._components = []

    def getForm(self):
        raise NotImplementedError

    def addLabel(self,label,**kw):
        frm = self.getForm()
        e = frm.labelFactory(self,label=label,**kw)
        self._components.append(e)
        return e
        
    def addEntry(self,name=None,type=None,*args,**kw):
        frm = self.getForm()
        if name is None:
            name = "entry" + str(len(frm.entries)+1)
        if type is None:
            type = STRING
        e = frm.entryFactory(frm,type,name=name,*args,**kw)
        self._components.append(e)
        frm.entries.define(e.name,e)
        return e
        
    def addButton(self,*args,**kw): 
        frm = self.getForm()
        btn = frm.buttonFactory(frm,*args,**kw)
        self._components.append(btn)
        frm.buttons.define(btn.name,btn)
        return btn

    def addPanel(self,direction): 
        frm = self.getForm()
        btn = frm.panelFactory(frm,direction)
        self._components.append(btn)
        return btn

    def addOkButton(self,*args,**kw):
        b = self.addButton(name="ok",
                           label="&OK",
                           onclick=self.getForm().ok)
        b.setDefault()
        return b

    def addCancelButton(self,*args,**kw):
        return self.addButton(name="cancel",
                              label="&Cancel",
                              onclick=self.getForm().cancel)

class Panel(Component,Container):
    def __init__(self,frm,direction,name=None,*args,**kw):
        assert direction in (self.VERTICAL,self.HORIZONTAL)
        if name is None:
            if direction is self.VERTICAL:
                name = "VPanel"
            else:
                name = "HPanel"
        Component.__init__(self,frm,name=name,*args,**kw)
        Container.__init__(self)
        self.direction = direction

    def getForm(self):
        return self.owner
    


## class ContainerForm(Describable,Container):

##     labelFactory = Label
##     entryFactory = Entry
##     buttonFactory = Button
##     panelFactory = Panel

##     def __init__(self,parent=None,*args,**kw):
##         Describable.__init__(self,*args,**kw)
##         Container.__init__(self)
##         self._parent = parent
##         self.entries = AttrDict()
##         self.buttons = AttrDict()
##         self.defaultButton = None
##         self._boxes = []
##         self._menu = None
##         self.lastEvent = None
    
##     def getForm(self):
##         return self

##     def addForm(self,*args,**kw):
##         return self.__class__(self,*args,**kw)
    
##     def show(self):
##         raise NotImplementedError
##     def showModal(self):
##         raise NotImplementedError

##     def ok(self,frm):
##         self.close()

##     def cancel(self,frm):
##         self.close()

    
class Form(Describable):

    labelFactory = Label
    entryFactory = Entry
    buttonFactory = Button
    panelFactory = Panel

    def __init__(self,parent=None,*args,**kw):
        Describable.__init__(self,*args,**kw)
        self._parent = parent
        self.entries = AttrDict()
        self.buttons = AttrDict()
        self.defaultButton = None
        self._boxes = []
        self._menu = None
        self.lastEvent = None
        self.mainComp = self.panelFactory(self,Container.VERTICAL)
        for m in ('addLabel','addEntry','addPanel',
                  'addButton', 'VERTICAL', 'HORIZONTAL',
                  'addOkButton', 'addCancelButton'):
            setattr(self,m,getattr(self.mainComp,m))

    
    def addForm(self,*args,**kw):
        return self.__class__(self,*args,**kw)
    
    def show(self):
        raise NotImplementedError
    def showModal(self):
        raise NotImplementedError

    def ok(self,frm):
        self.close()

    def cancel(self,frm):
        self.close()

    
