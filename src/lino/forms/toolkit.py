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

from lino.misc.descr import Describable
from lino.adamo.datatypes import STRING, MEMO
from lino.console import console # import Application
#from lino.console.session import Session
from lino.gendoc.gendoc import GenericDocument

from lino.forms import VERTICAL, HORIZONTAL,\
     Form, MessageDialog, ConfirmDialog, ReportForm

from lino.forms.forms import Container




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
    
    def setup(self):
        # overridden by toolkit implemetnations
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
    # mixin for Component
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
            #from cStringIO import StringIO
            out = StringIO()
            self.rpt.__xml__(out.write)
            
            class MemoViewer(Form):
                title="Text Editor"
                def setupForm(self):
                    self.addEntry(
                        type=MEMO(width=80,height=10),
                        value=out.getvalue())
                    
            MemoViewer(self).show()
        
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
                
            frm.status(s)
            
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


    def render(self,doc):
        if self.enabled:
            doc.report(self.rpt)



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
    
        

class Panel(Container,Component):
    
    def __init__(self,owner,direction,name=None,*args,**kw):
        assert direction in (VERTICAL,HORIZONTAL)
        if name is None:
            if direction is VERTICAL:
                name = "VPanel"
            else:
                name = "HPanel"
        #Container.__init__(self,name,*args,**kw)
        Component.__init__(self,owner,*args,**kw)
        self.direction = direction
        self._components = []

    def getComponents(self):
        return self._components

    def addComponent(self,c):
        self._components.append(c)
        return c


    




## class Application(console.Application):
    
##     mainForm=None
    
##     def addProgramMenu(self,sess,frm):
##         m = frm.addMenu("system","&Programm")
##         m.addItem("logout",label="&Beenden",action=frm.close)
##         m.addItem("about",label="Inf&o").setHandler(sess.showAbout)

##         def bugdemo(task):
##             for i in range(5,0,-1):
##                 sess.status("%d seconds left",i)
##                 task.increment()
##                 task.sleep()
##             thisWontWork()
            
        
##         m.addItem("bug",label="&Bug demo").setHandler(
##             sess.loop,bugdemo,"Bug demo")
##         #m.addItem(label="show &Console").setHandler(self.showConsole)
##         return m

##     def run(self):
##         frm=self.mainForm(self)
##         frm.show()
##         #self.session.toolkit.showForm(frm)


##     def addSession(self,sess):
##         #sess = self._sessionFactory(self,toolkit,**kw)
##         #sess = Session(toolkit)
##         self._sessions.append(sess)
##         #self.onOpenSession(sess)
##         #return sess

##     def removeSession(self,sess):
##         #self.onCloseSession(sess)
##         self._sessions.remove(sess)

##     def onOpenSession(self,sess):
##         self.showMainForm(sess)

##     def onCloseSession(self,sess):
##         pass


##     def close(self):
##         pass
##         for app in self.apps:
##             #syscon.debug("Killing session %r",sess)
##             app.close()
        
        

class AbstractToolkit:
    
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    panelFactory = Panel
    viewerFactory = TextViewer
    dataGridFactory = DataGrid
    navigatorFactory = DataForm
    #formFactory = Form
    menuBarFactory = MenuBar
    
    #jobFactory=Job
    #progresserFactory=Progresser
    
    def __init__(self):
        self.apps = []
        #self._sessions = []
        #self._currentProgresser=None
        
            
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
        for a in self.apps:
            a.close()


    def startApplication(self,app):
        #sess=Session(self)
        #app=appClass(self)
        app.setToolkit(self)
        self.apps.append(app)
        
    def stopApplication(self,app):
        self.apps.remove(app)
        if len(self.apps) == 0:
            self.stopRunning()
            #if self.consoleForm is not None:
            #    self.consoleForm.close()
    
            

    def setupOptionParser(self,p):
        pass


    def message(self,msg):
        return MessageDialog(self,msg).show()
        
##         frm = sess.form(label="Message")
##         frm.addLabel(msg)
##         frm.addOkButton()
##         frm.showModal()

    def confirm(self,*args,**kw):
        return ConfirmDialog(self,*args,**kw).show()
        
##         frm = sess.form(label="Confirmation",doc=prompt)
##         #frm.addLabel(prompt)
##         p = frm.addPanel(HORIZONTAL)
##         ok = p.addOkButton()
##         cancel = p.addCancelButton()
##         if default == "y":
##             ok.setDefault()
##         else:
##             cancel.setDefault()
##         frm.showModal()
##         return frm.lastEvent == ok



    def decide(self,sess,prompt,answers,
               title="Decision",
               default=0):
        raise "must be converted like message and confirm"
        frm = sess.form(label=title,doc=prompt)
        p = frm.addPanel(HORIZONTAL)
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
        
    
        
    def critical(self,sess,msg,*args,**kw):
        if msg is not None:
            self.error(sess,msg,*args,**kw)
        sess.close()
        self.stopRunning()

##     def createForm(self,sess,*args,**kw):
##         return self.formFactory(self,sess,*args,**kw)

    #def onShowForm(self,frm):
    def showForm(self,frm):
        raise NotImplementedError

    def refreshForm(self,frm):
        pass

##     def beginProgresser(self,sess,*args,**kw):
##         self._currentProgresser=Progresser(self._currentProgresser)
        
    
##     def createJob(self,sess,*args,**kw):
##         job=self.jobFactory()
##         job.init(sess,*args,**kw)
##         return job
    
##     def createProgresser(self,sess,*args,**kw):
##         return self.progresserFactory(sess,*args,**kw)
    
##     def openSession(self,sess):
##         #app.setToolkit(self)
##         #sess.toolkit = self
##         assert sess.toolkit is self
##         self._sessions.append(sess)
        
        

    def running(self):
        return True
        
    def run_forever(self):
        raise NotImplementedError
    
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
            console=syscon.getSystemConsole()
            #console=syscon.getToolkit()
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

        self._activeForm=None

    def setActiveForm(self,frm):
        self._activeForm = frm

    def getActiveForm(self):
        return self._activeForm

        
    def notice(self,app,*args,**kw):
        #assert app.mainForm is not None
        if self._activeForm is not None:
            self._activeForm.status(*args,**kw)
        else: self.message(app,*args,**kw)
        
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
                


    def showReport(self,app,rpt,**kw):
        ReportForm(app,rpt).show()
        #frm = sess.form(label=rpt.getTitle(),**kw)
        #frm.addDataGrid(rpt)
        #frm.show()
        



