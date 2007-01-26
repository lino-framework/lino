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


from PyQt4 import QtCore, QtGui
 

from lino.adamo.exceptions import InvalidRequestError

from lino.adamo import datatypes
from lino import forms
from lino.forms import toolkit

from lino.forms.qt import qtgrid

STRETCH = 1
DONTSTRETCH=0

BORDER=10
NOBORDER=0

#ENTRY_DOC_FONT = wx.SMALL_FONT
#ENTRY_PANEL_BACKGROUND = None
#ENTRY_LABEL_BACKGROUND = None
#ENTRY_PANEL_BACKGROUND = wx.BLUE
#ENTRY_LABEL_BACKGROUND = wx.GREEN

from textwrap import TextWrapper
docWrapper = TextWrapper(30)


def _setEditorSize(editor,type):

    editor.SetMinSize(editor.GetBestSize())


class EventCaller:
    
    def __init__(self,meth,*args,**kw):
        self.meth = meth
        self.args = args
        self.kw = kw
        
    def __call__(self,event):
        return self.meth(*self.args, **self.kw)

class Label(toolkit.Label):
    
    def qtsetup(self,form,panel,box):
        text = self.getLabel()
        if self.getDoc() is not None:
            text += '\n' + self.getDoc()
        ctrl = QtGui.QLabel(text,panel)
        box.addWidget(ctrl, DONTSTRETCH)
        self.qtctrl = ctrl
                
class Button(toolkit.Button):
    
    def qtsetup(self,form,panel,box):
        #parentFormCtrl = self.getForm().ctrl
        #winId = wx.NewId()
        btn = QtGui.QPushButton(self.getLabel(),panel)
        #btn.SetBackgroundColour('YELLOW')
        #parentFormCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)

        form.connect(btn, QtCore.SIGNAL("clicked()"), self.click) 
##         if self.hotkey is not None:
##             #print 'Button.wxsetup', self.hotkey
##             wx.EVT_CHAR(panel, self.EVT_CHAR)
##             #form.Bind(wx.EVT_KEY_DOWN,self.EVT_CHAR)
        if self.doc is not None:
            btn.setToolTip(self.doc)

        box.addWidget(btn,DONTSTRETCH)
        self.qtctrl = btn

    def setFocus(self):
        self.qtctrl.SetFocus()

class DataGrid(toolkit.DataGrid):
    
    def qtsetup(self,form,parent,box):
        #print "wxsetup()", self
        #box.Add(self.qtctrl, STRETCH, wx.EXPAND,BORDER)

        model=qtgrid.DataGridModel(self)
        
##         model=QSqlQueryModel();
##         model.setQuery(self.);
##         model.setHeaderData(0, Qt.Horizontal, tr("Name"));
##         model.setHeaderData(1, Qt.Horizontal, tr("Salary"));

        self.qtctrl=QtGui.QTableView(parent)
        self.qtctrl.setModel(model)
        #view.show();
        
        #self.refresh()
        
    def refresh(self):
##         if self.isDirty():
##             self.commit()
        self.qtctrl.table._load()
        self.qtctrl.table._refresh()
##         for row in self.qtctrl.table.rows:
##             print id(row)

    def onRowInserted(self,frm,row):
        #l=self.getSelectedRows()
        #print "wxtoolkit.onRowInserted()"
        #print "\n".join([str(r.index)+':'+str(r)+":"+str(id(r))
        #                 for r in self.qtctrl.table.rows])
        #row=frm.currentRow
        #print row.index
        oldlen=self.qtctrl.table.GetNumberRows()
        self.qtctrl.table.rows.insert(row.index,row)
        for tr in self.qtctrl.table.rows[row.index+2:]:
            tr.index += 1
            #print tr.index
        #print "\n".join([str(r.index)+':'+str(r)+":"+str(id(r))
        #                 for r in self.qtctrl.table.rows])
        #self.qtctrl.table.cells.append([s for col,s in row.cells()])
        self.qtctrl.table.resetRows(self.qtctrl,oldlen)
            
    def onRowsDeleted(self,frm,indexes):
        oldlen=len(self.qtctrl.table.rows)
        for i in indexes:
            del self.qtctrl.table.rows[i]
        self.qtctrl.table.resetRows(self.qtctrl,oldlen)
        
    def getSelectedRows(self):
        return self.qtctrl.getSelectedRows()

    def getSelectedRow(self):
        return self.qtctrl.getSelectedRow()

    def getSelectedCol(self):
        return self.qtctrl.getSelectedCol()
        

