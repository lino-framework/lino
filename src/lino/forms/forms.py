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



from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
from lino.gendoc.gendoc import GenericDocument

from lino.adamo.exceptions import InvalidRequestError
from lino.forms import gui
from lino.forms import keyboard
from lino.console.task import BugDemo
from lino.adamo.dbreports import QueryReport

VERTICAL = 1
HORIZONTAL = 2

YES=True
NO=False


class MenuContainer:
    # also used by gendoc.html.HtmlDocument
    def __init__(self):
        self.menuBar = None
        self._menuController = None
        
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = self.toolkit.menuBarFactory(
                self)
        return self.menuBar.addMenu(*args,**kw)

    def setMenuController(self,c):
        if self._menuController is None:
            self._menuController = c
        else:
            self.debug("ignored menuController %s" % str(c))

##     def setupMenu(self):
##         if self._menuController is not None:
##             self._menuController.setupMenu()
            


class Form(MenuContainer):
    
    title=None
    modal=False
    #doc=None
    returnValue=None
    enabled=True
    
    def __init__(self,
                 #data=None,
                 halign=None, valign=None,
                 title=None,
                 enabled=None): # *args,**kw):
        #if self.title is None:
        #Describable.__init__(self,None,*args,**kw)
        #assert isinstance(app,Application)
        #assert app.mainForm is not None
        MenuContainer.__init__(self)
        #self.app=app
        if title is not None:
            self.title=title
        if enabled is not None:
            self.enabled=enabled
        #self.session=sess
        self.accelerators=[]
        self._parent = None
        #self.data = data
        #self.entries = AttrDict()
        #self.buttons = AttrDict()
        #self.tables = AttrDict()
        self.defaultButton = None
        self.valign = valign
        self.halign = halign
        self._boxes = []
        self.lastEvent = None
        self.ctrl=None
        self.session=None
        self.mainComp=None


    def setup(self,sess):
        if self.ctrl is not None:
            raise InvalidRequestError("cannot setup() again")
        if self.session is not None:
            assert self.session is sess
        #assert not isinstance(sess,Toolkit)
        self.session=sess
        self.toolkit=sess.toolkit
        self.mainComp = sess.toolkit.vpanelFactory(self,weight=1)
            
        if self.__doc__ is not None:
            self.mainComp.label(self.__doc__)
            
        self.layout(self.mainComp)
        self.setupMenu()
        self.mainComp.setup()
        self.ctrl = self.toolkit.createFormCtrl(self)
        self.onShow()


    def __repr__(self):
        s = self.__class__.__name__
        s += '(title=%r)' % self.getTitle()
        s += ":\n"
        s += "\n  ".join(repr(self.mainComp).splitlines())
        #s += "\n)"
        return s
    
    
    def addAccelerator(self,hotkey,btn):
        self.accelerators.append((hotkey,btn))
        
        
##     def getComponents(self):
##         # implements Container
##         assert self.mainComp is not None, \
##                "Form %s was not setup()" % self.getTitle()
##         return ( self.mainComp, )

##     def addComponent(self,c):
##         # implements Container
##         return self.mainComp.addComponent(c)
        
    def getTitle(self):
        # may override to provide dynamic title
        assert self.title is not None,\
               "%s.title is None and getTitle() not defined" \
               % self.__class__
        return self.title

##     def configure(self,data=None,**kw):
##         if data is not None:
##             from lino.reports.reports import ReportRow
##             assert isinstance(data,ReportRow)
##         Describable.configure(self,data=data,**kw)

##     def getForm(self):
##         return self


