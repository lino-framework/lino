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


import Tkinter
#from Tkconstants import *
import tkSimpleDialog


#from lino.ui import console

from lino.adamo import datatypes
from lino.forms import base, gui
from lino.forms.tix import tixtable


STRETCH = 1
DONTSTRETCH=0

BORDER=10
NOBORDER=0

#ENTRY_DOC_FONT = wx.SMALL_FONT
ENTRY_PANEL_BACKGROUND = None
ENTRY_LABEL_BACKGROUND = None
#ENTRY_PANEL_BACKGROUND = wx.BLUE
#ENTRY_LABEL_BACKGROUND = wx.GREEN

from textwrap import TextWrapper
docWrapper = TextWrapper(30)

def menulabel(lbl):
    underline=lbl.index('&')
    lbl=lbl.replace('&','')
    return (lbl,underline)
    


class Label(base.Label):
    
    def setupTkinter(self,parent):
        text = self.getLabel()
        if self.getDoc() is not None:
            text += '\n' + self.getDoc()
        ctrl = Tkinter.Label(parent, text=text)
        ctrl.pack()
        self.tixctrl = ctrl
                
class Button(base.Button):
    
##     def __repr__(self):
##         return "Button %s %s at %s" % (
##             self.getLabel(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
    def setupTkinter(self,parentCtrl):
        #parentFormCtrl = self.getForm().tixctrl
        lbl,underline=menulabel(self.getLabel())
        btn = Tkinter.Button(parentCtrl,
                             text=lbl,underline=underline,
                             command=self.click)
        if self.doc is not None:
            btn.SetToolTipString(self.doc)

        btn.pack()
        self.tixctrl = btn

    def setFocus(self):
        self.tixctrl.SetFocus()

class DataGrid(base.DataGrid):
    
    def setupTkinter(self,parent):
        self.rpt.beginReport(self)
        coldefs=[ (col.getLabel(),col.width)
                  for col in self.rpt.columns]
        ctrl = tixtable.MultiListbox(parent,coldefs)

        for row in self.rpt.rows(self):
            ctrl.insert(Tkinter.END,
                        [ s for col,s in row.cells()])
        self.rpt.endReport(self)
        
        ctrl.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
        
        self.tixctrl=ctrl
        
    def report(self,rpt):
        #print __file__, rpt.iterator._filters
        # initialize...
        rpt.beginReport(self)
        
    def refresh(self):
        self.tixctrl.refresh()

    def getSelectedRows(self):
        return self.tixctrl.curselection()

        
class DataForm(base.DataForm):
    
    def setupTkinter(self,parent):
        if False:
            frm = self.getForm()

            mypanel = wx.Panel(parent,-1)
            box.Add(mypanel, STRETCH, wx.EXPAND|wx.ALL,BORDER)

            #hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox=SwappedBoxSizer(box)
            mypanel.SetSizer(hbox)
            self.wxctrl = mypanel


            self.statusLabel = wx.StaticText( mypanel, -1,
                                              self.getStatus())
            hbox.Add(self.statusLabel, STRETCH, wx.EXPAND, BORDER )

            hbox.Add( (10,1), DONTSTRETCH,0,NOBORDER)

            btn = wx.Button(mypanel, -1, "<")
            hbox.Add(btn, STRETCH, wx.EXPAND, BORDER )
            self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
                                       lambda e:self.skip(-1), btn)
                                       #EventCaller(self.skip,-1))

            btn = wx.Button(mypanel, -1, ">")
            hbox.Add(btn, STRETCH, wx.EXPAND, BORDER )
            self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
                                       lambda e:self.skip(1), btn)
                                       #EventCaller(self.skip,1))

    def getStatus(self):
        return "%d/%d" % (self.currentPos,len(self.rpt))
    
    def refresh(self):
        if False:
            self.statusLabel.SetLabel(self.getStatus())
        
        

class TextViewer(base.TextViewer):

    def __init__(self,*args,**kw):
        base.TextViewer.__init__(self,*args,**kw)
        #self._buffer = ""
        self.wxctrl = None
        
##     def onShow(self):
##         c = console.Console(self.addText,self.addText,
##                             verbosity=console._syscon._verbosity)
##         console.push(c)
        
    def onClose(self):
