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


import wx

from lino.ui import console

from lino.forms import base
from lino.forms.wx import wxgrid

WEIGHT = 1

ENTRY_PANEL_BACKGROUND = wx.GREEN
ENTRY_LABEL_BACKGROUND = wx.GREEN

from textwrap import TextWrapper
docWrapper = TextWrapper(30)



class EventCaller:
    def __init__(self,meth,*args,**kw):
        self.meth = meth
        self.args = args
        self.kw = kw
    def __call__(self,event):
        return self.meth(*self.args, **self.kw)


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

            
class WxApp(wx.App):

    def __init__(self):
        wx.App.__init__(self,0)


    def OnInit(self):
        wx.InitAllImageHandlers()
        #center.onBeginGUI(self)
        return True

    def OnExit(self):
        #center.shutdown()
        pass



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
        box.Add(ctrl, WEIGHT, wx.EXPAND|wx.ALL, 10)
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
        parentFormCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
        if self.doc is not None:
            btn.SetToolTipString(self.doc)

        box.Add(btn) #, 0, wx.CENTER,10)
        self.wxctrl = btn

    def setFocus(self):
        self.wxctrl.SetFocus()

class DataGrid(base.DataGrid):
    def setup(self,parent,box):
        ctrl = wxgrid.DataGridCtrl(parent,self)
        box.Add(ctrl) #, 0, wx.CENTER,10)
        self.wxctrl = ctrl
    def refresh(self):
        self.wxctrl.ForceRefresh()

    def getSelectedRows(self):
        #return self.wxctrl.GetSelectedRows()
        l = self.wxctrl.GetSelectedCells()
        if len(l) == 0:
            return [self.wxctrl.GetGridCursorRow()]
        return l
                
        
class DataNavigator(base.DataNavigator):
    
    def setup(self,parent,box):
        frm = self.getForm()
                
        mypanel = wx.Panel(parent,-1)
        box.Add(mypanel, WEIGHT, wx.EXPAND|wx.ALL,10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        mypanel.SetSizer(hbox)
        self.wxctrl = mypanel


        self.statusLabel = wx.StaticText( mypanel, -1,
                                          self.getStatus())
        hbox.Add(self.statusLabel, WEIGHT, wx.EXPAND, border=10 )
        
        hbox.Add( (10,1), 0)
        
        btn = wx.Button( mypanel, -1, "<")
        hbox.Add(btn, WEIGHT, wx.EXPAND, border=10 )
        self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
                                   lambda e:self.skip(-1), btn)
                                   #EventCaller(self.skip,-1))
        
        btn = wx.Button( mypanel, -1, ">")
        hbox.Add(btn, WEIGHT, wx.EXPAND, border=10 )
        self.getForm().wxctrl.Bind(wx.EVT_BUTTON,
                                   lambda e:self.skip(1), btn)
                                   #EventCaller(self.skip,1))
        
    def getStatus(self):
        return "%d/%d" % (self.currentPos,len(self.ds))
    
    def refresh(self):
        self.statusLabel.SetLabel(self.getStatus())
        
        

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
        box.Add(mypanel, WEIGHT, wx.ALL|wx.EXPAND,0)
        if self.direction == self.VERTICAL:
            mybox = wx.BoxSizer(wx.VERTICAL)
        else:
            mybox = wx.BoxSizer(wx.HORIZONTAL)
        mypanel.SetSizer(mybox)
        
        self.mybox = mybox # store reference to avoid crash?
        self.wxctrl = mypanel
        
        for c in self._components:
            c.setup(mypanel,mybox)
            