##     def setupForm(self):
##         raise "replaced by layout()"

    def layout(self,panel):
        pass

    def setupMenu(self):
        pass
            
    def set_parent(self,parent):
        #assert self._parent is None
        self._parent = parent

    def isShown(self):
        #return hasattr(self,'ctrl')
        return (self.ctrl is not None)

    def show(self):
        #assert not self.isShown(), \
        #       "Form %s already isShown()" % self.getTitle()
        self.toolkit.executeShow(self)
        return self.returnValue
        
    
    def onShow(self): self.mainComp.onShow()
    def store(self): self.mainComp.store()        
    def onClose(self): self.mainComp.onClose()
        
    def refresh(self):
        self.mainComp.refresh()
        self.toolkit.executeRefresh(self)
        
    def onIdle(self,evt):
        pass
    
    def onKillFocus(self,evt):
        self.toolkit.setActiveForm(self._parent)
        
    def onSetFocus(self,evt):
        self.toolkit.setActiveForm(self)

    def ok(self):
        self.close()
        
    def close(self,evt=None):
        #if not self.isShown(): return
        #self.mainComp.onClose()
        self.onClose()
        self.toolkit.closeForm(self,evt)
        self.ctrl=None
        #self.session=None
    
    # just forward to self.session:
    def showForm(self,frm):
        frm.set_parent(self)
        return self.session.showForm(frm)
    def notice(self,*args,**kw):
        return self.session.notice(*args,**kw)
    def message(self,*args,**kw):
        return self.session.message(*args,**kw)
    def confirm(self,*args,**kw):
        return self.session.confirm(*args,**kw)

    def main(self,*args,**kw):
        app=gui.GuiApplication(self)
        app.main(*args,**kw)

##     def show(self):
##         assert self.session is None
##         return gui.getRoot().showForm(self)
        
        
##     def __xml__(self,xml):
##         xml.begin_tag("form",title=self.getTitle())
##         xml.end_tag("form")
        
    
##         for c in self.getComponents():
            
##     def render(self,doc):
##         self.mainComp.render(doc)
        
##     def store(self):
##         self.mainComp.store()

##     def showModal(self):
##         #if self.menuBar is not None:
##         #    raise "Form with menu cannot be modal!"
##         self.show(modal=True)
##         return self.lastEvent == self.defaultButton


class MemoViewer(Form):
    title="Text Editor"
    def __init__(self,txt,**kw):
        self.txt=txt
        Form.__init__(self,**kw)
                    
    def layout(self,add):
        add.entry(
            type=MEMO(width=80,height=10),
            value=self.txt)
                    
