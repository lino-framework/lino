#----------------------------------------------------------------------
# ID:        $Id: ui.py,v 1.4 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#from lino.misc import gpl
#from lino import __version__
#from widgets import Window, MenuBar, Action
#from lino.adamo.database import Database
#from lino import copyright


class UI:
	def __init__(self,
					 author=None,
					 year=None,
					 verbose=False):
		self._messages = []
		self._defaultAction = None
		self._databases = {}
		#self.reportClass = None
		#self._mainWindow = None
		#if db is not None:
		#	self.setDatabase(db)
		self.verbose = verbose
  		#if verbose:
		#	print "verbose!"
		
##  		if verbose:
## 			print copyright(author=author,year=year)
## 			print "Lino version " + __version__
## 			print gpl.copyright(year,author)


	def addDatabase(self,db):
		self._databases[db.getName()] = db

## 	def addDatabase(self,name,
## 						 conn,schema,
## 						 label=None,description=None):
## 		db = Database(self,name,conn,schema,label,description)
## 		self._databases[name] = db
## 		# win = Window(db.getLabel())
## 		# schema.setupContext(self,ctx)
## 		# self.setMainWindow(win)
## 		# db.initUI(self)
## 		return db

	def getDatabase(self,name):
		return self._databases[name]
		
	def message(self,msg):
		self._messages.append(msg)
			
	def clearMessages(self):
		self._messages = []
		
	def getMessages(self):
		return self._messages

	def shutdown(self):
		for name,db in self._databases.items():
			db.shutdown()

	

## 	def getMainWindow(self):
## 		return self._mainWindow

## 	def setMainWindow(self,w):
## 		self._mainWindow = w

	def progress(self,msg):
		if self.verbose:
			print msg
		
	def decide(self,msg,answers,label="Question"):
		
		"""display string `msg` in a window with string `label` as
		title.  `answers` is a list of strings. Display one button for
		each item of `answers`.  return the index of selected answer.
		"""
		
		raise NotImplementedError
		
	def confirm(self,label,msg):

		"""display string `msg` in a window with string `label` as title
 		and two buttons labeled 'Yes' and 'No'. Return True if user
 		selected OK.  """

		raise	NotImplementedError

	
## 	def addMenuBar(self,name,label):
## 		mb = MenuBar(self,label)
## 		self._menubars[name] = mb
## 		return mb


## 	def setDefaultAction(self,meth,*args):
## 		self._defaultAction = Action(self,meth,args)
## 	def getDefaultAction(self):
## 		return self._defaultAction

	##
	## the following methods should be usable as actions
	## 
	
	def showReport(self,rpt,**kw):
		raise NotImplementedError

	def showForm(self,rpt,**kw):
		raise NotImplementedError

	def setMainMenu(self,evt,name):
		raise NotImplementedError

	def showAbout(self,evt,id,**kw):
		raise NotImplementedError,self.__class__
	
	def test_decide(self,evt,id,**kw):
		raise NotImplementedError,self.__class__
	
	def showWindow(self,evt,id,**kw):
		raise NotImplementedError

	def exit(self,evt):
		raise NotImplementedError
	
## class WindowManager:
##		def __init__(self):
##			self._windowList = []
##			self._currentWindow = None

##		def getCurrentWindow(self):
##			return self._currentWindow
	
##		def setCurrentWindow(self,win):
##			self._currentWindow = win
	
##		def getWindow(self,id):
##			return self._windowList[id]

##		def openWindow(self,label):
##			win = Window(label)
##			win.register(self,len(self._windowList))
##			self._windowList.append(win)
##			return win



## class WindowingUI(UI):
## 	# no longer used
## 	def __init__(self,db):
## 		UI.__init__(self,db)
## 		#self._wm = WindowManager()
## 		self._windows = []
## 		self._currentWindow = None
		
## 	def getCurrentWindow(self):
## 		return self._currentWindow
	
## 	def setCurrentWindow(self,win):
## 		if not hasattr(win,'uiid'):
## 			self.addWindow(win)
## 		self._currentWindow = win
	
## 	def getWindow(self,id):
## 		return self._windows[id]

## 	def getMainWindow(self):
## 		if len(self._windows):
## 			self.message("taking 0 as default")
## 			return self._windows[0]
## 		self.message("creating main window")
## 		# db = request.getWebApp().getConfigItem('db')
## 		w = self.db.getUserMenu(self)
## 		self.addWindow(w)
## 		return w
	
## ##		def getCurrentWindow(self):
## ##			return self._wm.getCurrentWindow()
	
## ##		def getWindow(self,id):
## ##			return self._wm.getWindow(id)




## 	def addWindow(self,w):
## 		assert not hasattr(w,"ui")
## 		assert not hasattr(w,"winid")
## 		assert not hasattr(w,"renderedActions")
## 		w.ui = self
## 		w.winid = len(self._windows)
## 		w.renderedActions = None
## 		self._windows.append(w)

## 	def killWindow(self,win):
## 		assert self._windows[win.winid] is win
## 		self._windows[win.winid] = None
	
## ## 	def confirm(self,label,msg,onOk,onNok=None):
		
## ## 		win = Window(label)
		
## ## 		#win = self.openWindow(label)
## ## 		self.addWindow(win)
## ## 		if onNok is None:
## ## 			onNok = win.getParent
## ## 		win.addLabel(label)
## ## 		win.addButton(label="Yes",func=onOk)
## ## 		win.addButton(label="No",func=onNok)
## ## 		return win

		


import sys

class ConsoleUI(UI):

	def showReport(self,rpt,out=None):
		if out is None:
			out = sys.stdout
		if rpt._showTitle:
			out.write(rpt.getLabel()+"\n")
			out.write("="*len(rpt.getLabel())+"\n")
		columns = rpt.getVisibleColumns()
		out.write(" ".join(
			[col.getLabel().ljust(col.getPreferredWidth()) \
			 for col in columns]).rstrip())
		out.write("\n")
		out.write(" ".join( ["-" * col.getPreferredWidth() \
							  for col in columns]))
		out.write("\n")
		for values in rpt: #.iterateAsColumns():
			l = []
			i = 0
			for value in values:
				col = columns[i]
				i += 1
				#value = qrow[col.queryCol.index]
				#value = col.atoms2value(atomicRow)
				l.append(col.render(value))
				#l.append(str(value).ljust(col.getPreferredWidth()))
				#i += 1
			out.write(" ".join(l).rstrip())
			out.write("\n")


	
