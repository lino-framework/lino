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


import wx

#from lino.ui import console
from lino.adamo.exceptions import InvalidRequestError

from lino.adamo import datatypes
#from lino.adamo.datatypes import MEMO
from lino import forms
from lino.forms import base

#from lino.forms import constants gui
from lino.forms.wx import wxgrid
#from lino.console import syscon
#from lino.forms.wx.showevents import showEvents
#from lino.misc import jobs

STRETCH = 1
DONTSTRETCH=0

BORDER=10
NOBORDER=0

ENTRY_DOC_FONT = wx.SMALL_FONT
ENTRY_PANEL_BACKGROUND = None
ENTRY_LABEL_BACKGROUND = None
#ENTRY_PANEL_BACKGROUND = wx.BLUE
#ENTRY_LABEL_BACKGROUND = wx.GREEN

from textwrap import TextWrapper
docWrapper = TextWrapper(30)


def _setEditorSize(editor,type):

    #print type
    #LINEHEIGHT = 10
    #CHARWIDTH = 10
        
    #CHARWIDTH = LINEHEIGHT = editor.GetFont().GetPointSize()
    #CHARWIDTH, LINEHEIGHT = editor.GetTextExtent("M")
    #print editor.GetFullTextExtent("M"), editor.GetTextExtent("M")
    #print editor.GetBestSize()
    
    #CHARWIDTH *= 2
        
    #editor.SetMaxSize( (type.maxWidth*CHARWIDTH,
    #                    type.maxHeight*LINEHEIGHT) )
    #editor.SetMinSize( (type.minWidth*CHARWIDTH,
    #                    type.minHeight*LINEHEIGHT) )
    
    editor.SetMinSize(editor.GetBestSize())


class EventCaller:
    
    def __init__(self,meth,*args,**kw):
        self.meth = meth
        self.args = args
        self.kw = kw
        
    def __call__(self,event):
        return self.meth(*self.args, **self.kw)
##         try:
##             return self.meth(*self.args, **self.kw)
##         except InvalidRequestError,e:
##             frm.session.status(str(e))
##         except Exception,e:
##             frm.session.exception(
##                 e,"after clicking '%s' in '%s'" % (
##                 self.getLabel(),frm.getLabel()))
        


## class EntryValidator(wx.PyValidator):
    
##     def __init__(self,entry):
##         wx.PyValidator.__init__(self)
##         self._entry = entry
        
##     def Clone(self):
##         print "Clone"
##         return self.__class__(self._entry)

##     def TransferToWindow(self):
##         s = self._entry.getValue()
##         self.GetWindow().SetValue(s)
##         return True

##     def TransferFromWindow( self ): 
##         s = self.GetWindow().GetValue()
##         self._entry.setValue(s)
##         return True     

            
## class Component:
    
##     def __repr__(self):
##         return "%s %s at %s" % (
##             self.getName(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        

class Label(base.Label):
    
    def setup(self,panel,box):
        text = self.getLabel()
        if self.getDoc() is not None:
            text += '\n' + self.getDoc()
        ctrl = wx.StaticText(panel,-1, text)
        box.Add(ctrl, DONTSTRETCH, wx.EXPAND|wx.ALL, BORDER)
        self.wxctrl = ctrl
                
class Button(base.Button):
    
##     def __repr__(self):
##         return "Button %s %s at %s" % (
##             self.getLabel(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
    def setup(self,parentCtrl,box):
        parentFormCtrl = self.getForm().wxctrl
        #winId = wx.NewId()
        btn = wx.Button(parentCtrl,-1,self.getLabel(),
                        wx.DefaultPosition,
                        wx.DefaultSize)
        #btn.SetBackgroundColour('YELLOW')
        #parentFormCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
        parentFormCtrl.Bind(wx.EVT_BUTTON,
                            EventCaller(self.click),
                            btn)
        if self.doc is not None:
            btn.SetToolTipString(self.doc)

        box.Add(btn,DONTSTRETCH,0,NOBORDER) #, 0, wx.CENTER,10)
        self.wxctrl = btn

    def setFocus(self):
        self.wxctrl.SetFocus()

class DataGrid(base.DataGrid):
    
    def setup(self,parent,box):
        self.wxctrl = wxgrid.DataGridCtrl(parent,self)
        box.Add(self.wxctrl, STRETCH, wx.EXPAND,BORDER)
        
    def refresh(self):
        self.wxctrl.refresh()

    def getSelectedRows(self):
        return self.wxctrl.getSelectedRows()

        
