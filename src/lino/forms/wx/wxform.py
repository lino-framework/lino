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


"""

about sizers.

- in wxWindows, a "Window" is what other GUI toolits call "Widget",
  "Control" or "Component": any visible object on screen.

- I use only nested BoxSizers.

- sizer.Add() can get either a wxWindow or another Sizer.

- A Sizer normally sets size and position of its *children*, depending
  on the size available in its parentWindow.

- The parentWindow of a Sizer is the Window that has been dedicated to
  this sizer, using SetSizer().

- When the parentWindow's size changes, its sizer will layout all its
  children.
  
- sizer.Fit(window) : Tell the sizer to resize the window to match the
  sizer's minimal size. That's the opposite direction: the sizer says
  how much space it needs.

- only the topSizer of a sizer hierarchy must become SetSizer() for a
  window. (Otherwise crash!)

"""

import wx

from lino.forms import base

WEIGHT = 1

class Label(base.Label):
    
    def setup(self,frm,panel,box):
        text = wx.StaticText(panel,-1, self.getLabel())
        box.Add(text) #, WEIGHT, wx.EXPAND|wx.ALL, 10)
                
class Button(base.Button):
    
    def setup(self,frm,panel,box):
        
        winId = wx.NewId()
        btn = wx.Button(panel,winId,self.getLabel(),
                        wx.DefaultPosition,
                        wx.DefaultSize)
        btn.SetBackgroundColour('YELLOW')
        frm.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
        #b.SetDefault()
        box.Add(btn) #, 0, wx.CENTER,10)
                
        

class Panel(base.Panel):
    
    def setup(self,frm,panel,box):
        mypanel = wx.Panel(panel,-1)
        box.Add(mypanel) #, WEIGHT, wx.ALL|wx.EXPAND,10)
        if self.direction == self.VERTICAL:
            mybox = wx.BoxSizer(wx.VERTICAL)
        else:
            mybox = wx.BoxSizer(wx.HORIZONTAL)
        # uncomment both following lines to get a crash
        box.Add(mybox)
        #mypanel.SetSizer(mybox) 
        
        self.mybox = mybox # store reference to avoid crash?
        
        for c in self._components:
            c.setup(frm,mypanel,mybox)
            
        
class Entry(base.Entry):

    def setup(self,frm,panel,box):
        mypanel = wx.Panel(panel,-1)
        box.Add(mypanel)#, WEIGHT, wx.EXPAND|wx.ALL,10)
        
        mybox = wx.BoxSizer(wx.HORIZONTAL)
        # uncomment both following lines to get a crash
        box.Add(mybox)
        # mypanel.SetSizer(mybox) 
        
        label = wx.StaticText(mypanel, -1, self.getLabel()) 
        label.SetBackgroundColour(wx.GREEN)
        mybox.Add(label)#, WEIGHT, wx.ALL|wx.EXPAND,10)

        s = self.type.format(self.value)
        editor = wx.TextCtrl(mypanel,-1, s)
        #self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        #editor.Bind(wx.EVT_CHAR, self.EvtChar)
        #editor.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        editor.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        #editor.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)
        mybox.Add(editor)#,WEIGHT,wx.EXPAND|wx.ALL,10)
        
        self.mybox = mybox # store reference to avoid crash?
        self.editor = editor # store reference to avoid crash?
        
        #return self.editor

    def OnKillFocus(self,evt):
        s = self.editor.GetValue()
        self.value = self.type.parse(s)
        evt.Skip()
        



class WxFrame(wx.Frame):

    def __init__(self, frm):
        self._frm = frm
        if frm._parent is None:
            parent = None
        else:
            parent = frm._parent._wxFrame
        wx.Frame.__init__(self, parent, -1,
                          frm.getLabel(),
                          #size = (400, 300),
                          style=wx.DEFAULT_FRAME_STYLE|
                          wx.NO_FULL_REPAINT_ON_RESIZE)

        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        wx.EVT_ICONIZE(self, self.OnIconfiy)
        wx.EVT_MAXIMIZE(self, self.OnMaximize)

        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)


    def setup(self): 
        frm = self._frm
        if frm._menu is not None:
            # todo: won't work
            # todo: put following code to frm._menu.installto(self)
            wxMenuBar = wx.MenuBar()
            for mnu in frm._menu.getMenus():
                wxm = self._createMenuWidget(mnu)
                wxMenuBar.Append(wxm,mnu.getLabel())

            self.SetMenuBar(wxMenuBar)
            
        #self.SetBackgroundColour("KHAKI3")
        self.SetBackgroundColour(wx.RED)
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self,-1)
        panel.SetBackgroundColour(wx.GREEN)
        #box.Add(panel,WEIGHT,wx.EXPAND|wx.ALL,10)
        
        for c in frm._components:
            c.setup(self,panel,mainBox)
                
        
        #box.Fit(self) # set size to minimum size as calculated by the
        # sizer
        #self.SetAutoLayout(True)
        #self.SetSizer(mainBox)
        #mainBox.Fit(self)
        self.SetSizerAndFit(mainBox)
        self.mainBox = mainBox
        #self.SetAutoLayout(True) 
        self.Layout()




    def _createMenuWidget(self,mnu):
        wxMenu = wx.Menu()
        for mi in mnu.getItems():
            #print repr(mi.getLabel())
            #"%s must be a String" % repr(mi.getLabel())
            winId = wx.NewId()
            doc = mi.getDoc()
            if doc is None:
                doc=""
            assert type(doc) == type(""),\
                     repr(mi)
            assert type(mi.getLabel()) == type(""),\
                     repr(mi)
            wxMenu.Append(winId,mi.getLabel(),doc)
            wx.EVT_MENU(self, winId, EventCaller(self.form,
                                                 mi.execute))
        return wxMenu

    def OnCloseWindow(self, event):
        self.dying = True
        #self.window = None
        #self.mainMenu = None
        #if hasattr(self, "tbicon"):
        #   del self.tbicon
        self.Destroy()
        #self._frm


    def OnIdle(self, evt):
        #wx.LogMessage("OnIdle")
        evt.Skip()

    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy")
        evt.Skip()

    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()




class Form(base.Form):
    labelFactory = Label
    entryFactory = Entry
    buttonFactory = Button
    panelFactory = Panel
    def __init__(self,*args,**kw):
        
        base.Form.__init__(self,*args,**kw)
        if self._parent is None:
            self.app = WxApp()
        else:
            self.app = self._parent.app
            
        self._wxFrame = WxFrame(self)

    def afterShow(self):
        if self._parent is None:
            self.app.SetTopWindow(self._wxFrame)
            self.app.MainLoop()
    
    def show(self):
        self._wxFrame.setup()
        self._wxFrame.Show()
        self.afterShow()

    def showModal(self):
        self._wxFrame.setup()
        self._wxFrame.MakeModal(True)
        self._wxFrame.Show()
        self.afterShow()
        return self.lastEvent == self.buttons.ok

    def close(self):
        self._wxFrame.Close()


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