class ReportForm(Form,GenericDocument):
    # used by ReportRowForm and ReportGridForm
    def __init__(self,rpt,**kw):
        Form.__init__(self,**kw)
        self.rpt=rpt
        self.rpt.beginReport()
        self.currentRow=None

    def beforeRowEdit(self):
        #print "beforeRowEdit()",repr(self.currentRow)
        #self.currentRow=self.getCurrentRow()
        if self.currentRow is None: return
        if self.isEditing():
            self.currentRow.item.lock()
            
    def afterRowEdit(self):
        if self.currentRow is None: return
        #print "afterRowEdit()",repr(self.currentRow.item)
        if self.currentRow.item.isLocked():
            self.store()
            self.currentRow.item.unlock()


    def getCurrentRow(self):
        #return self.rpt[self.recno]        
        return self.currentRow
        #if self.recno is None:
        #    return None
        #return self.rpt[self.recno]

    def setCurrentRow(self,row):
        self.afterRowEdit()
        self.currentRow=row
        self.beforeRowEdit()


    def isEditing(self):
        return False
            
    def setupMenu(self):
        self.setupFileMenu()
        self.setupEditMenu()
        self.rpt.setupMenu(self)
        
    def setupFileMenu(self):
        m = self.addMenu("file",label="&File")
        m.addItem("exit",label="&Exit",
                  action=self.close,
                  hotkey=keyboard.ESCAPE) # accel="ESC")
        m.addItem("refresh",
                  label="&Refresh",
                  action=self.refresh,
                  hotkey=keyboard.ALT_F5) # accel="Alt-F5")
        m.addItem("printRow",
                  label="Print &Row",
                  action=self.printRow,
                  hotkey=keyboard.F7) # accel="F7")
        m.addItem("printList",
                  label="Print &List",
                  action=self.printList,
                  hotkey=keyboard.SHIFT_F7) #accel="Shift-F7")
        return m
        

    def setupEditMenu(self):
        m = self.addMenu("edit",label="&Edit")
        def copy():
            #from cStringIO import StringIO
            out = StringIO()
            self.rpt.__xml__(out.write)
            self.showForm(MemoViewer(out.getvalue()))
        
        m.addItem("copy",
                  label="&Copy",
                  action=copy,
                  hotkey=keyboard.CTRL_C) # accel="Ctrl-C")
        
        #m = frm.addMenu("row",label="&Row")
        if self.rpt.canWrite():
            m.addItem("pickCellValue",
                      label="&Pick cell value...",
                      action=self.pickCellValue,
                      hotkey=keyboard.F1) # accel="F1")
            m.addItem("editCellValue",
                      label="&Edit cell value",
                      action=self.editCellValue,
                      hotkey=keyboard.F2) # accel="F2")
            m.addItem("delete",
                      label="&Delete selected row(s)",
                      action=self.deleteSelectedRows,
                      hotkey=keyboard.DELETE) # accel="DEL")
            m.addItem("insert",
                      label="&Insert new row",
                      action=self.insertRow,
                      hotkey=keyboard.INSERT) # accel="INS")
        return m

    def editCellValue(self):
        print self.__class__.__name__+".editCell() not yet implemented"

    
    def pickCellValue(self):
        #self.beforeRowEdit()
        col=self.getSelectedCol()
        row=self.getCurrentRow()
        if row is None:
            return
        #value=col.getCellValue(row)
        allowedValues=col.datacol.getAllowedValues(row.item)
        if allowedValues is None:
            return
        rpt=QueryReport(allowedValues)
        #print value
        #print allowedValues
        #rpt.show()
        def onpick(pickedRow):
            #print 1, row.item
            row.lock()
            #print 2, row.item
            col.setCellValue(row,pickedRow.item)
            #print 3, row.item
            row.unlock()
            #print 4, row.item
            self.refresh()
            #print 5, row.item
            
        self.showForm(ReportGridPickForm(rpt,onpick))
        #self.afterRowEdit()
        #self.refresh()

    #def setupGoMenu(self):
    #    pass

    def getTitle(self):
        if self.title is not None: return self.title
        return self.rpt.getTitle()


##     def insertRow(self):
##         assert self.rpt.canWrite()
##         row = self.rpt.appendRow()
##         self.refresh()

##     def goto(self,recno):
##         if recno == len(self.rpt):
##             self.insertRow()
##         else:
##             self.setCurrentRow(self.rpt[recno])
    


    def insertRow(self):
        assert self.rpt.canWrite()
        self.afterRowEdit()
        self.enabled=True
        item=self.rpt.query._appendRow()
        self.currentRow=self.rpt.processItem(item)
        self.onInsertRow()
        #row.item.commit()
        #self.rpt.query._store.fireUpdate()
        self.beforeRowEdit()
        self.refresh()
        #return row.item
    
##     def updateRow(self,row,*args):
##         i = 0
##         for col in self.columns:
##             if i == len(args):
##                 break
##             col.setCellValue(row,args[i])
##             #row._values[col.rowAttr._name] = args[i]
##             i += 1

##     def appendRowForEditing(self,*args):
##         item=self.query._appendRow()
##         row=ReportRow(self,item)
##         self.updateRow(row,*args)
##         return row
            
##     def appendRow(self,*args):
##         row=self.appendRowForEditing(*args)
##         row.item.commit()
##         self.query._store.fireUpdate()
##         return row.item
    
            
        
    
    def deleteSelectedRows(self):
        assert self.rpt.canWrite()
        if not self.session.confirm(
            "Delete %d rows. Are you sure?" % \
            len(self.grid.getSelectedRows())):
            return
        for i in self.grid.getSelectedRows():
            row = self.rpt[i].item.delete()
        self.refresh()

    def printRow(self):
        #print "printSelectedRows()", self.getSelectedRows()
        #workdir = "c:\\temp"
        #ui = self.getForm()
        #workdir = self.getForm().toolkit.app.tempDir
        from lino.oogen import SpreadsheetDocument
        doc = SpreadsheetDocument("printRow")
        for i in self.grid.getSelectedRows():
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
        rows = self.grid.getSelectedRows()
        if len(rows) == 1:
            rows = self.rpt
        rpt = doc.report()
        self.rpt.setupReport(rpt)
        rpt.execute(rows)
        #outFile = opj(workdir,self.ds.getName()+".sxc")
        doc.save(self,showOutput=True)

    def onClose(self):
        self.rpt.endReport()
        #self.rpt.query.getContext().unlock()

    

