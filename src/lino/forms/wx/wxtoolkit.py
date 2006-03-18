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
from lino.forms import toolkit

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
        

class Label(toolkit.Label):
    
    def wxsetup(self,form,panel,box):
        text = self.getLabel()
        if self.getDoc() is not None:
            text += '\n' + self.getDoc()
        ctrl = wx.StaticText(panel,-1, text)
        box.Add(ctrl, DONTSTRETCH, wx.EXPAND|wx.ALL, BORDER)
        self.wxctrl = ctrl
                
class Button(toolkit.Button):
    
##     def __repr__(self):
##         return "Button %s %s at %s" % (
##             self.getLabel(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
    def wxsetup(self,form,panel,box):
        #parentFormCtrl = self.getForm().ctrl
        #winId = wx.NewId()
        btn = wx.Button(panel,-1,self.getLabel(),
                        wx.DefaultPosition,
                        wx.DefaultSize)
        #btn.SetBackgroundColour('YELLOW')
        #parentFormCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
        panel.Bind(wx.EVT_BUTTON,
                   EventCaller(self.click),
                   btn)
##         if self.hotkey is not None:
##             #print 'Button.wxsetup', self.hotkey
##             wx.EVT_CHAR(panel, self.EVT_CHAR)
##             #form.Bind(wx.EVT_KEY_DOWN,self.EVT_CHAR)
        if self.doc is not None:
            btn.SetToolTipString(self.doc)

        box.Add(btn,DONTSTRETCH,0,NOBORDER) #, 0, wx.CENTER,10)
        self.wxctrl = btn

##     def EVT_CHAR(self,evt):
##         print "Button.EVT_CHAR"
##         if self.hotkey.match_wx(evt):
##             self.click()
##             return
##         evt.Skip()

    def setFocus(self):
        self.wxctrl.SetFocus()

class DataGrid(toolkit.DataGrid):
    
    def wxsetup(self,form,parent,box):
        #print "wxsetup()", self
        self.wxctrl = wxgrid.DataGridCtrl(parent,self)
        box.Add(self.wxctrl, STRETCH, wx.EXPAND,BORDER)
        
    def refresh(self):
        self.wxctrl.refresh()

    def getSelectedRows(self):
        return self.wxctrl.getSelectedRows()

        
## class DataForm(toolkit.DataForm):
    
##     def wxsetup(self,frm,parent,box):
##         if False:
##             mypanel = wx.Panel(parent,-1)
##             box.Add(mypanel, STRETCH, wx.EXPAND|wx.ALL,BORDER)

##             #hbox = wx.BoxSizer(wx.HORIZONTAL)
##             hbox=SwappedBoxSizer(box)
##             mypanel.SetSizer(hbox)
##             self.wxctrl = mypanel


##             self.statusLabel = wx.StaticText( mypanel, -1,
##                                               self.getStatus())
##             hbox.Add(self.statusLabel, STRETCH, wx.EXPAND, BORDER )

##             hbox.Add( (10,1), DONTSTRETCH,0,NOBORDER)

##             btn = wx.Button(mypanel, -1, "<")
##             hbox.Add(btn, STRETCH, wx.EXPAND, BORDER )
##             self.getForm().ctrl.Bind(wx.EVT_BUTTON,
##                                      EventCaller(self.skip,-1),
##                                      btn)

##             btn = wx.Button(mypanel, -1, ">")
##             hbox.Add(btn, STRETCH, wx.EXPAND, BORDER )
##             self.getForm().ctrl.Bind(wx.EVT_BUTTON,
##                                      EventCaller(self.skip,1),
##                                      btn)
##             self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
##                                        lambda e:self.skip(1), btn)
##                                        #EventCaller(self.skip,1))

    #def getStatus(self):
    #    return "%d/%d" % (self.currentPos,len(self.rpt))
    
##     def refresh(self):
##         if False:
##             self.statusLabel.SetLabel(self.getStatus())
        
        

class TextViewer(toolkit.TextViewer):

    def __init__(self,*args,**kw):
        toolkit.TextViewer.__init__(self,*args,**kw)
        #self._buffer = ""
        self.wxctrl = None
        
