## Copyright 2005-2007 Luc Saffre 

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

from lino.console.task import BugDemo
from lino.gendoc.gendoc import GenericDocument
from lino.forms import keyboard
from lino.forms.forms import Form, Dialog
#from lino.adamo.dbreports import QueryReport
from lino.forms.gui import GuiApplication

class CreateReportRowDialog(Dialog):
    
    def __init__(self,row,**kw):
        Dialog.__init__(self,**kw)
        self.row=row

    def layout(self,panel):
        for col in self.row.rpt.columns:
            if col.isMandatory():
                panel.dataentry(col,label=col.getLabel())
        #self.row.rpt.layoutReportForm(self,panel)
        panel.cancelButton()
        panel.okButton()
        
    def getTitle(self):
        return "Create Row in "+str(self.row.rpt)

    def getCurrentRow(self):
        return self.row



class ReportForm(Form,GenericDocument):
    
    """A Form used to display and edit the rows of a Report.
    
    This is the abstract base class for ReportRowForm and
    ReportGridForm.

    Vocabulary: Note that the *current* row is not necessarily the
    same as the *selected* row. In a ReportGridForm the user may start
    to edit a cell (whose row becomes current row and gets locked),
    then clicks on another row.
    
    """
    
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
        #print "afterRowEdit", self.currentRow
        if self.currentRow is None: return
        #print "afterRowEdit()",repr(self.currentRow.item)
        if self.currentRow.item.isNew() \
              or self.currentRow.item.isLocked():
            #print "isLocked()"
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
        raise DeprecationError("rpt=QueryReport(allowedValues)")
    
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


    def insertRow(self):
        """Interactively inserts a new row into the Report.
        
        Called when the user hits INSERT.

        """
        assert self.rpt.canWrite()
        self.afterRowEdit()
        self.enabled=True
##         item=self.rpt.query._appendRow()
##         self.currentRow=self.rpt.process_item(item)
        sel=self.getSelectedRow()
        #print "forms.insertRow()", sel
        if sel is None:
            index=0
        else:
            index=sel.index
        #print index
        #print id(self.currentRow)
        row=self.rpt.createRow(index)
        dlg=CreateReportRowDialog(row)
        if not self.showForm(dlg):
            return
        #print "dbforms.py:", row
        self.currentRow=row
        row.item.commit()
        #print id(self.currentRow)
        #row.item.commit()
        #self.rpt.query._store.fireUpdate()
        #self.beforeRowEdit()
        self.onRowInserted()
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
        l=self.getSelectedRows()
        if len(l) == 1:
            if not self.confirm(
                "Delete row '%s'. Are you sure?" % self.rpt[l[0]]):
                return
        elif not self.confirm(
            "Delete %d rows. Are you sure?" % len(l)):
            return
        
        # we must delete rows from bottom to top because deleting one
        # row changes the index of the rows behind it.
        
        l.sort()
        l.reverse()
        
        for i in l:
            self.rpt[i].item.delete()
        self.onRowsDeleted(l)
        
    def printRow(self):
        from lino.gendoc.html import HtmlDocument
        doc=HtmlDocument()
        for i in self.grid.getSelectedRows():
            row = self.rpt[i]
            row.printRow(doc)
        filename="tmp.html"
        doc.saveas(filename)
        self.session.showfile(filename)
        
##         #print "printSelectedRows()", self.getSelectedRows()
##         #workdir = "c:\\temp"
##         #ui = self.getForm()
##         #workdir = self.getForm().toolkit.app.tempDir
##         from lino.oogen import SpreadsheetDocument
##         doc = SpreadsheetDocument("printRow")
##         for i in self.grid.getSelectedRows():
##             row = self.rpt[i]
##             row.printRow(doc)
##         #outFile = opj(workdir,"raceman_report.sxc")
##         doc.save(self.getForm(),showOutput=True)

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
        doc.save(self,showOutput=True)

    def onClose(self):
        self.afterRowEdit()
        #print "onClose", self
        self.rpt.endReport()
        #self.rpt.query.getContext().unlock()

    

##     # implements GenericDocument
##     def getLineWidth(self):
##         return 100
##     def getColumnSepWidth(self):
##         return 0
                
        
    
class ReportRowForm(ReportForm):
    """A ReportForm who displays one row at a time.

    The user can browse the rows of the report using PGUP and PGDN.

    """
    def __init__(self,rpt,recno=0,**kw):
        ReportForm.__init__(self,rpt,**kw)
        self.currentRow=self.rpt[recno]
        #if recno < 0:
        #    recno+=len(self.rpt)
        #self.recno=recno
        self.beforeRowEdit()

    def isEditing(self):
        return self.enabled

    def onRowInserted(self):
        self.refresh()
    
    def onRowsDeleted(self,indexes):
        self.refresh()

    def getSelectedRow(self):
        return self.currentRow
    
##     def onClose(self):
##         self.afterRowEdit()
##         ReportForm.onClose(self)
        
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
##         if self.rpt.canWrite():
##             m.addItem("delete",
##                       label="&Delete selected row(s)",
##                       action=self.deleteCurrentRow,
##                       hotkey=keyboard.DELETE) # accel="DEL")
##             m.addItem("insert",
##                       label="&Insert new row",
##                       action=self.insertRow,
##                       hotkey=keyboard.INSERT) # accel="INS")

            
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
        

##     def deleteCurrentRow(self):
##         assert self.rpt.canWrite()
##         row=self.getCurrentRow()
##         if row is None:
##             print "no current row"
##             return
##         if not self.session.confirm(
##             "Delete this row. Are you sure?"):
##             return
##         row.item.delete()
##         self.refresh()
        
    def getSelectedRows(self):
        return [self.currentRow.index]
        

    def getStatus(self):
        return "%d/%d" % (self.currentRow.index,len(self.rpt))
    
