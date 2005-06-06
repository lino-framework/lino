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

#import os

import traceback
from cStringIO import StringIO


from lino.adamo.datatypes import STRING, MEMO
from lino.misc import jobs
from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
from lino.misc.jobs import Job


from lino.adamo.exceptions import InvalidRequestError
#from lino.ui import console
#from lino.forms.application import BaseApplication
from lino.forms import gui
from lino.console import syscon

#from lino.console import syscon
#from lino.console.application import Application
#from lino.console.console import CLI
#from lino.console.console import CaptureConsole

class Component(Describable):
    def __init__(self,owner,*args,**kw):
        Describable.__init__(self,None,*args,**kw)
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
    
    def onClose(self):
        pass
    
    def onShow(self):
        pass
    
        
class Button(Component):
    def __init__(self,owner,name=None,action=None,*args,**kw):
        Component.__init__(self,owner,name,*args,**kw)
        self.action = action
        self._args = []
        self._kw = {}

    def setHandler(self,action,*args,**kw):
        "set a handler with optional args and keyword parameters"
        self.action = action
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
            self.action(*(self._args),**(self._kw))
        except InvalidRequestError,e:
            frm.session.status(str(e))
        except Exception,e:
            frm.session.exception(
                e,"after clicking '%s' in '%s'" % (
                self.getLabel(),frm.getLabel()))
        #except Exception,e:
        #    frm.error(str(e))

class TextViewer(Component):
    
    def addText(self,v):
        raise NotImplementedError

    

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
    def __init__(self,owner,name,accel,*args,**kw):
        Button.__init__(self,owner,name,*args,**kw)
        self.accel = accel