class DataForm(base.DataForm):
    
    def setup(self,parent,box):
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
                                       EventCaller(self.skip,-1),
                                       btn)

            btn = wx.Button(mypanel, -1, ">")
            hbox.Add(btn, STRETCH, wx.EXPAND, BORDER )
            self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
                                       EventCaller(self.skip,1),
                                       btn)
##             self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
##                                        lambda e:self.skip(1), btn)
##                                        #EventCaller(self.skip,1))

    #def getStatus(self):
    #    return "%d/%d" % (self.currentPos,len(self.rpt))
    
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
    
    def setup(self,parentCtrl,box):
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

##     def __repr__(self):
##         s = "%s %s at %s (" % (
##             self.getName(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
##         for c in self._components:
##             s += "\n- " + ("\n  ".join(repr(c).splitlines()))
##         s += "\n)"
##         return s
    
    def setup(self,parent,box):
        mypanel = wx.Panel(parent,-1)
        box.Add(mypanel, self.weight, wx.ALL|wx.EXPAND,NOBORDER)
        if self.direction == self.VERTICAL:
            mybox = wx.BoxSizer(wx.VERTICAL)
        else:
            mybox = wx.BoxSizer(wx.HORIZONTAL)
        mypanel.SetSizer(mybox)
        
        self.mybox = mybox # store reference to avoid crash?
        self.wxctrl = mypanel
        
        for c in self._components:
            c.setup(mypanel,mybox)


def SwappedBoxSizer(box):
    if box.GetOrientation() == wx.VERTICAL:
        return wx.BoxSizer(wx.HORIZONTAL)
    else:
        return wx.BoxSizer(wx.VERTICAL)

class EntryMixin:

    def setup(self,panel,box):
        if self.hasLabel():
            mypanel = wx.Panel(panel,-1)
            mypanel.SetBackgroundColour(ENTRY_PANEL_BACKGROUND)
            box.Add(mypanel, self.weight, wx.EXPAND|wx.ALL,BORDER)
            #hbox = wx.BoxSizer(wx.HORIZONTAL)
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
    
    def setup(self,panel,box):
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
    
        

class Form(base.Form):

##     def afterShow(self):
##         console.debug(repr(self.mainComp))
##         #for ctrl in self._wxFrame.GetChildren():
##         #    print repr(ctrl)
##             #print ctrl.GetSize()
##             #print ctrl.GetPosition()
##         if self._parent is None:
##             self.app.SetTopWindow(self.wxctrl)
##             self.app.MainLoop()

    def __init__(self,*args,**kw):
        #self.progressDialog = None
        self.wxctrl = None
        base.Form.__init__(self,*args,**kw)


    def setParent(self,parent):
        assert self.wxctrl is None
        base.Form.setParent(self,parent)
        
