import wx
#from lino.adamo.ui import UI

class wxUI: #(UI):
	def __init__(self,sess):
		self.session = sess

	def onAppInit(self,app):
		#self.mainframe
		self.setMainMenu(None,"user")

## 	def showAdminMenu(self,evt):
## 		mb = self.db.getAdminMenu(self)
## 		self._setMenuBar(self.mainframe,mb)
## 		#frame = wx.Frame(wx.GetApp().GetTopWindow(),-1,mb.getLabel())
## 		#self._setMenuBar(frame,mb)
## 		#frame.Show()

## 	def showUserMenu(self,evt):
## 		mb = self.db.getUserMenu(self)
## 		self._setMenuBar(self.mainframe,mb)
## 		#frame = wx.Frame(wx.GetApp().GetTopWindow(),-1,mb.getLabel())
## 		#self._setMenuBar(frame,mb)
## 		#frame.Show()


	def showAbout(self, e):
		"More information about this program"
		from lino import copyleft
		txt = self.session.db.getLabel()
		txt += "\n\n" + self.session.db.getDescription()
		txt += "\n\n" + copyleft("2001-2003","Luc Saffre")
		dlg = wx.MessageDialog(wx.GetApp().GetTopWindow(),
									  txt, "About",
									  wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def confirm(self,msg,title="Confirmation"):
		dlg = wx.MessageDialog(wx.GetApp().GetTopWindow(),
									  msg, title,
									  wx.OK | wx.NO)
		dlg.ShowModal()
		dlg.Destroy()
		return True

	def exit(self,evt):
		if self.confirm("Are you sure?"):
			wx.GetApp().GetTopWindow().Close()
			

	def show(self,e,rpt,**kw):
		#rpt = self.db.provideReport(name,**kw)
		frame = wx.Frame(wx.GetApp().GetTopWindow(),-1,rpt.getLabel())
		from gridframe import RptGrid
		grid = RptGrid(frame,rpt)
		assert len(rpt.getColumns())
		mb = rpt.query.getMenuBar(self)
		self._setMenuBar(frame,mb)
##			frame = wx.Frame(None,-1,rpt.getLabel())
##			,\
##								  size = wx.Size(400,200),\
##								  style = wx.DEFAULT_FRAME_STYLE \
##								  | wx.WANTS_CHARS\
##								  | wx.NO_FULL_REPAINT_ON_RESIZE)
##			grid = RptGrid(frame,rpt)
		frame.Show(True)


## 	def showForm(self,e,row):
## 		frame = wx.Frame(wx.GetApp().GetTopWindow(),-1,rpt.getLabel())


	def decide(self,msg,answers,label="Question"):
		dlg = DecideDialog(wx.GetApp().GetTopWindow(),\
								 msg,label,answers)
		val = dlg.ShowModal()
		dlg.Destroy()
		return val



	def test_decide(self, event):
		msg = "Where do you want to go today?"
		answers = ("I don't know...","to restaurant?","to market?")
		title = "Important question"
		print "result : %d\n" % self.decide(msg,answers,title)
	



"""		
	DecideDialog:
		+==========================================================+
		| +------------------------------------------------------+ |
		| | msgPanel															| |
		| |																		| |
		| |																		| |
		| |																		| |
		| |																		| |
		| +------------------------------------------------------+ |
		| +------------------------------------------------------+ |
		| | buttonPanel														| |
		| |  +---------+	+---------+	 +---------+  +---------+	| |
		| |  | btn[0]	|	|			 |	 |			  |  | btn[n]	|	| |
		| |  |			|	|			 |	 |			  |  |			|	| |
		| |  +---------+	+---------+	 +---------+  +---------+	| |
		| +------------------------------------------------------+ |
		+----------------------------------------------------------+
		
	the top sizer is vbox and contains msgPanel and buttonPanel
		
"""		

class DecideDialog(wx.Dialog):
	
	""" Displays a modal dialog with a question and N buttons, 1 for
	each Label in answers. Returns the index of the chosen button.	 """
	
	def __init__(self, parent, msg, label, answers):
		style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_MODAL | wx.RESIZE_BORDER
		#label = babel.tr(lino.Messages.text,msg)
		#self.log = log
		wx.Dialog.__init__(self, parent, 
								 -1, label, 
								 wx.DefaultPosition, 
								 wx.DefaultSize, 
								 style, 
								 label)
			
		self.SetBackgroundColour(wx.RED) #wxNamedColour("MEDIUM ORCHID"))
		
		msgPanel = wx.StaticText(self, -1,msg) #,wxDefaultPosition, wxDefaultSize)
		msgPanel.SetBackgroundColour(wx.GREEN)
		buttonPanel = wx.Panel(self,-1) #,wxDefaultPosition, wxDefaultSize)
		msgPanel.SetBackgroundColour(wx.BLUE)
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(msgPanel,1,wx.EXPAND|wx.ALL,10)
		vbox.Add(buttonPanel,1,wx.EXPAND|wx.ALL,10)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		id = 10000
		for answer in answers:
			button = wx.Button(buttonPanel,id,answer,
				wx.DefaultPosition, wx.DefaultSize)
			# If wxDefaultSize is specified then the button is sized 
			# appropriately for the text.

			print "button %s: size=(%s)\n" % (answer,
				button.GetSize())
			hbox.Add(button, 1, wx.ALL,10)
			
			wx.EVT_BUTTON(self, id, self.OnButton)
			id += 1
			

		self.SetAutoLayout( True ) # tell dialog to use sizer
		
		self.SetSizer( vbox )		# actually set the sizer
		
		buttonPanel.SetSizer( hbox )
		hbox.Fit(buttonPanel)
		
		vbox.Fit( self ) # set size to minimum size as calculated by the sizer
		#vbox.SetSizeHints( self ) # set size hints to honour mininum size
			
		self.Layout()
			
	def OnButton(self,event):
		print "event.GetId() : %d\n" % event.GetId()
		# self.SetReturnCode()
		self.EndModal(event.GetId()-10000) 
		# self.Destroy()
		
