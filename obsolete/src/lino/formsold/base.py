## Copyright 2005-2006 Luc Saffre 

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


import traceback
from cStringIO import StringIO


from lino.adamo.datatypes import STRING, MEMO
#from lino.misc import jobs
from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
from lino.gendoc.gendoc import GenericDocument

from lino.adamo.exceptions import InvalidRequestError
#from lino.forms import gui

#from lino.forms.progresser import Progresser


class Component(Describable):
    def __init__(self,owner,
                 name=None,label=None,doc=None,
                 enabled=True,
                 weight=0):
        Describable.__init__(self,None,name,label,doc)
        self.owner = owner
        self.weight=weight
        self.enabled=enabled

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
    
    def render(self,doc):
        doc.p(self.getLabel())
        
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
        return self
        
    def click(self):
        "execute the button's handler"
        frm = self.getForm()
        frm.store()
        frm.lastEvent = self
        self.action(*(self._args),**(self._kw))
##         try:
##             self.action(*(self._args),**(self._kw))
##         except InvalidRequestError,e:
##             frm.session.status(str(e))
##         except Exception,e:
##             frm.session.exception(
##                 e,"after clicking '%s' in '%s'" % (
##                 self.getLabel(),frm.getLabel()))

        
    def render(self,doc):
        doc.renderButton(self)

class TextViewer(Component):
    
    def addText(self,v):
        raise NotImplementedError

    

class BaseEntry(Component):

    def getValueForEditor(self):
        "return current value as string"
        v = self.getValue()
        if v is None: return ""
        return self.format(v)

    def setValueFromEditor(self,s):
        "convert the string and store it as raw value"
        if len(s) == 0:
            self.setValue(None)
        else:
            self.setValue(self.parse(s))
            
    def store(self):
        "store data from widget"
        pass
    
    def getValue(self):
        "return current raw value"
        raise NotImplementedError
    
    def setValue(self,v):
        "store raw value"
        raise NotImplementedError
    
    def format(self,v):
        "convert raw value to string"
        raise NotImplementedError

    def render(self,doc):
        doc.renderEntry(self)
    
    def parse(self,s):
        "convert the non-empty string to a raw value"
        raise NotImplementedError
        
class Entry(BaseEntry):
    def __init__(self,owner, name=None, type=None,
                 value=None,
                 *args,**kw):

        Component.__init__(self,owner, name, *args,**kw)
        
        if type is None:
            type = STRING
            
        self._type = type
        
        self.setValue(value)

    def getValue(self):
        return self._value
    
##     def getType(self):
##         return self._type
    
    def format(self,v):
        return self._type.format(self._value)
    
    def parse(self,s):
        return self._type.parse(s)

    def setValue(self,v):
        if v is not None:
            self._type.validate(v)
        self._value = v
        self.refresh()
    def getMinWidth(self):
        return self._type.minWidth
    def getMaxWidth(self):
        return self._type.maxWidth
    def getMinHeight(self):
        return self._type.minHeight
    def getMaxHeight(self):
        return self._type.maxHeight


class DataEntry(BaseEntry):
    
    def __init__(self,frm,col,*args,**kw):
        Component.__init__(self,frm, col.name,*args,**kw)
        self.enabled = col.canWrite(frm.data)
        self.col = col
        
    def setValue(self,v):
        frm = self.getForm()
        self.col.datacol.setCellValue(frm.getLeadRow(),v)
        
    def parse(self,s):
        return self.col.datacol.rowAttr.parse(s)
    
    def format(self,v):
        return self.col.format(v)

##     def getType(self):
##         return self.col.getType()

    def getMaxWidth(self):
        return self.col.datacol.getMaxWidth()
    def getMinWidth(self):
        return self.col.datacol.getMinWidth()
    def getMaxHeight(self):
        return self.col.datacol.getMaxHeight()
    def getMinHeight(self):
        return self.col.datacol.getMinHeight()
    
    def getValue(self):
        frm = self.getForm()
        return self.col.getCellValue(frm.getLeadRow())

    def refresh(self):
        frm = self.getForm()
        self.enabled = self.col.canWrite(frm.getLeadRow())
        #self.refresh()
        

class Label(Component):
    def __init__(self,owner,*args,**kw):
        Component.__init__(self,owner,*args,**kw)

    def render(self,doc):
        doc.renderLabel(self)



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
    
    def addReportItem(self,*args,**kw):
        return self.getForm().session.addReportItem(self,*args,**kw)
    
    def findItem(self,name):
        for mi in self.items:
            if mi.name == name: return mi