##     def insertRow(self):
##         self.afterRowEdit()
##         assert self.rpt.canWrite()
##         self.currentRow=self.rpt.appendRow()
##         self.beforeRowEdit()
##         self.refresh()


class ReportGridForm(ReportForm):
    
    """A ReportForm whose main component is a datagrid on the Report.
    """
    
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
        row=self.getSelectedRow()
        if row is not None:
            print row.index
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
        
    def onRowInserted(self):
        #print "forms.onRowInserted()", self.currentRow.index
        self.grid.onRowInserted(self,self.currentRow)
    
    def onRowsDeleted(self,indexes):
        self.grid.onRowsDeleted(self,indexes)
        
    def getSelectedCol(self):
        if self.grid is None:
            return None
        return self.grid.getSelectedCol()
        
    def getSelectedRow(self):
        if self.grid is None: return None
##         l = self.grid.getSelectedRows()
##         if len(l) == 1:
##             return self.rpt[l[0]]
##         #raise "There is more than one row selected"
        return self.grid.getSelectedRow()

    def getSelectedRows(self):
        if self.grid is None: return []
        return self.grid.getSelectedRows()
    

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
    
    schemaClass=NotImplementedError
    
    minWidth=80
    minHeight=20
    
    def __init__(self,dbcontext,**kw):
        self.dbsess=dbcontext
        Form.__init__(self,**kw)
        
    def onClose(self):
        if self.dbsess is not None:
            self.dbsess.close()

    def addProgramMenu(self):
        m = self.addMenu("app","&Programm")
        m.addItem("close",label="&Beenden",action=self.close)
        #if self.toolkit.app is not None:
        m.addItem("about",label="Inf&o").setHandler(
            lambda : self.session.message(
            self.toolkit.root.aboutString()\
            +"\n\n"+self.toolkit.root.description.strip(),
            title="About"))

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

    
    def getTitle(self):
        return str(self.dbsess)
    

    def addReportItem(self,menu,name,rptclass,label=None,**kw):
        rpt=self.dbsess.createReport(rptclass)
        if label is None: label=rpt.getTitle()
        mi=menu.addItem(name,label=label,**kw)
        mi.setHandler(self.toolkit.show_report,self.session,rpt)

    
        
    def chooseDataRow(self,ds,currentRow,**kw):
        frm = self.form(label="Select from " + ds.getLabel(),**kw)
        grid = frm.addDataGrid(ds)
        grid.setModeChoosing()
        frm.showModal()
        return grid.getChosenRow()
        

    def showQuery(self,qry,*args,**kw):
        rpt=self.dbsess.createQueryReport(qry,*args,**kw)
        self.toolkit.show_report(self,rpt)

                

class DbApplication(GuiApplication):

    """Abstract base class for a single-database GUI application.

    """

    #usage=""
    filename=None
    langs=None
    dump=None
    populators=None
    loadMirrorsFrom=None
    mirrorLoaders=None

##     def __init__(self,filename=None,langs=None,dump=False,**kw):
##         GuiApplication.__init__(self,**kw)
##         self.filename=filename
##         self.langs=langs
##         self.dump=dump

    def configure(self,filename=None,langs=None,dump=False,
                  loadMirrorsFrom=None):
        GuiApplication.configure(self)
        if dump is not None:
            self.dump=dump
        if langs is not None:
            self.langs=langs
        if filename is not None:
            self.filename=filename
        if loadMirrorsFrom is not None:
            self.loadMirrorsFrom=loadMirrorsFrom

##     def registerMirrorLoader(self,ldr):
##         #self.loadMirrorsFrom="."
##         if self.mirrorLoaders is None:
##             self.mirrorLoaders=[]
##         self.mirrorLoaders.append(ldr)
           
    def applyOptions(self,options,args):
        if self.mirrorLoaders is not None:
            if options.loadMirrorsFrom is not None:
                self.loadMirrorsFrom=options.loadMirrorsFrom
        if len(args):
            if len(args) > 1:
                raise UsageError(
                    "Found %d arguments, expected 0 or 1" % len(args))
            self.filename=args[0]
        
    def setupOptionParser(self,parser):
        def call_set(option, opt_str, value, parser,**kw):
            self.configure(**kw)
        parser.add_option(
            "-d","--dump",
            help="dump all SQL commands to stdout",
            action="callback",
            callback=call_set,
            default=self.dump,
            callback_kwargs=dict(dump=True))
        if self.mirrorLoaders is not None:
            parser.add_option(
                "--loadMirrorsFrom",
                help="directory containing mirror source files",
                type="string",
                default=self.loadMirrorsFrom,
                dest="loadMirrorsFrom")


    def createMainForm(self):
        dbc=self.createContext()
        return self.mainFormClass(dbc)

    def createContext(self):
        #print "createContext"
        schema=self.mainFormClass.schemaClass(self)
        dbc=schema.createContext(langs=self.langs,
                                 filename=self.filename,
                                 dump=self.dump)
        if self.loadMirrorsFrom is not None:
            for lc in self.mirrorLoaders:
                ldr=lc(self.loadMirrorsFrom)
                self.runtask(ldr,dbc)
##             qry=dbc.query(lc.tableClass)
##             if qry._store.mtime()
##             it = dbc.schema.findImplementingTables(lc.tableClass)
##             assert len(it) == 1
##             it[0].setMirrorLoader(ldr)
##         if self._mirrorLoader.mtime() <= store.mtime():
##             sess.debug("No need to load "+\
##                        self._mirrorLoader.sourceFilename())
##             return
##         self._mirrorLoader.load(sess,store.query(sess))

        if self.populators is not None:
            for pc in self.populators:
                self.runtask(pc,dbc)
            
        return dbc

    
        

