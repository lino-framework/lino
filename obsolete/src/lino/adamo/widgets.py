#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#from components import OwnedThing
from lino.misc.descr import Describable


## class WindowComponent(Describable):
	
## 	def __init__(self,name,label,doc):
## 		Describable.__init__(self,name,label,doc)
## 		self._parent = None
## 		self._index = None
		
## 	def register(self,parent,index):
## 		assert self._parent is None
## 		self._parent = parent
## 		self._index = index
		
## 	def getParent(self):
## 		return self._parent
		
## 	def getId(self):
## 		return self._index

	
class Action:
	def __init__(self,
					 method,
					 *args,**kw):
		self.method = method
		self.args = args
		self.keywords = kw
		#OwnedThing.__init__(self,label,doc)
		
	def execute(self,*args):
		args = args + self.args
		f = self.method
		return f(*args,**self.keywords)

class Command(Describable,Action):
	def __init__(self,label,method,*args,**kw):
		#assert type(label) == type(""),"%s not a string" % repr(label)
		Describable.__init__(self,None,label)
		Action.__init__(self,method,*args,**kw)




class Menu(Describable):
	def __init__(self,label,doc=None):
		Describable.__init__(self,None,label,doc)
		self._items = []
		
		
	def getItems(self):
		return self._items

## 	def onOwnerInit1(self,owner,name):
## 		for (name,attr) in self.__dict__.items():
## 			if isinstance(attr,Command):
## 				attr.setOwner(self,name)
## 				self._items.append(attr)

	def addCommand(self,label,meth,*args,**kw):
 		assert type(label) == type(""),\
 				 "%s : not a string" % repr(label)
## 		if label is None:
## 			for a in args:
## 				if hasattr(a,"getLabel"):
## 					label = a.getLabel()
## 					assert type(label) == type(""),\
## 							 "%s : not a string" % repr(label)
## 					break
		#if label is None:
		#	label = meth.__name__
## 		if label is None:
## 			label = str(self)
		cmd = Command(label,meth, *args,**kw)
		self._items.append(cmd)
		return cmd
	




## class Label(WindowComponent):
## 	pass

	
## class Button(Action,WindowComponent):
## 	def __init__(self,name=None,label=None,func=None,args=()):
## 		#if action is None:
## 		#	 action = Action(label,func,args)
## 		#if label is None:
## 		#	 label = action.getLabel()
## 		WindowComponent.__init__(self,name,label)
## 		Action.__init__(self,func,args)
## 		#self._action = action
## 		#self.func = func
## 		#self.args = args

## 	#def getAction(self):
## 	#	 return self._action
	
## 	#def register(self,win,index):
## 	#	 Component.register(self,win,index)
## 		#if self._action is None:
## 		#	 self._action = win.addAction(self._label,self._func)






## class Window(Describable):

## 	#def __init__(self,ui,id,parent=None,label=None,desc=None):
## 	def __init__(self,parent=None,label=None,doc=None):
## 		#Describable.__init__(self,**kw)
## 		Describable.__init__(self,None,label,doc)
## 		#Component.__init__(self,label)
## 		self._components = []
## 		self._menubars = {}
## 		self._actions = []
## 		#self.ui = ui
## 		#self._id = id
## 		self._parent = parent

## ##		def getMenuBar(self):
## ##			for c in self._components:
## ##				if isinstance(c,MenuBar): return c
## ##			# return None
## ##			# return self._menuBar

## ## 	def getId(self):
## ## 		return self._id
	
## 	def getParent(self):
## 		return self._parent





## 	def showReport(self,rpt,**kw):
## 		raise NotImplementedError

## 	def showForm(self,rpt,**kw):
## 		raise NotImplementedError

## 	def setMainMenu(self,evt,name):
## 		raise NotImplementedError

## 	def showAbout(self,evt,id,**kw):
## 		raise NotImplementedError,self.__class__
	
## 	def test_decide(self,evt,id,**kw):
## 		raise NotImplementedError,self.__class__
	
## 	def showWindow(self,evt,id,**kw):
## 		raise NotImplementedError

## 	def exit(self,evt):
## 		raise NotImplementedError
	




	
	
## 	def add(self,comp):
## 		comp.register(self,len(self._components))
## 		self._components.append(comp)
## 		return comp

## 	def close(self):
## 		if self._parent is None:
## 			return ui.close()
## 		return ui.show(self._parent)

## 	def getAction(self,id):
## 		return self._actions[id]
	
## 	def getComponents(self):
## 		return self._components
	
## 	def addLabel(self,label):
## 		return self.add(Label(label))
	
## 	def addForm(self):
## 		return self.add(Form())
	
## 	def addMenuBar(self,name,label):
## 		mb = MenuBar(self,label)
## 		self._menubars[name] = mb
## 		return mb
## 		# return self.add(MenuBar(label))
	
## 	def getMenuBars(self):
## 		return self._menubars

## 	def addButton(self,action=None,label=None,func=None,args=()):
## 		return self.add(Button(action,label,func,args))
	
## 	def addGrid(self,query):
## 		return self.add(Grid(query))
	
## 	def addEditor(self,row,attr,label=None):
## 		return self.add(Editor(row,attr,label))


## class MainWindow(Window):
## 	def __init__(self,ui,id,db,parent=None,label=None,desc=None):
## 		#Describable.__init__(self,**kw)
## 		Window.__init__(self,ui,parent,label,desc)
## 		self.db = db
## 		db.defineMenus(self)

## class ReportWindow(Window):
## 	def __init__(self,ui,id,db,rpt,parent=None,label=None,desc=None):
## 		#Describable.__init__(self,**kw)
## 		Window.__init__(self,ui,parent,label,desc)
## 		self.rpt = rpt
## 		self.db = db
## 		rpt.defineMenus(self)

## 	def getSelectedRows(self):
## 		raise "TODO"
	