##     def onShow(self):
##         c = console.Console(self.addText,self.addText,
##                             verbosity=console._syscon._verbosity)
##         console.push(c)
        
    def onClose(self):
##         console.pop()
        console = self.getForm().toolkit.console
        console.redirect(*self.redirect)
        self.wxctrl = None
        #self._buffer = ""
        #raise "it is no good idea to close this window"
    
    def wxsetup(self,form,panel,box):
        #parentFormCtrl = self.getForm().wxctrl
        console = form.toolkit.console
        e = wx.TextCtrl(panel,-1,console.getConsoleOutput(),
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
    
## class Panel(toolkit.Panel):

##     def __repr__(self):
##         s = "%s %s at %s (" % (
##             self.getName(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
##         for c in self._components:
##             s += "\n- " + ("\n  ".join(repr(c).splitlines()))
##         s += "\n)"
##         return s
    
##     def wxsetup(self,form,parent,box):
##         mypanel = wx.Panel(parent,-1)
##         box.Add(mypanel, self.weight, wx.ALL|wx.EXPAND,NOBORDER)
##         if self.direction == forms.VERTICAL:
##             mybox = wx.BoxSizer(wx.VERTICAL)
##         else:
##             mybox = wx.BoxSizer(wx.HORIZONTAL)
##         mypanel.SetSizer(mybox)
        
##         self.mybox = mybox # store reference to avoid crash?
##         self.wxctrl = mypanel
        
##         for c in self._components:
##             c.wxsetup(form,mypanel,mybox)

class Panel(toolkit.Panel):

    def wxsetup(self,form,parent,box):
        #print self,"wxsetup()"
        mypanel = wx.Panel(parent,-1)
        box.Add(mypanel, self.weight, wx.ALL|wx.EXPAND,NOBORDER)
        if self.direction == forms.VERTICAL:
            mybox = wx.BoxSizer(wx.VERTICAL)
        else:
            mybox = wx.BoxSizer(wx.HORIZONTAL)
        mypanel.SetSizer(mybox)
        
        self.mybox = mybox # store reference to avoid crash?
        self.wxctrl = mypanel
        
        for c in self._components:
            c.wxsetup(form,mypanel,mybox)

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

    def wxsetup(self,form,panel,box):
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

        type = self.getType()
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
            v=self.getValue()
            if v is None:
                v=self.getType().defaultValue
            editor.SetValue(v)
            
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

##     def EVT_CHAR(self, evt):
##         print "EVT_CHAR ", self, evt.GetKeyCode()
##         if evt.GetKeyCode() == 27: return
##         evt.Skip()

    def getValueForEditor(self):
        "return current value as string"
        v = self.getValue()
        if v is None:
            return self.getType().defaultValue
        if isinstance(self.getType(),datatypes.StringType):
            return self.format(v)
        return v

    def setValueFromEditor(self,x):
        "convert the string and store it as raw value"
        if isinstance(self.getType(),datatypes.StringType):
            if len(x) == 0:
                self.setValue(None)
            else:
                self.setValue(self.parse(x))
        else:
            self.setValue(x)
            
    def refresh(self):
        if hasattr(self,'editor'):
            x = self.getValueForEditor()
            self.editor.SetValue(x)
        
    def setFocus(self):
        self.editor.SetFocus()
        self.editor.SetSelection(-1,-1)
        
    def isDirty(self):
        if isinstance(self.getType(),datatypes.StringType):
            return self.editor.IsModified()
        return False

    def store(self):
        #type = self._type
        #if isinstance(type,datatypes.StringType):
        if self.isDirty():
            s = self.editor.GetValue()
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
    
    def wxsetup(self,form,panel,box):
        EntryMixin.wxsetup(self,form,panel,box)
        self.editor.SetEditable(self.enabled)
        
    def refresh(self):
        EntryMixin.refresh(self)
        toolkit.DataEntry.refresh(self)
        self.editor.SetEditable(self.enabled)
        #if not self.enabled:
        #    print str(self), "is read-only"
    



## class Job(jobs.Job):
##     def status(self,msg,*args,**kw):
##         self._status = self.session.buildMessage(msg,*args,**kw)
##         self.refresh()
    
        


class WxApp(wx.App):

    def __init__(self,app):
        self.app = app
        wx.App.__init__(self,0)


    def OnInit(self):
        
        # wx.App.OnInit(self)        
        # Notice that if you want to to use the command line
        # processing provided by wxWidgets you have to call the base
        # class version in the derived class OnInit().
        
        wx.InitAllImageHandlers()
        #self.toolkit.wxinit()
        #self.toolkit.showMainForm()
        return True

    def OnExit(self):
        #center.shutdown()
        pass



class Toolkit(toolkit.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    hpanelFactory = HPanel
    vpanelFactory = VPanel
    dataGridFactory = DataGrid
    #navigatorFactory = DataForm
    #formFactory = Form
    #jobFactory=jobs.Job
    #progresserFactory=Progresser
    
##     def __init__(self,*args,**kw):
##         toolkit.Toolkit.__init__(self,*args,**kw)
##         #self.consoleForm = None
##         #self._setup = False
##         #self._running = False
##         #self.applicationBeingRun=None
##         self.wxapp = None
##         #self._activeForm=None





##     def createCompCtrl(self,comp,parent,box):
        
##         if comp.__class__ is toolkit.Label:
##             text = comp.getLabel()
##             if comp.getDoc() is not None:
##                 text += '\n' + comp.getDoc()
##             ctrl = wx.StaticText(parent,-1, text)
##             box.Add(ctrl, DONTSTRETCH, wx.EXPAND|wx.ALL, BORDER)
##             comp.ctrl = ctrl
##             return
        
##         if comp.__class__ is toolkit.Button:
##             def setFocus(self):
##                 self.wxctrl.SetFocus()
##                 # where to put this?

##             formCtrl = comp.getForm().ctrl
##             btn = wx.Button(parent,-1,comp.getLabel(),
##                             wx.DefaultPosition,
##                             wx.DefaultSize)
##             #btn.SetBackgroundColour('YELLOW')
##             #formCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
##             formCtrl.Bind(wx.EVT_BUTTON,
##                           EventCaller(comp.click),
##                           btn)
##             if comp.doc is not None:
##                 btn.SetToolTipString(comp.doc)

##             box.Add(btn,DONTSTRETCH,0,NOBORDER) #, 0, wx.CENTER,10)
##             comp.ctrl = btn
##             return









            
        
    def createFormCtrl(self,frm):
        parent=frm._parent
        if parent is None:
            parent=self.getActiveForm()
        if parent is None:
            wxparent = None
        else:
            wxparent = parent.ctrl
            
        #self.dying = False
        
        if frm.modal:
            ctrl = wx.Dialog(wxparent,-1,frm.getTitle(),
                             style=wx.DEFAULT_FRAME_STYLE|
                             wx.NO_FULL_REPAINT_ON_RESIZE)
        else:
            ctrl = wx.Frame(wxparent,-1,frm.getTitle(),
                            style=wx.DEFAULT_FRAME_STYLE|
                            wx.NO_FULL_REPAINT_ON_RESIZE|
                            wx.TAB_TRAVERSAL)
                                   
            ctrl.CreateStatusBar(1, wx.ST_SIZEGRIP)
            
            if frm.menuBar is not None:
                wxMenuBar = wx.MenuBar()
                for mnu in frm.menuBar.menus:
                    wxm = self._createMenuWidget(ctrl,mnu)
                    wxMenuBar.Append(wxm,mnu.getLabel())

                ctrl.SetMenuBar(wxMenuBar)

            
        ctrl.Bind(wx.EVT_SET_FOCUS, frm.onSetFocus)
        ctrl.Bind(wx.EVT_KILL_FOCUS, frm.onKillFocus)

        def flags(key):
            if key.shift: return wx.ACCEL_SHIFT
            if key.alt: return wx.ACCEL_ALT
            if key.ctrl: return wx.ACCEL_CTRL
            return wx.ACCEL_NORMAL


        #wx.EVT_CHAR(ctrl, self.EVT_CHAR)
        #wx.EVT_SIZE(ctrl, self.OnSize)
        wx.EVT_CLOSE(ctrl, frm.close)
        #wx.EVT_ICONIZE(ctrl, self.OnIconfiy)
        #wx.EVT_MAXIMIZE(ctrl, self.OnMaximize)

        
        #self.SetBackgroundColour(wx.RED)
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        
        #self.createCompCtrl(frm.mainComp,ctrl,mainBox)
        frm.mainComp.wxsetup(ctrl,ctrl,mainBox)
        
        if frm.defaultButton is not None:
            frm.defaultButton.wxctrl.SetDefault()

        if len(frm.accelerators):
            l=[ (flags(key),
                 key.keycode,
                 btn.wxctrl.GetId()) for key,btn in frm.accelerators]
            ctrl.SetAcceleratorTable(wx.AcceleratorTable(l))

            

        ctrl.SetSizerAndFit(mainBox)
        #self.mainBox = mainBox
        #self.wxctrl.SetAutoLayout(True) 
        #self.wxctrl.Layout()

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




    def _createMenuWidget(self,ctrl,mnu):
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
            wx.EVT_MENU(ctrl, winId,
                        EventCaller(mi.click))
        return wxMenu

    
    def executeShow(self,frm):
        if frm.modal:
            frm.ctrl.ShowModal()
        else:
            frm.ctrl.Show()

    def executeRefresh(self,frm):
        frm.ctrl.Refresh()

    def closeForm(self,frm,evt):
        #print "closeForm()"
        frm.ctrl.Destroy()


##     def EVT_CHAR(self, evt):
##         print "OnChar "+str(evt)
##         evt.Skip()


    def onIdle(self, evt):
        #self.onIdle()
        #wx.LogMessage("onIdle")
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





    def show_status(self,sess,msg):
        #frm=sess._activeForm
        frm=self.getActiveForm()
        while frm is not None and frm.modal:
            frm=frm._parent
        if frm is None:
            #base.Toolkit.showStatus(self,sess,msg)
            self.console.show_status(sess,msg)
        else:
            frm.ctrl.SetStatusText(msg)

    def onTaskBegin(self,task):
        #assert self.progressDialog is None
        #print job
        assert self._activeForm is not None
        title=""
##         if task.statusMessage is None:
##             stm=""
##         else:
##             stm=task.statusMessage
            
        task.wxctrl = wx.ProgressDialog(
            title,task.getStatusLine(),
            100,
            self._activeForm.ctrl,
            wx.PD_CAN_ABORT)#|wx.PD_ELAPSED_TIME)
        #return self.app.toolkit.console.onJobInit(job)

    def onTaskBreathe(self,task):
        if task.wxctrl is None: return
        pc = task.percentCompleted
        #if pc is None: pc = 0
        msg=task.getStatusLine()
        #if msg is None: msg=''
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

    
            
    def run_awhile(self):
        assert self.running()
        while self.root.ctrl.Pending():
            self.root.ctrl.Dispatch()

            #print self.wxctrl.Yield(False)
        #return self._abortRequested

##     def setup(self):
##         self._setup = True
##         self.init()
        
    def start_running(self,app):
        toolkit.Toolkit.start_running(self,app)
        self.root.ctrl = WxApp(self)
        #wx.EVT_IDLE(self.wxapp, self.onIdle)
        
    def run_forever(self,*args,**kw):
        assert self.running()
        #self.args=args
        #self.kw=kw
        #if not self._setup:
        #    self.setup()
        #assert not self.running()
        #self._running = True
        self.root.ctrl.MainLoop()

    #def showMainForm(self):
##     def wxinit(self):
##         raise "no longer used"
##         for a in self.apps:
##             a.run(*self.args,**self.kw)
##         for frm in self._submitted:
##             self.show_form(frm)
##         #sess.db.app.showMainForm(sess)

        
    
    def stop_running(self):
        wx.Exit()
        