class TextViewer(toolkit.TextViewer):

    def __init__(self,*args,**kw):
        toolkit.TextViewer.__init__(self,*args,**kw)
        #self._buffer = ""
        self.qtctrl = None
        
        
    def onClose(self):
##         console.pop()
        console = self.getForm().toolkit.console
        console.redirect(*self.redirect)
        self.qtctrl = None
        #self._buffer = ""
        #raise "it is no good idea to close this window"
    
    def qtwxsetup(self,form,panel,box):
        #parentFormCtrl = self.getForm().qtctrl
        console = form.toolkit.console
        e = wx.TextCtrl(panel,-1,console.getConsoleOutput(),
                        style=wx.TE_MULTILINE|wx.HSCROLL)
        e.SetBackgroundColour('BLACK')
        e.SetForegroundColour('WHITE')
        e.SetEditable(False)
        e.SetMinSize(e.GetBestSize())
        #_setEditorSize(e,MEMO(width=50,height=10))
        #e.SetEnabled(False)
        box.addWidget(e, STRETCH, wx.EXPAND|wx.ALL,NOBORDER)
        self.qtctrl = e
        self.qtctrl.SetInsertionPointEnd()
        #self.qtctrl.ShowPosition(-1)
        self.redirect = console.redirect(self.addText,self.addText)
        self.getForm().session.debug(
            str(e.GetMinSize())+" "+str(e.GetMaxSize()))

    def addText(self,s):
        self.qtctrl.WriteText(s)
        self.qtctrl.ShowPosition(-1)
##         if self.qtctrl is not None:
##             self.qtctrl.WriteText(s)
##             self.qtctrl.ShowPosition(-1)
##         else:
##             self._buffer += s
    

class Panel(toolkit.Panel):

    def qtsetup(self,form,parent,box):
        #print self,"wxsetup()"
        ctrl = QtGui.QWidget(parent)
        if box is not None:
            box.addWidget(ctrl,self.weight)
        if self.direction == forms.VERTICAL:
            mybox = QtGui.QVBoxLayout()
        else:
            mybox = QtGui.QHBoxLayout()
        ctrl.setLayout(mybox)
        
        self.mybox = mybox # store reference to avoid crash?
        self.qtctrl = ctrl
        
        for c in self._components:
            c.qtsetup(form,ctrl,mybox)
            c.qtctrl.adjustSize()

class VPanel(Panel):
    direction=forms.VERTICAL
class HPanel(Panel):
    direction=forms.HORIZONTAL

def SwappedBoxSizer(box):
    if box.GetOrientation() == wx.VERTICAL:
        return wx.BoxSizer(wx.HORIZONTAL)
    else:
        return wx.BoxSizer(wx.VERTICAL)