##     def job(self,*args,**kw):
##         job = jobs.Job()
##         job.init(self,*args,**kw)
##         return job
    
    def setup(self):
        assert self.wxctrl is None
        base.Form.setup(self)
        #self.setupMenu()
        parent=self._parent
        if parent is None:
            parent=self.session.toolkit._activeForm
        if parent is None:
            wxparent = None
        else:
            wxparent = parent.wxctrl
            
        #self.dying = False
        
        if self.modal:
            self.wxctrl = wx.Dialog(wxparent,-1,self.getLabel(),
                                    style=wx.DEFAULT_FRAME_STYLE|
                                    wx.NO_FULL_REPAINT_ON_RESIZE)
        else:
            self.wxctrl = wx.Frame(wxparent,-1,self.getLabel(),
                                   style=wx.DEFAULT_FRAME_STYLE|
                                   wx.NO_FULL_REPAINT_ON_RESIZE|
                                   wx.TAB_TRAVERSAL)
                                   
            self.wxctrl.CreateStatusBar(1, wx.ST_SIZEGRIP)
            
            if self.menuBar is not None:
                wxMenuBar = wx.MenuBar()
                for mnu in self.menuBar.menus:
                    wxm = self._createMenuWidget(mnu)
                    wxMenuBar.Append(wxm,mnu.getLabel())

                self.wxctrl.SetMenuBar(wxMenuBar)
            
        self.wxctrl.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.wxctrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        wx.EVT_CHAR(self.wxctrl, self.OnChar)
        wx.EVT_IDLE(self.wxctrl, self.OnIdle)
        #wx.EVT_SIZE(self.wxctrl, self.OnSize)
        wx.EVT_CLOSE(self.wxctrl, self.OnCloseWindow)
        #wx.EVT_ICONIZE(self.wxctrl, self.OnIconfiy)
        #wx.EVT_MAXIMIZE(self.wxctrl, self.OnMaximize)

        
        #self.SetBackgroundColour(wx.RED)
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        
        self.mainComp.setup(self.wxctrl,mainBox)
        
        if self.defaultButton is not None:
            self.defaultButton.wxctrl.SetDefault()

        self.wxctrl.SetSizerAndFit(mainBox)
        #self.mainBox = mainBox
        #self.wxctrl.SetAutoLayout(True) 
        #self.wxctrl.Layout()

        if self.halign is forms.CENTER:
            self.wxctrl.Centre(wx.HORIZONTAL)
        if self.valign is forms.CENTER:
            self.wxctrl.Centre(wx.VERTICAL)
            
        x,y = self.wxctrl.GetPositionTuple()

        if self.halign is forms.LEFT:
            x = 0
        elif self.halign is forms.RIGHT:
            x = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
            x -= self.wxctrl.GetSizeTuple()[0]
            
        if self.valign is forms.TOP:
            y = 0
        elif self.halign is forms.RIGHT:
            y = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
            y -= self.wxctrl.GetSizeTuple()[1]

        self.wxctrl.SetPosition((x,y))




    def _createMenuWidget(self,mnu):
        wxMenu = wx.Menu()
        for mi in mnu.items:
            #print repr(mi.getLabel())
            #"%s must be a String" % repr(mi.getLabel())
            winId = wx.NewId()
            doc = mi.getDoc()
            if doc is None:
                doc=""
            assert type(doc) == type(""), repr(mi)
            lbl = mi.getLabel()
            if mi.accel is not None:
                lbl += "\t" + mi.accel
            wxMenu.Append(winId,lbl,doc)
            wx.EVT_MENU(self.wxctrl, winId,
                        EventCaller(mi.click))
        return wxMenu

    
    def close(self):
        if self.isShown():
            self.wxctrl.Close()

    def isShown(self):
        return (self.wxctrl is not None)


    def OnCloseWindow(self, event):
        #self.dying = True
        # http://wiki.wxpython.org/index.cgi/Surviving_20with_20wxEVT_5fKILL_5fFOCUS_20under_20Microsoft_20Windows
        # Surviving with EVT_KILL_FOCUS under Microsoft Windows
        
        #self.window = None
        #self.mainMenu = None
        #if hasattr(self, "tbicon"):
        #   del self.tbicon
        self.onClose()
        self.wxctrl.Destroy()
        self.wxctrl = None

    def OnKillFocus(self,evt):
        self.session.toolkit._activeForm = self._parent
        
    def OnSetFocus(self,evt):
        self.session.toolkit.setActiveForm(self)


    def OnChar(self, evt):
        self.session.debug("OnChar "+str(evt))


    def OnIdle(self, evt):
        self.onIdle()
        #wx.LogMessage("OnIdle")
        evt.Skip()

##     def OnIconfiy(self, evt):
##         wx.LogMessage("OnIconfiy")
##         evt.Skip()

##     def OnMaximize(self, evt):
##         wx.LogMessage("OnMaximize")
##         evt.Skip()
        
    def OnSize(self, evt):
        wx.LogMessage("OnSize")
        evt.Skip()

    def refresh(self):
        base.Form.refresh(self)
        self.wxctrl.Refresh()


