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
    def setFocus(self):
        pass
        
class Button(Component):
    def __init__(self,owner,onclick=None,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self._onclick = onclick
        self._args = []
        self._kw = {}

    def setHandler(self,onclick,*args,**kw):
        "set a handler with optional args and keyword parameters"
        self._onclick = onclick
        self._args = args
        self._kw = kw

    def setDefault(self):
        "set this button as default button for its form"
        self.owner.defaultButton = self
        
    def click(self):
        "execute the button's handler"
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
        #if name is None:
        #    name = "entry" + str(len(frm.entries)+1)
        if type is None:
            type = STRING
        e = frm.entryFactory(frm,type,name=name,*args,**kw)
        self._components.append(e)
        if name is not None:
            frm.entries.define(name,e)
        return e
        
    def addButton(self,name=None,*args,**kw): 
        frm = self.getForm()
        btn = frm.buttonFactory(frm,name=name,*args,**kw)
        self._components.append(btn)
        if name is not None:
            frm.buttons.define(name,btn)
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
    


class MenuItem(Button):
    def __init__(self,owner,accel=None,*args,**kw):
        Button.__init__(self,owner,*args,**kw)
        self.accel = accel

class Menu(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.items = []

    def addItem(self,*args,**kw):
        i = MenuItem(self.owner,*args,**kw)
        self.items.append(i)
        return i
    
    def addButton(self,btn,accel=None,**kw):
        kw.setdefault("label",btn.getLabel())
        kw.setdefault("onclick",btn._onclick)
        return self.addItem(accel=accel,**kw)

class MenuBar(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.menus = []

    def addMenu(self,*args,**kw):
        i = Menu(self.owner,*args,**kw)
        self.menus.append(i)
        return i

    
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
        self.menuBar = None
        self.lastEvent = None
        self.mainComp = self.panelFactory(self,Container.VERTICAL)
        for m in ('addLabel','addEntry','addPanel',
                  'addButton', 'VERTICAL', 'HORIZONTAL',
                  'addOkButton', 'addCancelButton'):
            setattr(self,m,getattr(self.mainComp,m))

    
    def addForm(self,*args,**kw):
        return self.__class__(self,*args,**kw)
    
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = MenuBar(self)
        return self.menuBar.addMenu(*args,**kw)

    def show(self):
        raise NotImplementedError
    
    def showModal(self):
        self.show(modal=True)
        return self.lastEvent == self.defaultButton
    
    def info(self,msg):
        print msg
    def error(self,msg):
        print msg
        
    def confirm(self,prompt,default="y"):
        frm = self.addForm(label="Confirmation")
        frm.addLabel(prompt)
        p = frm.addPanel(Panel.HORIZONTAL)
        p.addOkButton()
        p.addCancelButton()
        if default == "y":
            frm.buttons.ok.setDefault()
        else:
            frm.buttons.cancel.setDefault()
        frm.showModal()
        return frm.lastEvent == frm.buttons.ok

    def ok(self,frm):
        self.close()

    def cancel(self,frm):
        self.close()

    