class EntryMixin:

    def qtsetup(self,form,panel,box):
        if self.hasLabel():
            mypanel = QtGui.QWidget(panel,-1)
            mypanel.SetBackgroundColour(ENTRY_PANEL_BACKGROUND)
            box.addWidget(mypanel, self.weight, wx.EXPAND|wx.ALL,BORDER)
            #hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox = SwappedBoxSizer(box)
            mypanel.setLayout(hbox)

            if self.doc is not None:
                label = QtGui.QWidget(mypanel,-1)
                label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer = SwappedBoxSizer(hbox)
                label.setLayout(labelSizer)

                labelCtrl = wx.StaticText(
                    label,-1,self.getLabel(),style=wx.ALIGN_RIGHT)
                labelCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer.addWidget(labelCtrl,DONTSTRETCH)

                docCtrl = wx.StaticText(
                    label, -1,
                    "\n".join(docWrapper.wrap(self.doc)),
                    style=wx.ALIGN_LEFT)
                docCtrl.SetFont(ENTRY_DOC_FONT)
                docCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer.addWidget(docCtrl,DONTSTRETCH)

            else:
                label = wx.StaticText(mypanel, -1,
                                      self.getLabel(),
                                      style=wx.ALIGN_RIGHT)
                label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)

            if hbox.GetOrientation() == wx.HORIZONTAL:
                hbox.addWidget(
                    label, STRETCH,
                    wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL,
                    BORDER)
            else:
                hbox.addWidget(
                    label, DONTSTRETCH,
                    wx.ALIGN_LEFT,
                    BORDER)

            hbox.addWidget( (10,1), DONTSTRETCH,0,NOBORDER) # spacer
            
        else:
            mypanel = panel
            hbox = box

        type = self.getType()
        if isinstance(type,datatypes.BoolType):
            editor=wx.CheckBox(mypanel,-1)
            v=self.getValue()
            if v is None:
                v=self.getType().defaultValue
            editor.SetValue(v)
        else:
            style=0
            if self.getMaxHeight() > 1:
                style = style|wx.TE_MULTILINE
            #if isinstance(type,datatypes.IntType):
            #    print __builtins__['type'](self.getValueForEditor())
            editor = wx.TextCtrl(mypanel,-1,
                                 self.getValueForEditor(),
                                 style=style)
                                 #validator=EntryValidator(self))
                                 #style=wx.TE_PROCESS_ENTER)

            editor.SetMinSize(editor.GetBestSize())
            #_setEditorSize(editor,self)
        
        if self.enabled:
            editor.Enable()
        else:
            editor.Disable()
            
        #print editor.GetMinSize(), editor.GetMaxSize()
        #print mypanel.GetMinSize(), editor.GetMaxSize()
        
        #self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        #editor.Bind(wx.EVT_CHAR, self.EVT_CHAR)
        #editor.Bind(wx.EVT_KEY_DOWN, self.EVT_CHAR)
        #editor.Bind(wx.EVT_KEY_UP, self.EVT_CHAR)
        #editor.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        #editor.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        #editor.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)

        self.editor = editor 
        if not self.hasLabel():
            if hbox.GetOrientation() == wx.HORIZONTAL:
                hbox.addWidget(editor,STRETCH,
                               wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,
                               BORDER)
            else:
                #print "dont stretch:",self
                hbox.addWidget(editor,DONTSTRETCH,
                               wx.ALIGN_LEFT,
                               BORDER)
            self.qtctrl = mypanel
        else:
            hbox.addWidget(editor,STRETCH)
            self.qtctrl = editor

##     def EVT_CHAR(self, evt):
##         print "EVT_CHAR ", self, evt.GetKeyCode()
##         if evt.GetKeyCode() == 27: return
##         evt.Skip()

    def getValueForEditor(self):
        "return current value as string"
        v = self.getValue()
        if isinstance(self.getType(),datatypes.BoolType):
            if v is None:
                return False
            return v
        if v is None: return ""
        return self.format(v)
        

    def setValueFromEditor(self,x):
        """convert the string and store it as raw value.

        """
        if isinstance(self.getType(),datatypes.BoolType):
            self.setValue(x)
        else:
            if len(x) == 0:
                self.setValue(None)
            else:
                self.setValue(self.parse(x))
            
    def refresh(self):
        if hasattr(self,'editor'):
            x = self.getValueForEditor()
            self.editor.SetValue(x)
        
    def setFocus(self):
        self.editor.SetFocus()
        self.editor.SetSelection(-1,-1)
        
    def isDirty(self):
        if isinstance(self.getType(),datatypes.BoolType):
            return False
        return self.editor.IsModified()

    def store(self):
        #type = self._type
        #if isinstance(type,datatypes.StringType):
        if self.isDirty():
            s = self.editor.GetValue()
            #print "wxtoolkit:store()",self,s
            self.setValueFromEditor(s)
        
        
        
##         # on MS-Windows:
##         # killfocus can accur after the windows have been destroyed
##         # note: looks as if this is not necessary anymore
        