class WxApp(wx.App):

    def __init__(self,toolkit):
        self.toolkit = toolkit
        wx.App.__init__(self,0)


    def OnInit(self):
        
        # wx.App.OnInit(self)        
        # Notice that if you want to to use the command line
        # processing provided by wxWidgets you have to call the base
        # class version in the derived class OnInit().
        
        wx.InitAllImageHandlers()
        #self.toolkit.init()
        self.toolkit.showMainForm()
        return True

    def OnExit(self):
        #center.shutdown()
        pass



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
    #jobFactory=jobs.Job
    #progresserFactory=Progresser
    
    def __init__(self,*args,**kw):
        base.Toolkit.__init__(self,*args,**kw)
        #self.consoleForm = None
        #self._setup = False
        #self._running = False
        self._activeForm=None
        self._session=None
        self.wxapp = None
        #self._activeForm=None


    def setActiveForm(self,frm):
        self._activeForm = frm


    def showStatus(self,sess,msg):
        #frm=sess._activeForm
        frm=self._activeForm
        while frm is not None and frm.modal:
            frm=frm._parent
        if frm is None:
            #base.Toolkit.showStatus(self,sess,msg)
            self.console.showStatus(sess,msg)
        else:
            frm.wxctrl.SetStatusText(msg)

    def onTaskBegin(self,task):
        #assert self.progressDialog is None
        #print job
        assert self._activeForm is not None
        if task.session.statusMessage is None:
            stm=""
        else:
            stm=task.session.statusMessage
            
        task.wxctrl = wx.ProgressDialog(
            task.label,stm,
            100,
            self._activeForm.wxctrl,
            wx.PD_CAN_ABORT)#|wx.PD_ELAPSED_TIME)
        #return self.app.toolkit.console.onJobInit(job)

    def onTaskBreathe(self,task):
        if task.wxctrl is None: return
        pc = task.percentCompleted
        if pc is None: pc = 0
        msg=task.session.statusMessage
        if msg is None: msg=''
        if not task.wxctrl.Update(pc,msg):
            task.requestAbort()
        self.run_awhile()
        
    def onTaskIncrement(self,task):
        self.onTaskBreathe(task)

##     def onTaskStatus(self,task):
##         if task.wxctrl is None: return
##         pc = task.percentCompleted
##         if pc is None: pc = 0
##         msg=task.session.statusMessage
##         if msg is None: msg=''
##         if not task.wxctrl.Update(pc,msg):
##             task.requestAbort()
        
##     def onTaskBreathe(self,task):
##         self.run_awhile()
        
##     def onTaskIncrement(self,task):
##         self.onTaskStatus(task)

    def onTaskResume(self,task):
        if task.wxctrl is None: return
        task.wxctrl.Resume()
        
    def onTaskDone(self,task):
        task.wxctrl.Update(100,'')
        task.wxctrl.Destroy()
        task.wxctrl = None

    def onTaskAbort(self,task,*args,**kw):
        task.wxctrl.Destroy()
        task.wxctrl = None

##     def onJobInit(self,job):
##         #assert self.progressDialog is None
##         #print job
##         assert self._activeForm is not None
##         job.wxctrl = wx.ProgressDialog(
##             job.getLabel(),
##             job.getStatus(),
##             100,
##             self._activeForm.wxctrl,
##             wx.PD_CAN_ABORT)#|wx.PD_ELAPSED_TIME)
##         #return self.app.toolkit.console.onJobInit(job)

##     def onJobRefresh(self,job):
##         self.run_awhile()
##         pc = job.pc
##         if pc is None:
##             pc = 0
##         if job.wxctrl is None:
##             return
##         if not job.wxctrl.Update(pc,job.getStatus()):
##             if job.confirmAbort():
##                 raise jobs.JobAborted(job)
##                 #job.abort()
##             else:
##                 job.wxctrl.Resume()

##     def onJobDone(self,job,msg):
##         if msg is None:
##             msg=""
##         job.wxctrl.Update(100,msg)
##         job.wxctrl.Destroy()
##         job.wxctrl = None
##         #return self.app.toolkit.console.onJobDone(*args,**kw)

##     def onJobAbort(self,job,*args,**kw):
##         job.wxctrl.Destroy()
##         job.wxctrl = None
##         #return self.app.toolkit.console.onJobAbort(*args,**kw)

    
            
    def running(self):
        #return self._running # self.wxapp is not None
        return self._session is not None

    def run_awhile(self):
        assert self.running()
        while self.wxapp.Pending():
            self.wxapp.Dispatch()

            #print self.wxctrl.Yield(False)
        #return self._abortRequested

##     def setup(self):
##         self._setup = True
##         self.init()
        
    def stopRunning(self):
        wx.Exit()
        
    def run_forever(self,sess):
        #if not self._setup:
        #    self.setup()
        assert not self.running()
        #self._running = True
        self._session=sess
        self.wxapp = WxApp(self)
        self.wxapp.MainLoop()

    def showMainForm(self):
        self._session.showMainForm()
        #sess.db.app.showMainForm(sess)

    def showForm(self,frm):
        if frm.modal:
            frm.wxctrl.ShowModal()
        else:
            frm.wxctrl.Show()

        
    
