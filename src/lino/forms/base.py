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

import os
opj = os.path.join

import traceback
from cStringIO import StringIO


from lino.adamo.datatypes import STRING
from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
#from lino import ui #import console

from lino.adamo.exceptions import InvalidRequestError
from lino.ui import console
from lino.forms.application import Application
from lino.misc import jobs



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
    def store(self):
        pass
    
    def beforeClose(self):
        pass
    
        
class Button(Component):
    def __init__(self,owner,action=None,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self._action = action
        self._args = []
        self._kw = {}

    def setHandler(self,action,*args,**kw):
        "set a handler with optional args and keyword parameters"
        self._action = action
        self._args = args
        self._kw = kw

    def setDefault(self):
        "set this button as default button for its form"
        self.getForm().defaultButton = self
        
    def click(self):
        "execute the button's handler"
        frm = self.getForm()
        frm.store()
        frm.lastEvent = self
        try:
            self._action(*(self._args),**(self._kw))
        except InvalidRequestError,e:
            frm.status(str(e))
        except Exception,e:
            frm.showException(e,"after clicking '%s' in '%s'" % (
                self.getLabel(),frm.getLabel()))
        #except Exception,e:
        #    frm.error(str(e))
        

class BaseEntry(Component):

    def getValueForEditor(self):
        "return current value as string"
        v = self.getValue()
        if v is None:
            return ""
        return self.format(v)

    def setValueFromEditor(self,s):
        "convert the string and store it as raw value"
        if len(s) == 0:
            self.setValue(None)
        else:
            self.setValue(self.parse(s))
            
    def store(self):
        "store data from widget"
        raise NotImplementedError
    
    def getValue(self):
        "return current raw value"
        raise NotImplementedError
    
    def setValue(self,v):
        "store raw value"
        raise NotImplementedError
    
    def format(self,v):
        "convert raw value to string"
        raise NotImplementedError
    
    def parse(self,s):
        "convert the non-empty string to a raw value"
        raise NotImplementedError
        
class Entry(BaseEntry):
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
        return self._value
    def getType(self):
        return self._type
    
    def format(self,v):
        return self._type.format(self._value)
    
    def parse(self,s):
        return self._type.parse(s)

    def setValue(self,v):
        self._type.validate(v)
        self._value = v
        self.refresh()


class DataEntry(BaseEntry):
    def __init__(self,owner,dc, *args,**kw):
        Component.__init__(self,owner, dc.name, *args,**kw)
        self.enabled = dc.canWrite(None)
        self.dc = dc
        
    def setValue(self,v):
        frm = self.getForm()
        self.dc.setCellValue(frm.data,v)
        
    def parse(self,s):
        return self.dc.rowAttr.parse(s)
    
    def format(self,v):
        return self.dc.rowAttr.format(v)

    def getType(self):
        return self.dc.rowAttr.getType()
    
    def getValue(self):
        frm = self.getForm()
        return self.dc.getCellValue(frm.data)

    def refresh(self):
        frm = self.getForm()
        self.enabled = self.dc.canWrite(frm.data)
        #self.refresh()
        
        

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
        kw.setdefault("action",btn._action)
        return self.addItem(accel=accel,**kw)

class MenuBar(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.menus = []

    def addMenu(self,*args,**kw):
        i = Menu(self.owner,*args,**kw)
        self.menus.append(i)
        return i


class Navigator:
    # mixin to be used with Component
    def __init__(self,ds):
        self.ds = ds
        #assert len(ds._lockedRows) == 0
        
    def setupMenu(self):
        frm = self.getForm()
        m = frm.addMenu("file",label="&File")
        m.addItem(label="&Exit",
                  action=frm.close,
                  accel="ESC")
        m.addItem(label="&Refresh",
                  action=frm.refresh,
                  accel="Alt-F5")
        
        m = frm.addMenu("row",label="&Row")
        m.addItem(label="Print &Row",
                  action=self.printRow,
                  accel="F7")
        m.addItem(label="Print &List",
                  action=self.printList,
                  accel="Shift-F7")
        m.addItem(label="&Delete this row",
                  action=self.deleteSelectedRows,
                  accel="DEL")
        m.addItem(label="&Insert new row",
                  action=self.insertRow,
                  accel="INS")
        self.ds.getLeadTable().setupMenu(self)

        def f():
            l = self.getSelectedRows()
            if len(l) == 1:
                s = "Row %d of %d" % (l[0]+1,len(self.ds))
            else:
                s = "Selected %s of %d rows" % (len(l), len(self.ds))
                
            #if len(self.ds._lockedRows) > 0:
            #    s += " (%d locked)" % len(self.ds._lockedRows)
            frm.setStatusText(s)
        frm.addIdleEvent(f)

    def deleteSelectedRows(self):
        if not self.getForm().confirm(
            "Delete %d rows. Are you sure?" % \
            len(self.getSelectedRows())):
            return
        for i in self.getSelectedRows():
            row = self.ds[i].delete()
        self.refresh()

    def insertRow(self):
        row = self.ds.appendRow()
        self.refresh()
    
    def printRow(self):
        #print "printSelectedRows()", self.getSelectedRows()
        #workdir = "c:\\temp"
        workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import Document
        doc = Document("printRow")
        for i in self.getSelectedRows():
            row = self.ds[i]
            row.printRow(doc)
        outFile = opj(workdir,"raceman_report.sxc")
        doc.save(outFile,showOutput=True)

    def printList(self):
        workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import Document
        doc = Document("printList")
        rows = self.getSelectedRows()
        if len(rows) == 1:
            rows = self.ds
        rpt = doc.report()
        self.ds.setupReport(rpt)
        rpt.execute(rows)
        outFile = opj(workdir,self.ds.getName()+".sxc")
        doc.save(outFile,showOutput=True)

    def getSelectedRows(self):
        raise NotImplementedError

    def getCurrentRow(self):
        l = self.getSelectedRows()
        if len(l) != 1:
            raise InvalidRequestError("more than one row selected!")
        i = l[0]
        if i == len(self.ds):
            raise InvalidRequestError(\
                "you cannot select the after-last row!")
        return self.ds[i]

    def withCurrentRow(self,meth,*args,**kw):
        r = self.getCurrentRow()
        meth(r,*args,**kw)
        
    def beforeClose(self):
        self.ds.unlock()


class DataGrid(Navigator,Component):    
    def __init__(self,owner,ds,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        Navigator.__init__(self,ds)


def nop(x):
    pass

class DataNavigator(Navigator,Component):
    def __init__(self,owner,ds,afterSkip=nop,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        Navigator.__init__(self,ds)
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


    def getSelectedRows(self):
        return [self.currentPos]
        


        

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
        e = frm.toolkit.labelFactory(self,label=label,**kw)
        self._components.append(e)
        return e
        
    def addEntry(self,name,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.entryFactory(frm,name,*args,**kw)
        self._components.append(e)
        frm.entries.define(name,e)
        return e
    
    def addDataEntry(self,dc,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.dataEntryFactory(frm,dc,*args,**kw)
        self._components.append(e)
        return e

##     def addTextEditor(self,s,*args,**kw):
##         frm = self.getForm()
##         e = frm.toolkit.textEditorFactory(frm,s,*args,**kw)
##         self._components.append(e)
##         return e

    def addDataGrid(self,ds,name=None,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.tableEditorFactory(self,ds,*args,**kw)
        self._components.append(e)
        frm.setMenuController(e)
        if name is not None:
            frm.tables.define(name,e)
        
    def addNavigator(self,ds,afterSkip=None,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.navigatorFactory(self,ds,afterSkip,*args,**kw)
        self._components.append(e)
        frm.setMenuController(e)
        
    def addPanel(self,direction): 
        frm = self.getForm()
        btn = frm.toolkit.panelFactory(self,direction)
        self._components.append(btn)
        return btn
    
    def addVPanel(self):
        return self.addPanel(self.VERTICAL)
    def addHPanel(self):
        return self.addPanel(self.HORIZONTAL)

    def addButton(self,name=None,*args,**kw): 
        frm = self.getForm()
        btn = frm.toolkit.buttonFactory(frm,name=name,*args,**kw)
        self._components.append(btn)
        if name is not None:
            frm.buttons.define(name,btn)
        return btn

    def addOkButton(self,*args,**kw):
        b = self.addButton(name="ok",
                           label="&OK",
                           action=self.getForm().ok)
        b.setDefault()
        return b

    def addCancelButton(self,*args,**kw):
        return self.addButton(name="cancel",
                              label="&Cancel",
                              action=self.getForm().cancel)

    def refresh(self):
        for c in self._components:
            c.refresh()
        
    def store(self):
        for c in self._components:
            c.store()
        
    def beforeClose(self):
        for c in self._components:
            c.beforeClose()


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


class GuiProgressBar(jobs.ProgressBar):
    
    def __init__(self,gui,label=None,**kw):
        if label is None:
            label = "Progress Bar"
        self.frm = gui.form(label=label)
        self.entry = self.frm.addEntry("progress",
                                       value="0%",
                                       enabled=False)
        jobs.ProgressBar.__init__(self,label=label,**kw)

    def onInit(self):
        self.frm.show()
        
    def onDone(self):
        self.frm.close()
        
    def onTitle(self):
        self.onInc()
        
    def onInc(self):
        self.entry.setValue(self._title+" "+str(self.pc)+"%")
        
        

class GUI(console.UI):
    
    def __init__(self):
        console.UI.__init__(self)

    def form(self,*args,**kw):
        raise NotImplementedError
    
    def decide(self,prompt,answers,
               title="Decision",
               default=0):
        frm = self.form(label=title,doc=prompt)
        p = frm.addPanel(Panel.HORIZONTAL)
        buttons = []
        for i in range(len(answers)):
            btn = p.addButton(label=answers[i])
            btn.setHandler(frm.close)
            buttons.append(btn)
        frm.showModal()
        for i in range(len(answers)):
            if frm.lastEvent == buttons[i]:
                return i
        raise "internal error: no button clicked?"
        
    
    def confirm(self,prompt,default="y"):
        frm = self.form(label="Confirmation",doc=prompt)
        #frm.addLabel(prompt)
        p = frm.addPanel(Panel.HORIZONTAL)
        ok = p.addOkButton()
        cancel = p.addCancelButton()
        if default == "y":
            ok.setDefault()
        else:
            cancel.setDefault()
        frm.showModal()
        return frm.lastEvent == ok

    def message(self,msg):
        frm = self.form(label="Message")
        frm.addLabel(msg)
        frm.addOkButton()
        frm.showModal()

    def status(self,msg):
        self.warning(msg)
        
    def warning(self,msg):
        console.warning(msg)

    def verbose(self,msg):
        console.verbose(msg)

    def info(self,msg):
        console.info(msg)

    def error(self,msg):
        console.error(msg)

    def job(self,*args,**kw):
        return console.job(*args,**kw)

##     def make_progressbar(self,*args,**kw):
##         return GuiProgressBar(self,*args,**kw)

    def showAbout(self,app):
        frm = self.form(label="About",doc=app.aboutString())
        frm.addOkButton()
        frm.show()
        
        
    def showDataForm(self,ds,**kw):
        frm = self.form(label=ds.getLabel(),**kw)
        ds.setupForm(frm)
        frm.show()
        
    def showDataGrid(self,ds,**kw):
        #assert isinstance(ds,Datasource)
        frm = self.form(label=ds.getLabel(),**kw)
        frm.addDataGrid(ds)
        frm.show()
        
    def showException(self,e,details=None):
        msg = str(e)
        out = StringIO()
        traceback.print_exc(None,out)
        s = out.getvalue()
        del out
        if details is not None:
            msg += "\n" + details
        #msg += "\nIgnore?"
        #print s
        while True:
            i = self.decide(
                msg,
                answers=("~End","~Ignore","~Details","~Send"))
            if i == 0:
                raise e
            elif i == 1:
                return
            elif i == 2:
                frm = self.form(label="Details")
                frm.addEntry(type=MEMO,value=s)
                frm.show()
                




class Form(Describable,GUI):

    def __init__(self,toolkit,parent,data=None,*args,**kw):
        Describable.__init__(self,*args,**kw)
        GUI.__init__(self)
        self.toolkit = toolkit
        self._parent = parent
        self.data = data
        self.entries = AttrDict()
        self.buttons = AttrDict()
        self.tables = AttrDict()
        self.defaultButton = None
        self._boxes = []
        self.menuBar = None
        self.lastEvent = None
        self.mainComp = toolkit.panelFactory(self,Container.VERTICAL)
        self._menuController = None
        self._idleEvents = []
        for m in ('addLabel',
                  'addEntry', 'addDataEntry',
                  'addDataGrid','addNavigator',
                  'addPanel','addVPanel','addHPanel',
                  'addButton', 'VERTICAL', 'HORIZONTAL',
                  'addOkButton', 'addCancelButton'):
            setattr(self,m,getattr(self.mainComp,m))
        if self.doc is not None:
            self.addLabel(self.doc)

    def getForm(self):
        return self

    def setMenuController(self,c):
        if self._menuController is None:
            self._menuController = c
        else:
            console.debug("ignored menuController %s" % str(c))

    def addIdleEvent(self,f):
        self._idleEvents.append(f)

    def setupMenu(self):
        if self._menuController is not None:
            self._menuController.setupMenu()
    
    def form(self,*args,**kw):
        "create a form with this as parent"
        return self.toolkit.form(self,*args,**kw)
    
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = MenuBar(self)
        return self.menuBar.addMenu(*args,**kw)

    def show(self,modal=False):
        raise NotImplementedError
    
    def onIdle(self):
        for e in self._idleEvents:
            e()
    
    def onClose(self):
        self.mainComp.beforeClose()
        
    def close(self):
        self.onClose()
    
    
            
    def validate(self):
        for e in self.entries:
            msg = e.validate()
            if msg is not None:
                return msg
            
    def refresh(self):
        self.mainComp.refresh()
        
    def store(self):
        self.mainComp.store()

    def showModal(self):
        if self.menuBar is not None:
            raise "Form with menu cannot be modal!"
        self.show(modal=True)
        return self.lastEvent == self.defaultButton

    def ok(self):
        self.close()

    def cancel(self):
        self.close()

##     def info(self,msg):
##         #print msg
##         self.setMessage(msg)
##     def error(self,msg):
##         self.warning(msg)
##         #print msg



class Toolkit(GUI):
    
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    #textEditorFactory = TextEditor
    buttonFactory = Button
    panelFactory = Panel
    tableEditorFactory = DataGrid
    navigatorFactory = DataNavigator
    formFactory = Form
    

    
    def __init__(self,app=None):
        self.app = app
        GUI.__init__(self)

    def setApplication(self,app):
        self.app = app

    def check(self):
        if self.app is None:
            self.app = Application(name="Automagic GUI application")
    
    def getOptionParser(self,**kw):
        self.check()
        return self.app.getOptionParser(**kw)

    def parse_args(self,argv=None,**kw):
        parser = self.getOptionParser(**kw)
        return parser.parse_args(argv)
        

    def form(self,parent=None,*args,**kw):
        self.check()
        frm = self.formFactory(self,parent,*args,**kw)
        if parent is None:
            if self.app.mainForm is None:
                self.app.setMainForm(frm)
        return frm
    

    def main(self):
        raise NotImplementedError
        #frm = self.app.getMainForm()
        #frm.show()

        