##         console.pop()
        console = self.getForm().session.toolkit.console
        console.redirect(*self.redirect)
        self.wxctrl = None
        #self._buffer = ""
        #raise "it is no good idea to close this window"
    
    def setupTkinter(self,parentCtrl):
        parentFormCtrl = self.getForm().wxctrl
        console = self.getForm().session.toolkit.console
        e = wx.TextCtrl(parentCtrl,-1,console.getConsoleOutput(),
                        style=wx.TE_MULTILINE|wx.HSCROLL)
        e.SetBackgroundColour('BLACK')
        e.SetForegroundColour('WHITE')
        e.SetEditable(False)
        e.SetMinSize(e.GetBestSize())
        #_setEditorSize(e,MEMO(width=50,height=10))
        #e.SetEnabled(False)
        box.Add(e, STRETCH, wx.EXPAND|wx.ALL,NOBORDER)
        self.wxctrl = e
        self.wxctrl.SetInsertionPointEnd()
        #self.wxctrl.ShowPosition(-1)
        self.redirect = console.redirect(self.addText,self.addText)
        self.getForm().session.debug(
            str(e.GetMinSize())+" "+str(e.GetMaxSize()))

    def addText(self,s):
        self.wxctrl.WriteText(s)
        self.wxctrl.ShowPosition(-1)
##         if self.wxctrl is not None:
##             self.wxctrl.WriteText(s)
##             self.wxctrl.ShowPosition(-1)
##         else:
##             self._buffer += s
    
class Panel(base.Panel):

    def setupTkinter(self,parent):
        self.tixctrl = Tkinter.Frame(parent)
        
        for c in self._components:
            c.setupTkinter(self.tixctrl)
            
        self.tixctrl.pack()


def SwappedBoxSizer(box):
    if box.GetOrientation() == wx.VERTICAL:
        return wx.BoxSizer(wx.HORIZONTAL)
    else:
        return wx.BoxSizer(wx.VERTICAL)

class EntryMixin:

    def setupTkinter(self,panel):
        if self.hasLabel():
            mypanel = wx.Panel(panel,-1)
            mypanel.SetBackgroundColour(ENTRY_PANEL_BACKGROUND)
            box.Add(mypanel, self.weight, wx.EXPAND|wx.ALL,BORDER)
            hbox = SwappedBoxSizer(box)
            mypanel.SetSizer(hbox)

            if self.doc is not None:
                label = wx.Panel(mypanel,-1)
                label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer = SwappedBoxSizer(hbox)
                label.SetSizer(labelSizer)

                labelCtrl = wx.StaticText(
                    label,-1,self.getLabel(),style=wx.ALIGN_RIGHT)
                labelCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer.Add(labelCtrl,DONTSTRETCH,wx.EXPAND,BORDER)

                docCtrl = wx.StaticText(
                    label, -1,
                    "\n".join(docWrapper.wrap(self.doc)),
                    style=wx.ALIGN_LEFT)
                docCtrl.SetFont(ENTRY_DOC_FONT)
                docCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
                labelSizer.Add(docCtrl,DONTSTRETCH,wx.EXPAND,BORDER)

            else:
                label = wx.StaticText(mypanel, -1,
                                      self.getLabel(),
                                      style=wx.ALIGN_RIGHT)
                label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)

            if hbox.GetOrientation() == wx.HORIZONTAL:
                hbox.Add(
                    label, STRETCH,
                    wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL,
                    BORDER)
            else:
                hbox.Add(
                    label, DONTSTRETCH,
                    wx.ALIGN_LEFT,
                    BORDER)

            hbox.Add( (10,1), DONTSTRETCH,0,NOBORDER) # spacer
            
        else:
            mypanel = panel
            hbox = box

        type = self._type
        if isinstance(type,datatypes.StringType):
            style=0
            if self.getMaxHeight() > 1:
                style = style|wx.TE_MULTILINE
            editor = wx.TextCtrl(mypanel,-1,
                                 self.getValueForEditor(),
                                 style=style)
                                 #validator=EntryValidator(self))
                                 #style=wx.TE_PROCESS_ENTER)

            editor.SetMinSize(editor.GetBestSize())
            #_setEditorSize(editor,self)
        elif isinstance(type,datatypes.BoolType):
            editor=wx.CheckBox(mypanel,-1)
        #print editor.GetMinSize(), editor.GetMaxSize()
        #print mypanel.GetMinSize(), editor.GetMaxSize()
        
        #self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        #editor.Bind(wx.EVT_CHAR, self.EvtChar)
        #editor.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        #editor.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        #editor.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)

        self.editor = editor 
        if self.hasLabel():
            if hbox.GetOrientation() == wx.HORIZONTAL:
                hbox.Add(editor,STRETCH,
                         wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,
                         BORDER)
            else:
                hbox.Add(editor,DONTSTRETCH,
                         wx.ALIGN_LEFT,
                         BORDER)
            self.wxctrl = mypanel
        else:
            hbox.Add(editor,STRETCH,
                     wx.EXPAND|wx.ALL,NOBORDER)
            self.wxctrl = editor

    def refresh(self):
        if hasattr(self,'editor'):
            s = self.getValueForEditor()
            self.editor.SetValue(s)
        
    def setFocus(self):
        self.editor.SetFocus()
        self.editor.SetSelection(-1,-1)


    def store(self):
        #type = self._type
        #if isinstance(type,datatypes.StringType):
        if self.editor.IsModified():
            s = self.editor.GetValue()
            self.setValueFromEditor(s)
        
        
        