##         #if self.form.dying: return
##         if self.editor.IsModified():
##             s = self.editor.GetValue()
##             self.setValueFromEditor(s)
##             evt.Skip()

            
class Entry(EntryMixin,toolkit.Entry):
    pass

class DataEntry(EntryMixin,toolkit.DataEntry):
    
    def qtsetup(self,form,panel,box):
        EntryMixin.qtsetup(self,form,panel,box)
        #self.editor.SetEditable(self.enabled)
        if self.enabled:
            self.editor.Enable()
        else:
            self.editor.Disable()
        
    def refresh(self):
        EntryMixin.refresh(self)
        toolkit.DataEntry.refresh(self)
        if self.enabled:
            self.editor.Enable()
        else:
            self.editor.Disable()
        #self.editor.SetEditable(self.enabled)
        #if not self.enabled:
        #    print str(self), "is read-only"
    



## class QtApp(QtGui.QApplication):

##     def __init__(self,app):
##         self.app = app
##         QtGui.QApplication.__init__(app.args)


##     def OnInit(self):
        
##         # wx.App.OnInit(self)        
##         # Notice that if you want to to use the command line
##         # processing provided by wxWidgets you have to call the base
##         # class version in the derived class OnInit().
        
##         wx.InitAllImageHandlers()
##         #self.toolkit.wxinit()
##         #self.toolkit.showMainForm()
##         return True

##     def OnExit(self):
##         #center.shutdown()
##         pass