##     # implements GenericDocument
##     def getLineWidth(self):
##         return 100
##     def getColumnSepWidth(self):
##         return 0
                
        
    
class ReportRowForm(ReportForm):
    def __init__(self,rpt,recno=0,**kw):
        ReportForm.__init__(self,rpt,**kw)
        self.currentRow=self.rpt[recno]
        #if recno < 0:
        #    recno+=len(self.rpt)
        #self.recno=recno
        self.beforeRowEdit()

    def isEditing(self):
        return self.enabled

    def onInsertRow(self):
        pass
    
    def onClose(self):
        self.afterRowEdit()
        ReportForm.onClose(self)
        
    def layout(self,panel):
        self.rpt.layoutReportForm(self,panel)
            
    def toggleEditing(self):
        self.afterRowEdit()
        self.enabled=not self.enabled
        self.beforeRowEdit()
        self.refresh()
            
    
    def getTitle(self):
        return "[%d/%d] " % (self.currentRow.index+1,len(self.rpt)) \
               +unicode(self.currentRow.item)

    def onIdle(self):
        if self.currentRow is None: return
        s = "Row %d of %d" % (self.currentRow.index,
                              len(self.rpt))
        self.session.status(s)

    def setupMenu(self):
        self.setupFileMenu()
        self.setupEditMenu()        
        m = self.addMenu("row",label="&Row")
        m.addItem("next",
                  label="&Next",
                  action=lambda : (self.skip(1), self.refresh()),
                  hotkey=keyboard.PGDN) # "PgDn")
        m.addItem("previous",
                  label="&Previous",
                  action=lambda : (self.skip(-1), self.refresh()),
                  hotkey=keyboard.PGUP) # "PgUp")
        m.addItem("edit",
                  label="&Edit",
                  hotkey=keyboard.F2).setHandler(self.toggleEditing)
        
        self.rpt.setupMenu(self)

    def setupEditMenu(self):
        m = self.addMenu("edit",label="&Edit")
        def copy():
            #from cStringIO import StringIO
            out = StringIO()
            self.rpt.__xml__(out.write)
            self.showForm(MemoViewer(out.getvalue()))
        
        m.addItem("copy",
                  label="&Copy",
                  action=copy)
        
        #m = frm.addMenu("row",label="&Row")
        if self.rpt.canWrite():
            m.addItem("delete",
                      label="&Delete selected row(s)",
                      action=self.deleteCurrentRow,
                      hotkey=keyboard.DELETE) # accel="DEL")
            m.addItem("insert",
                      label="&Insert new row",
                      action=self.insertRow,
                      hotkey=keyboard.INSERT) # accel="INS")

            
    def skip(self,n):
        recno=self.currentRow.index
        if n > 0:
            if recno + n < len(self.rpt):
                recno += n
            else:
                return
        else:
            if recno + n >= 0:
                recno += n
            else:
                return
        self.setCurrentRow(self.rpt[recno])
        self.refresh()
        

    def deleteCurrentRow(self):
        assert self.rpt.canWrite()
        row=self.getCurrentRow()
        if row is None:
            print "no current row"
            return
        if not self.session.confirm(
            "Delete this row. Are you sure?"):
            return
        row.item.delete()
        self.refresh()
        
    #def getSelectedRows(self):
    #    return [self.getCurrentRow()]
        

    def getStatus(self):
        return "%d/%d" % (self.currentRow.index,len(self.rpt))
    
##     def insertRow(self):
##         self.afterRowEdit()
##         assert self.rpt.canWrite()
##         self.currentRow=self.rpt.appendRow()
##         self.beforeRowEdit()
##         self.refresh()