class Menu(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.items = []

    def addItem(self,name,accel=None,**kw):
        i = MenuItem(self.owner,name,accel,**kw)
        self.items.append(i)
        return i
    
    def addButton(self,btn,accel=None,**kw):
        kw.setdefault("label",btn.getLabel())
        kw.setdefault("action",btn.action)
        return self.addItem(accel=accel,**kw)
    
    def addLink(self,htdoc,**kw):
        # used by gendoc.html
        kw.setdefault("label",htdoc.title)
        kw.setdefault("action",self.owner.urlto(htdoc))
        return self.addItem(htdoc.name,**kw)

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
        m.addItem("exit",label="&Exit",
                  action=frm.close,
                  accel="ESC")
        m.addItem("refresh",
                  label="&Refresh",
                  action=frm.refresh,
                  accel="Alt-F5")

        def copy():
            from cStringIO import StringIO
            out = StringIO()
            self.ds.__xml__(out.write)
            f = frm.session.form("Text Editor")
            f.addEntry(type=MEMO(width=80,height=10),
                       value=out.getvalue())
            f.show()
        
        
        
        m = frm.addMenu("edit",label="&Edit")
        m.addItem("copy",
                  label="&Copy",
                  action=copy)
        
        m = frm.addMenu("row",label="&Row")
        m.addItem("printRow",
                  label="Print &Row",
                  action=self.printRow,
                  accel="F7")
        m.addItem("printList",
                  label="Print &List",
                  action=self.printList,
                  accel="Shift-F7")
        m.addItem("delete",
                  label="&Delete this row",
                  action=self.deleteSelectedRows,
                  accel="DEL")
        m.addItem("insert",
                  label="&Insert new row",
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
            frm.session.status(s)
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
        #ui = self.getForm()
        #workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import SpreadsheetDocument
        doc = SpreadsheetDocument("printRow")
        for i in self.getSelectedRows():
            row = self.ds[i]
            row.printRow(doc)
        #outFile = opj(workdir,"raceman_report.sxc")
        doc.save(self.getForm(),showOutput=True)

    def printList(self):
        #ui = self.getForm()
        #workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import SpreadsheetDocument
        doc = SpreadsheetDocument("printList")
        rows = self.getSelectedRows()
        if len(rows) == 1:
            rows = self.ds
        rpt = doc.report()
        self.ds.setupReport(rpt)
        rpt.execute(rows)
        #outFile = opj(workdir,self.ds.getName()+".sxc")
        doc.save(self.getForm(),showOutput=True)

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
        
    def onClose(self):
        self.ds.unlock()


class DataGrid(Navigator,Component):
    def __init__(self,owner,ds,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        Navigator.__init__(self,ds)
        self.choosing = False
        self.chosenRow = None

    def setModeChoosing(self):
        self.choosing = True

    def getChosenRow(self):
        return self.chosenRow
    
    def setChosenRow(self,row):
        self.chosenRow = row
        


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
        e = frm.session.toolkit.labelFactory(self,label=label,**kw)
        self._components.append(e)
        return e
        
    def addEntry(self,name=None,*args,**kw):
        frm = self.getForm()
        e = frm.session.toolkit.entryFactory(frm,name,*args,**kw)
        self._components.append(e)
        if name is not None:
            frm.entries.define(name,e)
        return e
    
    def addDataEntry(self,dc,*args,**kw):
        frm = self.getForm()
        e = frm.session.toolkit.dataEntryFactory(frm,dc,*args,**kw)
        self._components.append(e)
        return e

    def addDataGrid(self,ds,name=None,*args,**kw):
        frm = self.getForm()
        e = frm.session.toolkit.dataGridFactory(self,ds,*args,**kw)
        self._components.append(e)
        frm.setMenuController(e)
        if name is not None:
            frm.tables.define(name,e)
        return e
        
    def addNavigator(self,ds,afterSkip=None,*args,**kw):
        frm = self.getForm()
        e = frm.session.toolkit.navigatorFactory(
            self, ds,afterSkip,*args,**kw)
        self._components.append(e)
        frm.setMenuController(e)
        
    def addPanel(self,direction): 
        frm = self.getForm()
        btn = frm.session.toolkit.panelFactory(self,direction)
        self._components.append(btn)
        return btn
    
    def addViewer(self): 
        frm = self.getForm()
        c = frm.session.toolkit.viewerFactory(self)
        self._components.append(c)
        return c
    
    def addVPanel(self):
        return self.addPanel(self.VERTICAL)
    def addHPanel(self):
        return self.addPanel(self.HORIZONTAL)

    def addButton(self,name=None,*args,**kw): 
        frm = self.getForm()
        btn = frm.session.toolkit.buttonFactory(
            frm,name=name,*args,**kw)
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
        
    def onClose(self):
        for c in self._components:
            c.onClose()

    def onShow(self):
        for c in self._components:
            c.onShow()


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


## class GuiProgressBar(jobs.ProgressBar):
    
##     def __init__(self,gui,label=None,**kw):
##         if label is None:
##             label = "Progress Bar"
##         self.frm = gui.form(label=label)
##         self.entry = self.frm.addEntry("progress",
##                                        value="0%",
##                                        enabled=False)
##         jobs.ProgressBar.__init__(self,gui,label=label,**kw)

##     def onInit(self):
##         self.frm.show()
        
## ##     def onDone(self,job):
## ##         self.frm.close()
        
##     def onStatus(self,job):
##         self.onInc(job)
        
        
##     def onInc(self,job):
##         self.entry.setValue(job._status+" "+str(job.pc)+"%")



    

class MenuContainer:
    def __init__(self):
        self.menuBar = None
        self._menuController = None
        
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = MenuBar(self)
        return self.menuBar.addMenu(*args,**kw)

    def setMenuController(self,c):
        if self._menuController is None:
            self._menuController = c
        else:
            self.debug("ignored menuController %s" % str(c))






class Form(Describable,MenuContainer):

    def __init__(self,sess,parent,data=None,
                 halign=None, valign=None,
                 *args,**kw):
        Describable.__init__(self,None,*args,**kw)
        MenuContainer.__init__(self)
        #GUI.__init__(self)
        #assert isinstance(app,Application)
        self.session=sess
        #self.toolkit=sess.toolkit
        #self.app = sess.app
        self._parent = parent
        self.data = data
        self.entries = AttrDict()
        self.buttons = AttrDict()
        self.tables = AttrDict()
        self.defaultButton = None
        self.valign = valign
        self.halign = halign
        self._boxes = []
        self.lastEvent = None
        self.mainComp = sess.toolkit.panelFactory(
            self, Container.VERTICAL)
        self._idleEvents = []
        self._onClose = []
        for m in ('addLabel','addViewer',
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

    def addIdleEvent(self,f):
        self._idleEvents.append(f)

    def addOnClose(self,f):
        self._onClose.append(f)

    def setupMenu(self):
        if self._menuController is not None:
            self._menuController.setupMenu()
            
    def setParent(self,parent):
        assert self._parent is None
        #self._parent = parent

    def show(self,modal=False):
        # overridden by implementors
        self.session.notice("show(%s)",self.getLabel())
    
    def isShown(self):
        raise NotImplementedError
    
    def onIdle(self):
        for e in self._idleEvents:
            e()
    
    def onShow(self):
        self.mainComp.onShow()
        
    def onClose(self):
        self.mainComp.onClose()
        for e in self._onClose:
            e()
        
    def close(self):
        if self.isShown():
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
        #if self.menuBar is not None:
        #    raise "Form with menu cannot be modal!"
        self.show(modal=True)
        return self.lastEvent == self.defaultButton

    def ok(self):
        self.close()

    def cancel(self):
        self.close()






class Toolkit:
    
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    panelFactory = Panel
    viewerFactory = TextViewer
    dataGridFactory = DataGrid
    navigatorFactory = DataNavigator
    formFactory = Form
    jobFactory=Job
    
    def __init__(self,console=None):
        self._sessions = []
        #self.consoleForm = None
        if console is None:
            console=syscon.getSystemConsole()
            #console=CaptureConsole(
            #    verbosity=syscon._syscon._verbosity)
        self.console = console
        # non-overridable forwarding
        for funcname in (
            'debug', 'notice','warning',
            'verbose', 'error','critical',
            'job',
            'report','textprinter',
            ):
            setattr(self,funcname,getattr(console,funcname))

    def status(self,*args,**kw):
        # overridable forwarding
        return self.console.status(self,*args,**kw)


    def onJobRefresh(self,*args,**kw):
        return self.console.onJobRefresh(self,*args,**kw)
    def onJobInit(self,*args,**kw):
        return self.console.onJobInit(self,*args,**kw)
    def onJobDone(self,*args,**kw):
        return self.console.onJobDone(self,*args,**kw)
    def onJobAbort(self,*args,**kw):
        return self.console.onJobAbort(self,*args,**kw)
    
            
   

##     def setApplication(self,app):
##         self.app = app

##     def check(self):
##         if self.app is None:
##             self.app = Application(name="Automagic GUI application")
    

    def unused_setupOptionParser(self,parser):
        self.console.setupOptionParser(parser)
        parser.add_option(
            "--console",
            help="open separate window for console output",
            action="store_true",
            dest="showConsole",
            default=True)
        parser.add_option(
            "--no-console",
            help="no console window",
            action="store_false",
            dest="showConsole")

    def unused_applyOptions(self,options,args):
        self.console.applyOptions(options,args)
        self.showConsole = options.showConsole
    
##     def get OptionParser(self,**kw):
##         parser = self.console.getOptionParser(**kw)
##         parser.add_option(
##             "--console",
##             help="open separate window for console output",
##             action="store_true",
##             dest="showConsole",
##             default=True)
##         parser.add_option(
##             "--no-console",
##             help="no console window",
##             action="store_false",
##             dest="showConsole")
##         return parser

##     def parse_args(self,argv=None,**kw):
##         parser = self.getOptionParser(**kw)
##         (options, args) = parser.parse_args(argv)
##         self.showConsole = options.showConsole
##         return (options, args)
    
        
    def createForm(self,sess,parent,*args,**kw):
        return self.formFactory(sess,parent,*args,**kw)
    
    def addSession(self,sess):
        #app.setToolkit(self)
        sess.toolkit = self
        self._sessions.append(sess)
        
    def init(self):
        
        """ the console window must be visible during
        application.init()"""
        
##         if self.showConsole:
##             if self.consoleForm is None:
##                 self.consoleForm = frm = self._apps[0].form(
##                     None, label="Console",
##                     halign=gui.RIGHT, valign=gui.BOTTOM)
##                 frm.addViewer()
##                 frm.show()
        for sess in self._sessions:
            sess.db.app.showMainForm(sess)
            #for sess in app.startup(self):
            #    app.showMainForm(sess)
            
        #frm = app.getMainForm(self)
        #self.consoleForm.setParent(frm)
        #self.app.setMainForm(frm)
        #frm.show()
        #self.wxctrl.SetTopWindow(frm.wxctrl)
        
    def closeSession(self,sess):
        self._sessions.remove(sess)
        if len(self._sessions) == 0:
            self.stopRunning()
            #if self.consoleForm is not None:
            #    self.consoleForm.close()
        





    def message(self,sess,msg):
        frm = sess.form(label="Message")
        frm.addLabel(msg)
        frm.addOkButton()
        frm.showModal()

    def decide(self,sess,prompt,answers,
               title="Decision",
               default=0):
        frm = sess.form(label=title,doc=prompt)
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
        
    
    def confirm(self,sess,prompt,default="y"):
        frm = sess.form(label="Confirmation",doc=prompt)
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

    def abortRequested(self):
        return False
    
    def isInteractive(self):
        return True

##     def job(self,*args,**kw):
##         return console.job(*args,**kw)

##     def make_progressbar(self,*args,**kw):
##         return ProgressBar(self,*args,**kw)
##         # return GuiProgressBar(self,*args,**kw)

    def showException(self,sess,e,details=None):
        msg = str(e)
        out = StringIO()
        traceback.print_exc(None,out)
        s = out.getvalue()
        del out
        if details is not None:
            msg += "\n" + details
        while True:
            i = sess.decide(
                msg,
                title="Oops, an error occured!",
                answers=("&Raise exception",
                         "&Ignore",
                         "&Details",
                         "&Send"))
            if i == 0:
                raise
            elif i == 1:
                return
            elif i == 2:
                frm = sess.form(label="Details")
                frm.addEntry(type=MEMO,value=s)
                frm.show()
                






    def running(self):
        raise NotImplementedError
        
    def run_forever(self):
        raise NotImplementedError
    
    def run_awhile(self):
        raise NotImplementedError

    def stopRunning(self):
        raise NotImplementedError
        

    def main(self,app,argv=None):
        app.parse_args(argv)
        self.addSession(sess)
        self.run_forever()
        