class Toolkit(toolkit.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    hpanelFactory = HPanel
    vpanelFactory = VPanel
    dataGridFactory = DataGrid
            
    def createFormCtrl(self,frm):
        parent=frm._parent
        if parent is None:
            qtparent = None
        else:
            qtparent = parent.ctrl

            
        if frm.modal:
            ctrl = QtGui.QDialog(qtparent)
            frm.mainComp.qtsetup(ctrl,ctrl,None)
            # ctrl.layout().addWidget(frm.mainComp.qtctrl)
        else:
            ctrl = QtGui.QMainWindow(qtparent)
            #ctrl.CreateStatusBar(1, wx.ST_SIZEGRIP)
            #centralWidget=QtGui.QWidget()
            #ctrl.setCentralWidget(centralWidget)
            frm.mainComp.qtsetup(ctrl,ctrl,None)
            ctrl.setCentralWidget(frm.mainComp.qtctrl)

        ctrl.setWindowTitle(frm.getTitle())
        
        if frm.menuBar is not None:
            qtMenuBar = ctrl.menuBar()
            for mnu in frm.menuBar.menus:
                qtmnu = qtMenuBar.addMenu(mnu.getLabel())
                for mi in mnu.items:
                    shk=0
                    lbl=mi.getLabel()
                    if mi.hotkey is not None:
                        hotkey=mi.hotkey.__name__.replace("_","-")
                        lbl += "\t" + hotkey
                        shk=QtGui.QKeySequence(hotkey)
                    qtmnu.addAction(lbl,mi.click,shk)

        

##         ctrl.Bind(wx.EVT_SET_FOCUS, frm.onSetFocus)
##         ctrl.Bind(wx.EVT_KILL_FOCUS, frm.onKillFocus)

##         def flags(key):
##             if key.shift: return wx.ACCEL_SHIFT
##             if key.alt: return wx.ACCEL_ALT
##             if key.ctrl: return wx.ACCEL_CTRL
##             return wx.ACCEL_NORMAL


##         wx.EVT_CLOSE(ctrl, frm.close)

        #mainBox=QtGui.QVBoxLayout() 
        #ctrl.setLayout(mainBox)


##         if frm.defaultButton is not None:
##             frm.defaultButton.qtctrl.SetDefault()

##         # MenuItems have no .qtctrl, the are automagically bound if
##         # the lbl passed to wxMenu.Append(winId,lbl,doc) contains a \t
##         # and a key name...

##         if len(frm.accelerators):
##             l=[ (flags(key),
##                  key.keycode,
##                  btn.qtctrl.GetId())
##                 for key,btn
##                 in frm.accelerators if hasattr(btn,'qtctrl')]
##             ctrl.SetAcceleratorTable(wx.AcceleratorTable(l))

            
        

        CHARWIDTH = ctrl.fontMetrics().averageCharWidth()
        LINEHEIGHT = ctrl.fontMetrics().lineSpacing()

        if frm.minWidth is not None:
            ctrl.setMinimumWidth(frm.minWidth * CHARWIDTH)
        if frm.minHeight is not None:
            ctrl.setMinimumHeight(frm.minHeight * LINEHEIGHT)
            
        if frm.maxWidth is not None:
            ctrl.setMaximumWidth(frm.maxWidth * CHARWIDTH)
        if frm.maxHeight is not None:
            ctrl.setMaximumHeight(frm.maxHeight * LINEHEIGHT)
            
        if False:
            if frm.halign is forms.CENTER:
                ctrl.Centre(wx.HORIZONTAL)
            if frm.valign is forms.CENTER:
                ctrl.Centre(wx.VERTICAL)

            x,y = ctrl.GetPositionTuple()

            if frm.halign is forms.LEFT:
                x = 0
            elif frm.halign is forms.RIGHT:
                x = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
                x -= ctrl.GetSizeTuple()[0]

            if frm.valign is forms.TOP:
                y = 0
            elif frm.halign is forms.RIGHT:
                y = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
                y -= ctrl.GetSizeTuple()[1]

            ctrl.SetPosition((x,y))
        
        return ctrl




    def executeShow(self,frm):
        frm.ctrl.adjustSize()
        frm.ctrl.show()

    def executeRefresh(self,frm):
        frm.ctrl.update()
        # docs/examples/forms4.py : pgup/pgdn changes the title
        frm.ctrl.setWindowTitle(frm.getTitle())

    def closeForm(self,frm,evt):
        #print "closeForm()"
        frm.ctrl.close()



    def onTaskBegin(self,task):
        #assert self.progressDialog is None
        #print job
        #assert self._activeForm is not None
        if self._activeForm is None:
            parent=None
        else:
            parent=self._activeForm.ctrl
        title=""
##         if task.statusMessage is None:
##             stm=""
##         else:
##             stm=task.statusMessage
        if task.maxval == 0:
            task.qtctrl=None
            return self.console.onTaskBegin(task)
        else:
            task.qtctrl = QtGui.QProgressDialog(
                labelText=task.getStatusLine(),
                maximum=100,
                parent=parent)
            task.qtctrl.setWindowTitle(title)

    def on_breathe(self,task):
        if not hasattr(task,'qtctrl') or task.qtctrl is None:
            return self.console.on_breathe(task)
        msg=task.getStatus()
        #pc = task.percentCompleted
        pc=int(100*task.curval/task.maxval)
        #if pc is None: pc = 0
        if msg is not None:
            task.qtctrl.setLabelText(msg)
        task.qtctrl.setValue(pc)
        if task.qtctrl.wasCancelled():
            task.requestAbort()
        self.run_awhile()
        

    def onTaskResume(self,task):
        if task.qtctrl is None:
            return self.console.onTaskResume(task)
        task.qtctrl.Resume()
        
    def onTaskDone(self,task):
        if task.qtctrl is None:
            return self.console.onTaskDone(task)
        task.qtctrl.setValue(100)
        task.qtctrl.close()
        task.qtctrl=None

    def onTaskAbort(self,task,*args,**kw):
        if task.qtctrl is None:
            return self.console.onTaskAbort(task)
        task.qtctrl.close()
        task.qtctrl=None

    def run_awhile(self):
        assert self.running()
        while self.root.ctrl.hasPendingEvents():
            self.root.ctrl.processEvents()

    def start_running(self,app):
        toolkit.Toolkit.start_running(self,app)
        self.root.ctrl = QtGui.QApplication([])
        #self.wxapp = WxApp(self)
        #wx.EVT_IDLE(self.wxapp, self.onIdle)
        
    def run_forever(self,*args,**kw):
        assert self.running()
        self.root.ctrl.exec_()

    def stop_running(self):
        self.root.ctrl.exit()
        