class ReportGridForm(ReportForm):
    
    rowForm=ReportRowForm
    
    def __init__(self,*args,**kw):
        ReportForm.__init__(self,*args,**kw)
        self.grid=None
        #self.pickedRow=None
        self.editing=False

    def layout(self,panel):
        self.grid=panel.datagrid(self.rpt)

    def setupEditMenu(self):
        m=ReportForm.setupEditMenu(self)
        m.addItem("showRowForm",
                  label="&Form view",
                  action=self.showRowForm,
                  hotkey=keyboard.CTRL_RETURN) # accel="Ctrl-ENTER")

        
    def showRowForm(self):
        #self.pickedRow=self.getCurrentRow()
        row=self.getCurrentRow()
        frm=self.rowForm(self.rpt,row.index)
        self.showForm(frm)
        
    def isEditing(self):
        return self.editing

    def onIdle(self):
        if self.grid is None: return
        l = self.grid.getSelectedRows()
        if len(l) == 1:
            s = "Row %d of %d" % (l[0]+1,len(self.rpt))
        else:
            s = "Selected %s of %d rows" % (len(l), len(self.rpt))
                
        self.session.status(s)
        
    def onInsertRow(self):
        self.grid.onInsertRow(self)
    
    def getSelectedCol(self):
        if self.grid is None:
            return None
        return self.grid.getSelectedCol()
        
    def getCurrentRow(self):
        if self.grid is None: return None
##         l = self.grid.getSelectedRows()
##         if len(l) == 1:
##             return self.rpt[l[0]]
##         #raise "There is more than one row selected"
        return self.grid.getCurrentRow()

class ReportGridPickForm(ReportGridForm):
    #modal=True
    def __init__(self,rpt,onpick,*args,**kw):
        ReportGridForm.__init__(self,rpt,*args,**kw)
        self.onpick=onpick
        #self.pickedRow=None
        
    def setupFileMenu(self):
        m=ReportGridForm.setupFileMenu(self)
        m.addItem("pick",
                  label="&Pick this row",
                  action=self.pick,
                  hotkey=keyboard.RETURN) # accel="ENTER"
    def pick(self):
        #self.pickedRow=self.getCurrentRow()
        pickedRow=self.getCurrentRow()
        if pickedRow is not None:
            self.onpick(pickedRow)
            self.close()
        else:
            self.session.notice("Cannot pick Nothing")

    
        
        
    
class DbMainForm(Form):
    
    #schemaClass=NotImplementedError
    
    def __init__(self,dbsess,*args,**kw):
        if dbsess is None:
            dbsess=self.createContext()
##         if dbsess is not None:
##             assert isinstance(dbsess.db.schema,self.schemaClass),\
##                    "%s is not a %s" % (dbsess.db.schema,
##                                        self.schemaClass)
            
        self.dbsess=dbsess
        Form.__init__(self,*args,**kw)

    def createContext(self):
        raise NotImplementedError

##     def setupForm(self):
##         if self.dbsess is None:
##             self.dbsess=self.schemaClass(self.toolkit).quickStartup()

    def addProgramMenu(self):
        m = self.addMenu("app","&Programm")
        m.addItem("close",label="&Beenden",action=self.close)
        #if self.toolkit.app is not None:
        m.addItem("about",label="Inf&o").setHandler(
            lambda : self.session.message(
            self.toolkit.root.aboutString(), title="About"))

##         def bugdemo(task):
##             for i in range(5,0,-1):
##                 self.session.status("%d seconds left",i)
##                 task.increment()
##                 task.sleep()
##             thisWontWork()
            
        
##         m.addItem("bug",label="&Bug demo").setHandler(
##             self.session.loop,bugdemo,"Bug demo")

        self.addTaskItem(m,"bug",BugDemo())

        
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m
    
    def addTaskItem(self,menu,name,task,label=None,**kw):
        if label is None: label=task.getTitle()
        mi=menu.addItem(name,label=label,**kw)
        mi.setHandler(task.runfrom,self.session)

    
    def onClose(self):
        self.dbsess.close()

    def getTitle(self):
        return str(self.dbsess)
    

    def addReportItem(self,menu,name,rptclass,label=None,**kw):
        rpt=self.dbsess.createReport(rptclass)
        if label is None: label=rpt.getTitle()
        mi=menu.addItem(name,label=label,**kw)
        mi.setHandler(self.toolkit.show_report,self.session,rpt)

    
