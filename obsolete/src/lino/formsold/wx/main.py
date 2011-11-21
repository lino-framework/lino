raise "not used"

## Copyright 2003-2005 Luc Saffre 

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
import os

from lino.adamo.widgets import Action
from lino.adamo.datasource import DataCell
from lino.adamo import center
from lino.adamo.session import Session


from gridframe import RptFrame

class EventCaller(Action):
    "ignores the event"
    def __init__(self,form,meth,*args,**kw):
        self._form = form
        Action.__init__(self,meth,*args,**kw)
    def __call__(self,evt):
        #self._form.getSession().notifyMessage("%s called %s." % (
        #   str(evt), str(self)))
        self.execute()



class wxDataCell(DataCell):
        
    def makeEditor(self,parent):
        self.editor = wx.TextCtrl(parent,-1,self.format())

        #self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        #editor.Bind(wx.EVT_CHAR, self.EvtChar)
        #editor.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.editor.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        #editor.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)
        return self.editor

    def OnKillFocus(self,evt):
        v = self.editor.GetValue()
        if len(v) == 0:
            v = None
        self.col.setCellValue(self.row,v)
        evt.Skip()
            

class FormFrame(wx.Frame):
    # overviewText = "wxPython Overview"

    def __init__(self, form):
        print "FormFrame.__init__()"
        #self.ui = ui
        title = form.getLabel()
        #title = self.session.db.getLabel()
        #parent = form.getSession().getCurrentForm()
        parent = None
        wx.Frame.__init__(self, parent, -1, title,
                                size = (400, 300),
                                style=wx.DEFAULT_FRAME_STYLE|
                                wx.NO_FULL_REPAINT_ON_RESIZE)

        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        wx.EVT_ICONIZE(self, self.OnIconfiy)
        wx.EVT_MAXIMIZE(self, self.OnMaximize)

        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        self.setForm(form)
        
        self.Show()



    def setForm(self,form):
        self.form = form
        
        if len(form.getMenus()) != 0:
            wxMenuBar = wx.MenuBar()
            for mnu in self.form.getMenus():
                wxm = self._createMenuWidget(mnu)
                wxMenuBar.Append(wxm,mnu.getLabel())

            self.SetMenuBar(wxMenuBar)
            db = self.form.getSession().db
            self.SetTitle(db.getLabel() +" - " \
                              + self.form.getLabel().replace(db.schema.HK_CHAR, ''))
            
        #self.SetBackgroundColour(wx.RED)

        if len(form) > 0:

            fieldsPanel = wx.Panel(self,-1)

            vbox = wx.BoxSizer(wx.VERTICAL)
            for cell in form:
                p = wx.Panel(fieldsPanel,-1)
                vbox.Add(p)

                hbox = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(p, -1, cell.col.rowAttr.getLabel()) 
                #label.SetBackgroundColour(wx.GREEN)
                hbox.Add(label, 1, wx.ALL,10)

                editor = cell.makeEditor(p)
                hbox.Add(editor, 1, wx.ALL,10)
                p.SetSizer(hbox)


            fieldsPanel.SetSizer( vbox )


            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(fieldsPanel,1,wx.EXPAND|wx.ALL,10)

            buttons = form.getButtons()
            if len(buttons):
                buttonPanel = wx.Panel(self,-1) 
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                for (name,meth) in buttons: 
                    winId = wx.NewId()
                    button = wx.Button(buttonPanel,winId,name,
                                       wx.DefaultPosition,
                                       wx.DefaultSize)
                    hbox.Add(button, 1, wx.ALL,10)

                    wx.EVT_BUTTON(self, winId, EventCaller(form,meth))

                buttonPanel.SetSizer(hbox)
                hbox.Fit(fieldsPanel)

                vbox.Add(buttonPanel,1,wx.EXPAND|wx.ALL,10)

            self.SetAutoLayout( True ) # tell dialog to use sizer

            self.SetSizer( vbox )       # actually set the sizer


            vbox.Fit( self ) # set size to minimum size as calculated by the sizer
            #vbox.SetSizeHints( self ) # set size hints to honour mininum size
            
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
        self.mainMenu = None
        #if hasattr(self, "tbicon"):
        #   del self.tbicon
        self.Destroy()


    def OnIdle(self, evt):
        #wx.LogMessage("OnIdle")
        evt.Skip()

    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy")
        evt.Skip()

    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()


class WxSession(Session):
    
    _dataCellFactory = wxDataCell
    
    def error(self,*a):
        return center.center().console.error(*a)
    def debug(self,*a):
        return center.center().console.debug(*a)
    def info(self,*a):
        return center.center().console.info(*a)

    def showForm(self,formName,modal=False,**kw):
        frm = self.openForm(formName,**kw)
        frame = FormFrame(frm)
##      if modal:
##          frame.showModal()
##      else:
##          frame.show()

    def showReport(self,ds,showTitle=True,**kw):
        frame = RptFrame(None,-1,ds)
        frame.Show()
    


class WxApp(wx.App):

    def __init__(self,rootSession):
        #center.center().setSessionFactory(WxSession)
        #self.session = rootSession.spawn()
        #rootSession.end()
        self.session = WxSession(db=rootSession.db,
                                 langs=rootSession.getLangs())
        wx.App.__init__(self,0)


    def OnInit(self):
        wx.InitAllImageHandlers()
        self.session.onBeginSession()
        
##      self.session.onStartUI()
##      frame = self.session.getCurrentForm() # forms.login
##      #assert frame is not None
##      #print frame
##      #frame = FormFrame(None, -1, form)
##      self.SetTopWindow(frame)
        return True

    def OnExit(self):
        self.session.shutdown()

## class wxApplication(Application):
##  def __init__(self,**kw):
##      Application.__init__(self,**kw)
##      self.wxapp = wxAppInstance(self)
        
##  def createSession(self,**kw):
##      return wxSession(self,**kw)
        
##  def run(self):
##      self.wxapp.MainLoop()
        