##         # on MS-Windows:
##         # killfocus can accur after the windows have been destroyed
##         # note: looks as if this is not necessary anymore
        
##         #if self.owner.dying: return
##         if self.editor.IsModified():
##             s = self.editor.GetValue()
##             self.setValueFromEditor(s)
##             evt.Skip()

            
class Entry(EntryMixin,base.Entry):
    pass

class DataEntry(EntryMixin,base.DataEntry):
    
    def setupTkinter(self,panel):
        EntryMixin.setup(self,panel,box)
        self.editor.SetEditable(self.enabled)
        
    def refresh(self):
        EntryMixin.refresh(self)
        base.DataEntry.refresh(self)
        self.editor.SetEditable(self.enabled)
        #if not self.enabled:
        #    print str(self), "is read-only"
    



## class Job(jobs.Job):
##     def status(self,msg,*args,**kw):
##         self._status = self.session.buildMessage(msg,*args,**kw)
##         self.refresh()

class Dialog(tkSimpleDialog.Dialog):
    pass

class NonmodalDialog(Tkinter.Toplevel):
    """
    A non-modal tkSimpleDialog.Dialog.
    Modified copy from tkSimpleDialog.py (Python 2.4):
    - does not grab focus
    - buttonbox is empty by default
    """
    def __init__(self, parent, title=None):
        Tkinter.Toplevel.__init__(self, parent)
        #self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.result=None

        body = Tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                      parent.winfo_rooty()+50))

        # self.initial_focus.focus_set()

        # self.mainloop()

    def buttonbox(self):
        pass
    
    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Tkinter.Toplevel.destroy(self)

    def cancel(self, event=None):
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass
        

class Form(base.Form):


    def __init__(self,*args,**kw):
        self.tixctrl = None
        base.Form.__init__(self,*args,**kw)


    def setParent(self,parent):
        assert self.tixctrl is None
        base.Form.setParent(self,parent)
        
    
    def setupTkinter(self):
        assert self.tixctrl is None
        if self._parent is None:
            parent = None
        else:
            parent = self._parent.tixctrl

        if self.modal:
            ctrl = Dialog(parent,title=self.getLabel())
        else:
            ctrl = NonmodalDialog(parent,
                                  title=self.getLabel())

        #self.tixctrl.title(self.getLabel())
        
        #print ctrl.__class__,'"%s"'%self.getLabel()
        
        if self.menuBar is not None:
            mbar = Tkinter.Menu(ctrl)
            ctrl.config(menu=mbar)
            
            for mnu in self.menuBar.menus:
                self._createMenuWidget(mbar,mnu)

        self.tixctrl=ctrl
        
        self.mainComp.setupTkinter(ctrl)
        
        
        #self.tixctrl.size(fill=BOTH,expand=1) 
            
        #self.wxctrl.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        #self.wxctrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        #wx.EVT_CHAR(self.wxctrl, self.OnChar)
        #wx.EVT_IDLE(self.wxctrl, self.OnIdle)
        #wx.EVT_SIZE(self.wxctrl, self.OnSize)
        #wx.EVT_CLOSE(self.wxctrl, self.OnCloseWindow)
        #wx.EVT_ICONIZE(self.wxctrl, self.OnIconfiy)
        #wx.EVT_MAXIMIZE(self.wxctrl, self.OnMaximize)

        
        #self.SetBackgroundColour(wx.RED)
        
        #mainBox = wx.BoxSizer(wx.VERTICAL)
        #mainBox=None
        
        
        #if self.defaultButton is not None:
        #    self.defaultButton.wxctrl.SetDefault()

        #self.wxctrl.SetSizerAndFit(mainBox)
        
        #self.mainBox = mainBox
        #self.wxctrl.SetAutoLayout(True) 
        #self.wxctrl.Layout()

##         if self.halign is gui.CENTER:
##             self.wxctrl.Centre(wx.HORIZONTAL)
##         if self.valign is gui.CENTER:
##             self.wxctrl.Centre(wx.VERTICAL)
            
##         x,y = self.wxctrl.GetPositionTuple()