##     def showViewGrid(self,tc,*args,**kw):
##         rpt=self.getViewReport(tc,*args,**kw)
##         return self.toolkit.showReport(rpt)
    
##     def showDataForm(self,rpt,**kw):
##         rpt.showFormNavigator(self,**kw)
        
##     def showDataForm(self,rpt,**kw):
##         frm = self.form(label=rpt.getLabel(),**kw)
##         rpt.setupForm(frm)
##         frm.show()
        
    def chooseDataRow(self,ds,currentRow,**kw):
        frm = self.form(label="Select from " + ds.getLabel(),**kw)
        grid = frm.addDataGrid(ds)
        grid.setModeChoosing()
        frm.showModal()
        return grid.getChosenRow()
        
##     def runLoader(self,loader): #lc,*args,**kw):
##         #store=self.getStore(loader.tableClass)
##         #loader.load(self,store)
##         #store=self.getStore(lc.tableClass)
##         #loader=lc(self,*args,**kw)
##         loader.run(self)
        

    def showQuery(self,qry,*args,**kw):
        rpt=self.dbsess.createQueryReport(qry,*args,**kw)
        self.toolkit.show_report(self,rpt)

##     def report(self,*args,**kw):
##         rpt=self.createReport(*args,**kw)
##         self.session.report(rpt)
    

##     def showMainForm(self):
##         self.db.app.showMainForm(self)









## class ReportForm(Form):
##     def __init__(self,app,rpt):
##         Form.__init__(self,app)
##         self.rpt = rpt # a Query or a Report
##         #assert len(ds._lockedRows) == 0
##         self.rpt.beginReport(self)
        
        
##     def setupGoMenu(self):
##         pass
        
##     def setupMenu(self):
##         m = self.addMenu("file",label="&File")
##         m.addItem("exit",label="&Exit",
##                   action=self.close,
##                   accel="ESC")
##         m.addItem("refresh",
##                   label="&Refresh",
##                   action=self.refresh,
##                   accel="Alt-F5")
##         m.addItem("printRow",
##                   label="Print &Row",
##                   action=self.printRow,
##                   accel="F7")
##         m.addItem("printList",
##                   label="Print &List",
##                   action=self.printList,
##                   accel="Shift-F7")
        
##         self.setupGoMenu()
        

##         m = self.addMenu("edit",label="&Edit")
##         def copy():
##             #from cStringIO import StringIO
##             out = StringIO()
##             self.rpt.__xml__(out.write)
##             MemoViewer(self,out.getvalue()).show()
        
##         m.addItem("copy",
##                   label="&Copy",
##                   action=copy)
        
##         #m = frm.addMenu("row",label="&Row")
##         if self.rpt.canWrite():
##             m.addItem("delete",
##                       label="&Delete selected row(s)",
##                       action=self.deleteSelectedRows,
##                       accel="DEL")
##             m.addItem("insert",
##                       label="&Insert new row",
##                       action=self.insertRow,
##                       accel="INS")
            
##         self.rpt.setupMenu(self)

##     def onIdle(self):
##         l = self.getSelectedRows()
##         if len(l) == 1:
##             s = "Row %d of %d" % (l[0]+1,len(self.rpt))
##         else:
##             s = "Selected %s of %d rows" % (len(l), len(self.rpt))
##         self.status(s)

##     def insertRow(self):
##         assert self.rpt.canWrite()
##         row = self.rpt.appendRow()
##         self.refresh()
    
##     def deleteSelectedRows(self):
##         assert self.rpt.canWrite()
##         if not self.confirm(
##             "Delete %d rows. Are you sure?" % \
##             len(self.getSelectedRows())):
##             return
##         for i in self.getSelectedRows():
##             row = self.rpt[i].delete()
##         self.refresh()