class EntryMixin:

    def setup(self,panel,box):
        mypanel = wx.Panel(panel,-1)
        mypanel.SetBackgroundColour(ENTRY_PANEL_BACKGROUND)
        box.Add(mypanel, WEIGHT, wx.EXPAND|wx.ALL,10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        mypanel.SetSizer(hbox)

        if self.doc is not None:
            label = wx.Panel(mypanel,-1)
            label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
            labelSizer = wx.BoxSizer(wx.VERTICAL)
            label.SetSizer(labelSizer)

            labelCtrl = wx.StaticText(label, -1,
                                      self.getLabel(),
                                      style=wx.ALIGN_RIGHT)
            labelCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
            labelSizer.Add(labelCtrl,1,wx.EXPAND,10)
            
            #ENTRY_DOC_FONT = wx.Font(pointSize=8,
            #                         family=wx.DEFAULT)
            ENTRY_DOC_FONT = wx.SMALL_FONT
            docCtrl = wx.StaticText(
                label, -1,
                "\n".join(docWrapper.wrap(self.doc)),
                style=wx.ALIGN_LEFT)
            docCtrl.SetFont(ENTRY_DOC_FONT)
            docCtrl.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
            labelSizer.Add(docCtrl,1,wx.EXPAND,10)
            
        else:
            label = wx.StaticText(mypanel, -1,
                                  self.getLabel(),
                                  style=wx.ALIGN_RIGHT)
            label.SetBackgroundColour(ENTRY_LABEL_BACKGROUND)
            
        hbox.Add(label, WEIGHT,
                 wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL,
                 border=10,
                 )

        hbox.Add( (10,1), 0) # spacer


        editor = wx.TextCtrl(mypanel,-1,self.getValueForEditor())
                             #validator=EntryValidator(self))
                             #style=wx.TE_PROCESS_ENTER)
        #self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        #editor.Bind(wx.EVT_CHAR, self.EvtChar)
        #editor.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        #editor.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        #editor.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)
        hbox.Add(editor,
                 WEIGHT,
                 wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,
                 10)
        
        self.editor = editor # store reference to avoid crash?
        self.wxctrl = mypanel

    def refresh(self):
        if hasattr(self,'editor'):
            s = self.getValueForEditor()
            self.editor.SetValue(s)
        
    def setFocus(self):
        self.editor.SetFocus()
        self.editor.SetSelection(-1,-1)


    def store(self):
        if self.editor.IsModified():
            s = self.editor.GetValue()
            self.setValueFromEditor(s)
        
        

##     def OnKillFocus(self,evt):
##         print "OnKillFocus() "+self.getLabel()
        
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
    
    def refresh(self):
        EntryMixin.refresh(self)
        base.DataEntry.refresh(self)
        self.editor.SetEditable(self.enabled)
    
        

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


    def setStatusMessage(self,msg):
        if self.modal:
            print msg
        else:
            self.wxctrl.SetStatusText(msg)
            
    def setup(self):
        self.setupMenu()
        if self._parent is None:
            #self.app = WxApp()
            wxparent = None
        else:
            #self.app = self._parent.app
            wxparent = self._parent.wxctrl
            
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

        wx.EVT_CHAR(self.wxctrl, self.OnChar)
        wx.EVT_IDLE(self.wxctrl, self.OnIdle)
        wx.EVT_CLOSE(self.wxctrl, self.OnCloseWindow)
        wx.EVT_ICONIZE(self.wxctrl, self.OnIconfiy)
        wx.EVT_MAXIMIZE(self.wxctrl, self.OnMaximize)
        
        if self.menuBar is not None:
            # todo: won't work
            # todo: put following code to frm._menu.installto(self)
            wxMenuBar = wx.MenuBar()
            for mnu in self.menuBar.menus:
                wxm = self._createMenuWidget(mnu)
                wxMenuBar.Append(wxm,mnu.getLabel())

            self.wxctrl.SetMenuBar(wxMenuBar)
            
        #self.SetBackgroundColour(wx.RED)
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        
        self.mainComp.setup(self.wxctrl,mainBox)
        
        if self.defaultButton is not None:
            self.defaultButton.wxctrl.SetDefault()

        self.wxctrl.SetSizerAndFit(mainBox)
        #self.mainBox = mainBox
        #self.wxctrl.SetAutoLayout(True) 
        #self.wxctrl.Layout()
        self.wxctrl.Centre(wx.BOTH)




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
            wx.EVT_MENU(self.wxctrl, winId, EventCaller(mi.click))
        return wxMenu

    
    def show(self,modal=False):
        self.modal = modal
        #print "show", self.getLabel()
        self.setup()
        #for c in self.wxctrl.GetChildren():
        #    print c
        console.debug(repr(self.mainComp))
        if self.modal:
            self.wxctrl.ShowModal()
        else:
            self.wxctrl.Show()
            if self.app.mainForm is None:
                #print "automagic app.main() call"
                self.app.main(self)
            

##     def showModal(self):
##         assert self._parent is not None
##         self.setup()
##         #self.afterShow()
##         #self._wxFrame.MakeModal(True)
##         #self.show()
##         return self.lastEvent == self.buttons.ok

    def close(self):
        #print "close", self.getLabel()
        self.wxctrl.Close()


    def OnCloseWindow(self, event):
        #self.dying = True
        # http://wiki.wxpython.org/index.cgi/Surviving_20with_20wxEVT_5fKILL_5fFOCUS_20under_20Microsoft_20Windows
        # Surviving with EVT_KILL_FOCUS under Microsoft Windows
        
        #self.window = None
        #self.mainMenu = None
        #if hasattr(self, "tbicon"):
        #   del self.tbicon
        self.wxctrl.Destroy()


    def OnChar(self, evt):
        print "OnChar", evt


    def OnIdle(self, evt):
        #wx.LogMessage("OnIdle")
        evt.Skip()

    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy")
        evt.Skip()

    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()

    def refresh(self):
        base.Form.refresh(self)
        self.wxctrl.Refresh()


class WxUI:
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    panelFactory = Panel
    tableEditorFactory = DataGrid
    navigatorFactory = DataNavigator
    formFactory = Form
    
    def __init__(self,app):
        self.app = app
        self.wxctrl = WxApp()
        self.console = console
        #app.console = ...

    def mainLoop(self):
        "called from Application.main()"
        frm = self.app.mainForm
        #frm.show()
        self.wxctrl.SetTopWindow(frm.wxctrl)
        self.wxctrl.MainLoop()

