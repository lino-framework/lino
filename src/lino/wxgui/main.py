#----------------------------------------------------------------------
# main.py:	MainFrame
#				
#				
# Created:	 2003-10-26
# Copyright: (c) 2003 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import wx
import os

class MainFrame(wx.Frame):
	# overviewText = "wxPython Overview"

	def __init__(self, parent, id, title):
		#self.ui = ui
		#title = ui.db.getLabel()
		wx.Frame.__init__(self, parent, id, title,
								size = (400, 300),
								style=wx.DEFAULT_FRAME_STYLE|
								wx.NO_FULL_REPAINT_ON_RESIZE)

		wx.EVT_IDLE(self, self.OnIdle)
		wx.EVT_CLOSE(self, self.OnCloseWindow)
		wx.EVT_ICONIZE(self, self.OnIconfiy)
		wx.EVT_MAXIMIZE(self, self.OnMaximize)

		self.Centre(wx.BOTH)
		self.CreateStatusBar(1, wx.ST_SIZEGRIP)



	#---------------------------------------------
	def OnCloseWindow(self, event):
		self.dying = True
		#self.window = None
		self.mainMenu = None
		#if hasattr(self, "tbicon"):
		#	del self.tbicon
		self.Destroy()


	#---------------------------------------------
	def OnIdle(self, evt):
		#wx.LogMessage("OnIdle")
		evt.Skip()

	#---------------------------------------------
	def OnIconfiy(self, evt):
		wx.LogMessage("OnIconfiy")
		evt.Skip()

	#---------------------------------------------
	def OnMaximize(self, evt):
		wx.LogMessage("OnMaximize")
		evt.Skip()





class MyApp(wx.App):

	def __init__(self,ui):
		self.ui = ui
		wx.App.__init__(self,0)
		
	def OnInit(self):
		wx.InitAllImageHandlers()
		frame = MainFrame(None, -1, self.ui.db.getLabel())
		self.ui.mainframe = frame
		self.ui.onAppInit(self)
		# self.ui.showUserMenu(None)
		# self._setMenuBar(frame,self.ui.db.getMainMenu(self.ui))
		frame.Show()
		self.SetTopWindow(frame)
		return True

	def OnExit(self):
		self.ui.db.shutdown()



if __name__ == '__main__':
	# don't use this. use /scripts/wxdemo.py
	from lino.sprl import demo
	demo.startup()
	from wxui import wxUI
	ui = wxUI(demo.db)
	app = MyApp(ui)
	app.MainLoop()