##     def printRow(self):
##         #print "printSelectedRows()", self.getSelectedRows()
##         #workdir = "c:\\temp"
##         #ui = self.getForm()
##         #workdir = self.getForm().toolkit.app.tempDir
##         from lino.oogen import SpreadsheetDocument
##         doc = SpreadsheetDocument("printRow")
##         for i in self.getSelectedRows():
##             row = self.rpt[i]
##             row.printRow(doc)
##         #outFile = opj(workdir,"raceman_report.sxc")
##         doc.save(self,showOutput=True)

##     def printList(self):
##         #ui = self.getForm()
##         #workdir = self.getForm().toolkit.app.tempDir
##         raise "must rewrite"
##         from lino.oogen import SpreadsheetDocument
##         doc = SpreadsheetDocument("printList")
##         rows = self.getSelectedRows()
##         if len(rows) == 1:
##             rows = self.rpt
##         rpt = doc.report()
##         self.rpt.setupReport(rpt)
##         rpt.execute(rows)
##         #outFile = opj(workdir,self.ds.getName()+".sxc")
##         doc.save(self.getForm(),showOutput=True)

##     def getSelectedRows(self):
##         raise NotImplementedError

##     def getCurrentRow(self):
##         l = self.getSelectedRows()
##         if len(l) != 1:
##             raise InvalidRequestError("more than one row selected!")
##         i = l[0]
##         if i == len(self.rpt):
##             raise InvalidRequestError(\
##                 "you cannot select the after-last row!")
##         return self.rpt[i]

##     def withCurrentRow(self,meth,*args,**kw):
##         r = self.getCurrentRow()
##         meth(r,*args,**kw)
        
##     def onClose(self):
##         self.rpt.onClose()

##     def getLineWidth(self):
##         return 80
##     def getColumnSepWidth(self):
##         return 0

## def nop(x):
##     pass

## class ReportRowForm(ReportForm):
    
##     def __init__(self,app,rpt,afterSkip=nop,*args,**kw):
##         ReportForm.__init__(app,rpt)
##         self.afterSkip = afterSkip
##         self.currentPos = 0

##     def skip(self,n):
##         #print __name__, n
##         if n > 0:
##             if self.currentPos + n < len(self.rpt):
##                 self.currentPos += n
##                 self.afterSkip(self)
##                 self.refresh()
##         else:
##             if self.currentPos + n >= 0:
##                 self.currentPos += n
##                 self.afterSkip(self)
##                 self.refresh()


##     def getSelectedRows(self):
##         return [self.currentPos]
        

##     def setupGoMenu(self):
##         frm = self.getForm()
##         m = frm.addMenu("go",label="&Go")
##         m.addItem("next",
##                   label="&Next",
##                   accel="PgDn").setHandler(self.skip,1)
##         m.addItem("previous",
##                   label="&Previous",
##                   accel="PgUp").setHandler(self.skip,-1)

##     def getStatus(self):
##         return "%d/%d" % (self.currentPos,len(self.rpt))
    
    
                
        

class Dialog(Form):
    
    modal=True
    
    def ok(self):
        self.returnValue=YES
        self.close()

    def cancel(self):
        self.returnValue=NO
        self.close()


class MessageDialog(Dialog):
    title="Message"
    def __init__(self,msg,**kw):
        Dialog.__init__(self,**kw)
        self.msg=msg
        
    def layout(self,p):
        p.label(self.msg)
        p.okButton()
        
class ConfirmDialog(Dialog):
    title="Confirmation"
    def __init__(self,prompt,default=YES,**kw):
        Dialog.__init__(self,**kw)
        self.prompt=prompt
        self.default=default
        
    def layout(self,panel):
        panel.label(self.prompt)
        
        #p=self.addPanel(HORIZONTAL)
        p=panel.hpanel()
        ok=p.okButton()
        cancel = p.cancelButton()
        if self.default == YES:
            ok.setDefault()
        else:
            cancel.setDefault()