##         if self.halign is gui.LEFT:
##             x = 0
##         elif self.halign is gui.RIGHT:
##             x = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
##             x -= self.wxctrl.GetSizeTuple()[0]
            
##         if self.valign is gui.TOP:
##             y = 0
##         elif self.halign is gui.RIGHT:
##             y = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
##             y -= self.wxctrl.GetSizeTuple()[1]

##         self.wxctrl.SetPosition((x,y))



    def _createMenuWidget(self,mbar,mnu):
        tixMenu = Tkinter.Menu(mbar)
        lbl,underline=menulabel(mnu.getLabel())
        mbar.add_cascade(label=lbl,menu=tixMenu,
                         underline=underline)
        for mi in mnu.items:
            lbl=mi.getLabel()
            
            doc = mi.getDoc()
            if doc is None:
                doc=""
            assert type(doc) == type(""), repr(mi)
            lbl = mi.getLabel()
            if mi.accel is not None:
                lbl += "\t" + mi.accel
                
            lbl,underline=menulabel(lbl)
            #underline=lbl.index('&')
            #lbl=lbl.replace('&','')
            tixMenu.add_command(label=lbl,
                                command=mi.click,
                                underline=underline)
                


    
    def close(self):
        if self.isShown():
            self.tixctrl.destroy()

    def isShown(self):
        return (self.tixctrl is not None)


    def OnCloseWindow(self, event):
        #self.dying = True
        # http://wiki.wxpython.org/index.cgi/Surviving_20with_20wxEVT_5fKILL_5fFOCUS_20under_20Microsoft_20Windows
        # Surviving with EVT_KILL_FOCUS under Microsoft Windows
        
        #self.window = None
        #self.mainMenu = None
        #if hasattr(self, "tbicon"):
        #   del self.tbicon
        self.onClose()
        self.tixctrl.destroy()
        self.tixctrl = None

    def refresh(self):
        base.Form.refresh(self)
        self.tixctrl.refresh()


#tx -> tix
#Toolkit.wxapp -> root
#.wxctrl -> tixctrl
#Task.wxctrl -> tixMeter

class Toolkit(base.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    panelFactory = Panel
    dataGridFactory = DataGrid
    navigatorFactory = DataForm
    formFactory = Form
    
    def __init__(self,*args,**kw):
        base.Toolkit.__init__(self,*args,**kw)
        self._session=None
        #self.root = None
        #self._activeForm=None



    def showStatus(self,sess,msg):
        frm=sess._activeForm
        if frm is None or frm.modal:
            base.Toolkit.showStatus(self,sess,msg)
            #syscon.status(msg,*args,**kw)
        else:
            frm.tixctrl.SetStatusText(msg)

    def onTaskBegin(self,task):
        assert task.session._activeForm is not None
        if task.session.statusMessage is None:
            stm=""
        else:
            stm=task.session.statusMessage
            
        task.tixMeter = Tix.Meter(
            task.session._activeForm.tixctrl,
            label=task.label,
            text=stm,
            value=100)


    def onTaskStatus(self,task):
        if task.tixMeter is None: return
        pc = task.percentCompleted
        if pc is None: pc = 0
        msg=task.session.statusMessage
        if msg is None: msg=''
        if not task.tixMeter.Update(value=pc,text=msg):
            task.requestAbort()
        
    def onTaskIncrement(self,task):
        self.onTaskStatus(task)

    def onTaskBreathe(self,task):
        self.run_awhile()
        
    def onTaskResume(self,task):
        if task.tixMeter is None: return
        task.tixMeter.Resume()
        
    def onTaskDone(self,task):
        task.tixMeter.Update(value=100,text='')
        #task.tixMeter.Destroy()
        task.tixMeter = None

    def onTaskAbort(self,task,*args,**kw):
        #task.wxctrl.Destroy()
        task.tixMeter = None

            
    def running(self):
        #return self._running # self.wxapp is not None
        return self._session is not None

    def run_awhile(self):
        assert self.running()
        pass
        #while self.wxapp.Pending():
        #    self.wxapp.Dispatch()

    def stopRunning(self):
        Tkinter._tkroot.destroy()
        
    def run_forever(self,sess):
        #if not self._setup:
        #    self.setup()
        assert not self.running()
        #self._running = True
        self._session=sess
        self.root = Tkinter.Tk()
        self.root.title("console")
        self.root.iconify()
        self.showMainForm()
        #self.root.mainloop()
        Tkinter.mainloop()

    def showMainForm(self):
        self._session.showMainForm()
        #sess.db.app.showMainForm(sess)

    def showForm(self,frm):
        frm.setupTkinter()

        
    def refreshForm(self,frm):
        pass

    
