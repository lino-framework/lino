import sys

import wx

from lino.forms.wx.showevents import showEvents


class MyForm:

    def __init__(self,parent,modal,withBtnPanel,
                 withMainPanel=True):
        self.title = "modal=%s,withBtnPanel=%s,withMainPanel=%s" % (
            modal, withBtnPanel, withMainPanel)
        #self.modal = modal
        if modal:
            self.wxctrl = wx.Dialog(parent,-1,self.title,
                                    style=wx.DEFAULT_FRAME_STYLE|
                                    wx.NO_FULL_REPAINT_ON_RESIZE)
        else:
            self.wxctrl = wx.Frame(parent,-1,self.title,
                                   style=wx.DEFAULT_FRAME_STYLE|
                                   wx.NO_FULL_REPAINT_ON_RESIZE|
                                   wx.TAB_TRAVERSAL
                                   )
            #self.wxctrl.CreateStatusBar(1, wx.ST_SIZEGRIP)
            
        #showEvents(self.wxctrl)

        #wx.EVT_CHAR(self.wxctrl, self.OnChar)
        wx.EVT_CLOSE(self.wxctrl, self.OnCloseWindow)
        if withMainPanel:
            mainPanel = wx.Panel(self.wxctrl)
            mainPanel.SetBackgroundColour(wx.RED)
        else:
            mainPanel = self.wxctrl
        
        mainBox = wx.BoxSizer(wx.VERTICAL)

        txt = wx.TextCtrl(mainPanel,-1, "text1",size=(400,20))
        mainBox.Add(txt,border=10)
        #wx.EVT_LEAVE_WINDOW(txt,self.showEvent)
        showEvents(txt)
        
        txt = wx.TextCtrl(mainPanel,-1, "text2",size=(400,20))
        #wx.EVT_LEAVE_WINDOW(txt,self.showEvent)
        mainBox.Add(txt,border=10)

        buttonBox = wx.BoxSizer(wx.HORIZONTAL)
        if withBtnPanel:
            btnPanel = wx.Panel(mainPanel,-1)
            mainBox.Add(btnPanel,border=10)
            btnPanel.SetSizer(buttonBox)
            btnPanel.SetBackgroundColour(wx.GREEN)
        else:
            btnPanel = mainPanel
            mainBox.Add(buttonBox,border=10)
        

        btn = wx.Button(btnPanel,-1,"&OK")
        self.wxctrl.Bind(wx.EVT_BUTTON,
                         lambda e: self.ok(e),
                         btn)
        buttonBox.Add(btn,border=10)
        btn.SetDefault()
        
        btn = wx.Button(btnPanel,-1,"&Cancel")
        self.wxctrl.Bind(wx.EVT_BUTTON,
                         lambda e: self.cancel(e),
                         btn)
        buttonBox.Add(btn,border=10)
        

        mainPanel.SetSizerAndFit(mainBox)

        if modal:
            self.wxctrl.ShowModal()
        else:
            self.wxctrl.Show()
        
    def ok(self,evt):
        print "ok"
        
    def cancel(self,evt):
        print "cancel"
        

    def OnCloseWindow(self, event):
        print "OnCloseWindow"
        self.wxctrl.Destroy()
        #event.Skip()




app = wx.App(0)

if "1" in sys.argv:
    MyForm(None,modal=False,withBtnPanel=False)
if "2" in sys.argv:
    MyForm(None,modal=False,withBtnPanel=True)
if "3" in sys.argv:
    MyForm(None,modal=True,withBtnPanel=False)
if "4" in sys.argv:
    MyForm(None,modal=True,withBtnPanel=True)

app.MainLoop()
    