class MenuBar(Component):
    
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.menus = []

    def addMenu(self,*args,**kw):
        i = Menu(self.owner,*args,**kw)
        self.menus.append(i)
        return i
    
    def findMenu(self,name):
        for mnu in self.menus:
            if mnu.name == name: return mnu


class ReportMixin:
    # mixin to be used with Component
    def __init__(self,rpt):
        self.rpt = rpt # a Query or a Report
        #assert len(ds._lockedRows) == 0
        self.rpt.beginReport(self)
        
    def setupGoMenu(self):
        pass
        
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
        m.addItem("printRow",
                  label="Print &Row",
                  action=self.printRow,
                  accel="F7")
        m.addItem("printList",
                  label="Print &List",
                  action=self.printList,
                  accel="Shift-F7")
        
        self.setupGoMenu()
        

        m = frm.addMenu("edit",label="&Edit")
        def copy():
            from cStringIO import StringIO
            out = StringIO()
            self.rpt.__xml__(out.write)
            f = frm.session.form("Text Editor")
            f.addEntry(type=MEMO(width=80,height=10),
                       value=out.getvalue())
            f.show()
        
        m.addItem("copy",
                  label="&Copy",
                  action=copy)
        
        #m = frm.addMenu("row",label="&Row")
        if self.rpt.canWrite():
            m.addItem("delete",
                      label="&Delete selected row(s)",
                      action=self.deleteSelectedRows,
                      accel="DEL")
            m.addItem("insert",
                      label="&Insert new row",
                      action=self.insertRow,
                      accel="INS")
            
        self.rpt.setupMenu(self)
        

        def f():
            l = self.getSelectedRows()
            if len(l) == 1:
                s = "Row %d of %d" % (l[0]+1,len(self.rpt))
            else:
                s = "Selected %s of %d rows" % (len(l), len(self.rpt))
                
            frm.session.status(s)
            
        frm.addIdleEvent(f)

    def insertRow(self):
        assert self.rpt.canWrite()
        row = self.rpt.appendRow()
        self.refresh()
    
    def deleteSelectedRows(self):
        assert self.rpt.canWrite()
        if not self.getForm().confirm(
            "Delete %d rows. Are you sure?" % \
            len(self.getSelectedRows())):
            return
        for i in self.getSelectedRows():
            row = self.rpt[i].delete()
        self.refresh()

    def printRow(self):
        #print "printSelectedRows()", self.getSelectedRows()
        #workdir = "c:\\temp"
        #ui = self.getForm()
        #workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import SpreadsheetDocument
        doc = SpreadsheetDocument("printRow")
        for i in self.getSelectedRows():
            row = self.rpt[i]
            row.printRow(doc)
        #outFile = opj(workdir,"raceman_report.sxc")
        doc.save(self.getForm(),showOutput=True)

    def printList(self):
        #ui = self.getForm()
        #workdir = self.getForm().toolkit.app.tempDir
        raise "must rewrite"
        from lino.oogen import SpreadsheetDocument
        doc = SpreadsheetDocument("printList")
        rows = self.getSelectedRows()
        if len(rows) == 1:
            rows = self.rpt
        rpt = doc.report()
        self.rpt.setupReport(rpt)
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
        if i == len(self.rpt):
            raise InvalidRequestError(\
                "you cannot select the after-last row!")
        return self.rpt[i]

    def withCurrentRow(self,meth,*args,**kw):
        r = self.getCurrentRow()
        meth(r,*args,**kw)
        
    def onClose(self):
        self.rpt.onClose()

    def getLineWidth(self):
        return 80
    def getColumnSepWidth(self):
        return 0
                

