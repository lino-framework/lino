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

    def __repr__(self):
        return self.getName()
        
    def setFocus(self):
        pass
    def getForm(self):
        return self.owner.getForm()
    def refresh(self):
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
        self.getForm().defaultButton = self
        
    def click(self):
        "execute the button's handler"
        self.getForm().lastEvent = self
        self._onclick(self.owner,*(self._args),**(self._kw))
        

class Entry(Component):
    def __init__(self,owner, name=None, type=None,
                 enabled=True,
                 value="",
                 *args,**kw):

        Component.__init__(self,owner, name, *args,**kw)
        
        if type is None:
            type = STRING
            
        self._type = type
        
        self.enabled=enabled
        
        self.setValue(value)

    def getValue(self):
        if self._value is None:
            return ""
        return self._type.format(self._value)
    
    def setValue(self,s):
        if len(s) == 0:
            self._value = None
        else:
            self._value = self._type.parse(s)
    

class DataEntry(Component):
    def __init__(self,owner,dc, *args,**kw):
        Component.__init__(self,owner, dc.name, *args,**kw)
        self.enabled = dc.canWrite(None)
        self.dc = dc
        
    def setValue(self,s):
        frm = self.getForm()
        if len(s) == 0:
            self.dc.setCellValue(frm.data,None)
        else:
            v=self.dc.rowAttr.parse(s)
            self.dc.setCellValue(frm.data,v)

    def getValue(self):
        frm = self.getForm()
        v = self.dc.getCellValue(frm.data)
        if v is None:
            return ""
        return self.dc.rowAttr.format(v)

    def refresh(self):
        frm = self.getForm()
        self.enabled = self.dc.canWrite(frm.data)
        
        
        

class Label(Component):
    def __init__(self,owner,*args,**kw):
        Component.__init__(self,owner,*args,**kw)




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



        

class Container(Component):
    
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self,owner,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self._components = []


    def __repr__(self):
        s = Component.__repr__(self)
        for c in self._components:
            s += "\n- " + ("\n  ".join(repr(c).splitlines()))
        s += "\n)"
        return s
    
    def addLabel(self,label,**kw):
        frm = self.getForm()
        e = frm.labelFactory(self,label=label,**kw)
        self._components.append(e)
        return e
        
    def addEntry(self,name,*args,**kw):
        frm = self.getForm()
        e = frm.entryFactory(frm,name,*args,**kw)
        self._components.append(e)
        frm.entries.define(name,e)
        return e
    
    def addDataEntry(self,dc,*args,**kw):
        frm = self.getForm()
        e = frm.dataEntryFactory(frm,dc,*args,**kw)
        self._components.append(e)
        return e

    def addTableEditor(self,ds,name=None,*args,**kw):
        frm = self.getForm()
        e = frm.tableEditorFactory(self,ds,*args,**kw)
        self._components.append(e)
        if name is not None:
            frm.tables.define(name,e)
        
    def addNavigator(self,ds,afterSkip=None,*args,**kw):
        frm = self.getForm()
        e = frm.navigatorFactory(self,ds,afterSkip,*args,**kw)
        self._components.append(e)
        
    def addPanel(self,direction): 
        frm = self.getForm()
        btn = frm.panelFactory(self,direction)
        self._components.append(btn)
        return btn
    
    def addVPanel(self):
        return self.addPanel(self.VERTICAL)
    def addHPanel(self):
        return self.addPanel(self.HORIZONTAL)

    def addButton(self,name=None,*args,**kw): 
        frm = self.getForm()
        btn = frm.buttonFactory(frm,name=name,*args,**kw)
        self._components.append(btn)
        if name is not None:
            frm.buttons.define(name,btn)
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

    def refresh(self):
        for c in self._components:
            c.refresh()
        

class Panel(Container):
    def __init__(self,owner,direction,name=None,*args,**kw):
        assert direction in (self.VERTICAL,self.HORIZONTAL)
        if name is None:
            if direction is self.VERTICAL:
                name = "VPanel"
            else:
                name = "HPanel"
        Container.__init__(self,owner,name,*args,**kw)
        self.direction = direction



class TableEditor(Component):    
    def __init__(self,owner,ds,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self.ds = ds


def nop(x):
    pass

class Navigator(Component):
    def __init__(self,owner,ds,afterSkip=nop,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self.ds = ds
        #if afterSkip is None:
        #    afterSkip = lambda self: self.getForm().refresh()
        self.afterSkip = afterSkip
        self.currentPos = 0

    def skip(self,n):
        #print __name__, n
        if n > 0:
            if self.currentPos + n < len(self.ds):
                self.currentPos += n
                self.afterSkip(self)
                self.getForm().refresh()
        else:
            if self.currentPos + n >= 0:
                self.currentPos += n
                self.afterSkip(self)
                self.getForm().refresh()


        
        

    
class Form(Describable):

    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    panelFactory = Panel
    tableEditorFactory = TableEditor
    navigatorFactory = Navigator

    def __init__(self,parent=None,data=None,*args,**kw):
        Describable.__init__(self,*args,**kw)
        self._parent = parent
        self.data = data
        self.entries = AttrDict()
        self.buttons = AttrDict()
        self.tables = AttrDict()
        self.defaultButton = None
        self._boxes = []
        self.menuBar = None
        self.lastEvent = None
        self.mainComp = self.panelFactory(self,Container.VERTICAL)
        for m in ('addLabel',
                  'addEntry', 'addDataEntry',
                  'addTableEditor','addNavigator',
                  'addPanel','addVPanel','addHPanel',
                  'addButton', 'VERTICAL', 'HORIZONTAL',
                  'addOkButton', 'addCancelButton'):
            setattr(self,m,getattr(self.mainComp,m))
        if self.doc is not None:
            self.addLabel(self.doc)

    def getForm(self):
        return self
    
    def addForm(self,*args,**kw):
        return self.__class__(self,*args,**kw)
    
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = MenuBar(self)
        return self.menuBar.addMenu(*args,**kw)

    def show(self):
        raise NotImplementedError
    
            
    def refresh(self):
        self.mainComp.refresh()
    
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

    