class DataGrid(ReportMixin,Component,GenericDocument):
    def __init__(self,owner,ds,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        ReportMixin.__init__(self,ds)
        self.choosing = False
        self.chosenRow = None

    def setModeChoosing(self):
        self.choosing = True

    def getChosenRow(self):
        return self.chosenRow
    
    def setChosenRow(self,row):
        self.chosenRow = row
        
    def render(self,doc):
        doc.renderDataGrid(self)
            
    # implements GenericDocument
    def getLineWidth(self):
        return 100


##     def render(self,doc):
##         if self.enabled:
##             doc.report(self.rpt)



def nop(x):
    pass

class DataForm(ReportMixin,Component):
    
    def __init__(self,owner,rpt,afterSkip=nop,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        ReportMixin.__init__(self,rpt)
        self.afterSkip = afterSkip
        self.currentPos = 0

    def skip(self,n):
        #print __name__, n
        if n > 0:
            if self.currentPos + n < len(self.rpt):
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
        

    def setupGoMenu(self):
        frm = self.getForm()
        m = frm.addMenu("go",label="&Go")
        m.addItem("next",
                  label="&Next",
                  accel="PgDn").setHandler(self.skip,1)
        m.addItem("previous",
                  label="&Previous",
                  accel="PgUp").setHandler(self.skip,-1)

    def getStatus(self):
        return "%d/%d" % (self.currentPos,len(self.rpt))
    
        

class Container(Component):
    
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self,owner,*args,**kw):
        Component.__init__(self,owner,*args,**kw)
        self._components = []


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

    def render(self,doc):
        # used by cherrygui. sorry for ugliness.
        for c in self._components:
            c.render(doc)
        

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
        
    # def addEntry(self,name=None,*args,**kw):
    def addEntry(self,*args,**kw):
        frm = self.getForm()
        #e = frm.session.toolkit.entryFactory(frm,name,*args,**kw)
        e = frm.session.toolkit.entryFactory(frm,None,*args,**kw)
        self._components.append(e)
        #if name is not None:
        #    frm.entries.define(name,e)
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
        
    def addNavigator(self,rpt,afterSkip=None,*args,**kw):
        frm = self.getForm()
        e = frm.session.toolkit.navigatorFactory(
            self, rpt,afterSkip,*args,**kw)
        self._components.append(e)
        frm.setMenuController(e)
        
    def addPanel(self,direction,**kw): 
        frm = self.getForm()
        btn = frm.session.toolkit.panelFactory(self,direction,**kw)
        self._components.append(btn)
        return btn
    
    def addVPanel(self,**kw):
        return self.addPanel(self.VERTICAL,**kw)
    def addHPanel(self,**kw):
        return self.addPanel(self.HORIZONTAL,**kw)

    def addViewer(self): 
        frm = self.getForm()
        c = frm.session.toolkit.viewerFactory(self)
        self._components.append(c)
        return c
    
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

    def __init__(self,toolkit,sess,data=None,
                 halign=None, valign=None,
                 *args,**kw):
        Describable.__init__(self,None,*args,**kw)
        MenuContainer.__init__(self)
        self.session=sess
        self.toolkit=toolkit
        self._parent = None # parent
        self.data = data
        #self.entries = AttrDict()
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

    def getLeadRow(self):
        return self.data

    def configure(self,data=None,**kw):
        if data is not None:
            from lino.reports.reports import ReportRow
            assert isinstance(data,ReportRow)
        Describable.configure(self,data=data,**kw)

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

    def setup(self):
        self.setupMenu()

    def show(self,modal=False):
        #self.session.notice("show(%s)",self.getLabel())

        if not self.toolkit.running():
            self.toolkit.run_forever(self.session)
            #if self.app.mainForm == self:
            #    return
            # todo: uergh...

        if self.isShown():
            raise InvalidRequestError("form is already shown")
            
        self.modal = modal
        #self.session.debug("show(modal=%s) %s",modal,self.getLabel())
        self.setup()
        #self.session.toolkit.setupForm(self)
        #self.session.debug(repr(self.mainComp))
        self.mainComp.onShow()
        self.onShow()
        #self.session.setActiveForm(self)
        #self.session.toolkit.onShowForm(self)
        self.toolkit.showForm(self)
        
    
    def refresh(self):
        self.mainComp.refresh()
        self.toolkit.refreshForm(self)
        
    def isShown(self):
        return False
    
    def onIdle(self):
        try:
            for e in self._idleEvents:
                e()
        except Exception,e:
            pass
    
    def onShow(self):
        pass
        
    def onClose(self):
        self.mainComp.onClose()
        for e in self._onClose:
            e()
        
    def close(self):
        if self.isShown():
            self.onClose()
    
    
            
    def validate(self):
        #for e in self.entries:
        for e in self._components:
            msg = e.validate()
            if msg is not None:
                return msg
            
    def render(self,doc):
        self.mainComp.render(doc)
        
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





class AbstractToolkit:
    
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    panelFactory = Panel
    viewerFactory = TextViewer
    dataGridFactory = DataGrid
    #reportGridFactory = ReportGrid
    navigatorFactory = DataForm
    formFactory = Form
    
    #jobFactory=Job
    #progresserFactory=Progresser
    
    def __init__(self):
        self._sessions = []
        self._currentProgresser=None
        
            
    def shutdown(self):
        #self.verbose("Done after %f seconds.",
        #             time.time() - self._started)
##         if sys.platform == "win32":
##             utime, stime, cutime, cstime, elapsed_time = os.times()
##             syscon.verbose("%.2f+%.2f=%.2f seconds used",
##                            utime,stime,utime+stime)
##         else:
##             syscon.verbose( "+".join([str(x) for x in os.times()])
##                           + " seconds used")
        for sess in self._sessions:
            sess.close()

    def setupOptionParser(self,p):
        pass

        
    def critical(self,sess,msg,*args,**kw):
        if msg is not None:
            self.error(sess,msg,*args,**kw)
        sess.close()
        self.stopRunning()

    def createForm(self,sess,*args,**kw):
        return self.formFactory(self,sess,*args,**kw)

    #def onShowForm(self,frm):
    def showForm(self,frm):
        raise NotImplementedError

    def refreshForm(self,frm):
        pass

    def beginProgresser(self,sess,*args,**kw):
        self._currentProgresser=Progresser(self._currentProgresser)
        
    
##     def createJob(self,sess,*args,**kw):
##         job=self.jobFactory()
##         job.init(sess,*args,**kw)
##         return job
    
##     def createProgresser(self,sess,*args,**kw):
##         return self.progresserFactory(sess,*args,**kw)
    
    def openSession(self,sess):
        #app.setToolkit(self)
        #sess.toolkit = self
        assert sess.toolkit is self
        self._sessions.append(sess)
        
    def closeSession(self,sess):
        self._sessions.remove(sess)
        if len(self._sessions) == 0:
            self.stopRunning()
            #if self.consoleForm is not None:
            #    self.consoleForm.close()
        

    def running(self):
        return True
        
    def run_forever(self):
        pass
        #raise NotImplementedError
    
    def run_awhile(self):
        pass
        #raise NotImplementedError

    def stopRunning(self):
        pass
        

##     def main(self,app,argv=None):
##         app.parse_args(argv)
##         self.addSession(sess)
##         self.run_forever()
        


    
class Toolkit(AbstractToolkit):
    
    def __init__(self,console=None):
        AbstractToolkit.__init__(self)
        #self.consoleForm = None
        if console is None:
            from lino.console import syscon
            #console=syscon.getSystemConsole()
            console=syscon.getToolkit()
            #console=CaptureConsole(
            #    verbosity=syscon._syscon._verbosity)
        self.console = console
        # non-overridable forwarding
        for funcname in (
            'debug', 'warning',
            'verbose', 'error',
            'textprinter',
            ):
            setattr(self,funcname,getattr(console,funcname))

    def notice(self,*args,**kw):
        self.message(*args,**kw)
        
    def status(self,*args,**kw):
        # overridable forwarding
        return self.console.status(*args,**kw)


    def onTaskBegin(self,*args,**kw):
        return self.console.onTaskBegin(*args,**kw)
    def onTaskDone(self,*args,**kw):
        return self.console.onTaskDone(*args,**kw)
    def onTaskAbort(self,*args,**kw):
        return self.console.onTaskAbort(*args,**kw)
    def onTaskIncrement(self,*args,**kw):
        return self.console.onTaskIncrement(*args,**kw)
    def onTaskBreathe(self,*args,**kw):
        return self.console.onTaskBreathe(*args,**kw)
    

    def message(self,sess,msg,*args):
        if len(args):
            msg=sess.buildMessage(msg,*args)
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

    def showException(self,sess,e,details=None):
        msg = str(e)
        #msg = e.getMessage()
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
                answers=("&End",
                         "&Ignore",
                         "&Details",
                         "&Send"))
            if i == 0:
                sess.critical(s)
                return
            
            elif i == 1:
                return
            elif i == 2:
                frm = sess.form(label="Details")
                frm.addEntry(type=MEMO,value=s)
                frm.showModal()
                #return
                


    def showReport(self,sess,rpt,**kw):
        frm = sess.form(label=rpt.getTitle(),**kw)
        frm.addDataGrid(rpt)
        frm.show()
        




