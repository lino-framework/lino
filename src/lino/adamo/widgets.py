#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.misc.descr import Describable
from lino.misc.etc import issequence

## class Widget:
## 	def asLeftMargin(self,renderer):
## 		renderer.write('left margin')
## 	def asPreTitle(self,renderer):
## 		renderer.write('preTitle')
## 	def getLabel(self):
## 		return repr(self)

			
## class RowWidget(Widget):
## 	def asBody(self,renderer):
## 		self.asPage(renderer)
## 		self.asFooter(renderer)

## 	def asLeftMargin(self,renderer):
## 		renderer.write('<p><a href="add">add row</a>')
## 		renderer.write('<br><a href="delete">delete row</a></p>')
## 		self._area._db.asLeftMargin(renderer)


## 	def asPreTitle(self,renderer):
## 		pass
	
## 	def asFooter(self,renderer):
## 		pass

## 	def asFormCell(self,renderer):
## 		self.asParagraph(renderer)

## 	def asLabel(self,renderer):
## 		renderer.renderLink(
## 			url=renderer.uriToRow(self),
## 			label=self.getLabel())
		
## 	def asPage(self,renderer):
## 		renderer.writeForm(self.getAttrValues())

## 	def renderDetails(self,renderer):
## 		pass
## ## 		wr = renderer.write
## ## 		if False:
## ## 			wr("<ul>")
## ## 			for (name,dtl) in self._area._table._details.items():
## ## 				rpt = dtl.query(self)
## ## 				wr('<li>')
## ## 				rpt.asParagraph(renderer)
## ## 				wr("</li>")

## ## 			wr("</ul>")
		
			
## 	def asParagraph(self,renderer):
## 		return self.asLabel(renderer)
## ## 		wr = renderer.write
## ## 		for name,attr in self._area._table._rowAttrs.items():
## ## 			if not name in ('body'):
## ## 				value = getattr(self,name)
## ## 				if value is not None:
## ## 					wr('<b>%s:</b> ' % name)
## ## 					type = getattr(attr,'type',None)
## ## 					renderer.renderValue(value,type)
## ## 					wr(" ")


	

	

class Window(Describable):

	#def __init__(self,ui,id,parent=None,label=None,desc=None):
	def __init__(self,parent=None,label=None,desc=None):
		#Describable.__init__(self,**kw)
		Describable.__init__(self,parent,label,desc)
		#Component.__init__(self,label)
		self._components = []
		self._menubars = {}
		self._actions = []
		#self.ui = ui
		#self._id = id
		self._parent = parent

##		def getMenuBar(self):
##			for c in self._components:
##				if isinstance(c,MenuBar): return c
##			# return None
##			# return self._menuBar

	def getId(self):
		return self._id
	
	def getParent(self):
		return self._parent





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
	




	
	
	def add(self,comp):
		comp.register(self,len(self._components))
		self._components.append(comp)
		return comp

	def close(self):
		if self._parent is None:
			return ui.close()
		return ui.show(self._parent)

	def getAction(self,id):
		return self._actions[id]
	
	def getComponents(self):
		return self._components
	
	def addLabel(self,label):
		return self.add(Label(label))
	
	def addForm(self):
		return self.add(Form())
	
	def addMenuBar(self,name,label):
		mb = MenuBar(self,label)
		self._menubars[name] = mb
		return mb
		# return self.add(MenuBar(label))
	
	def getMenuBars(self):
		return self._menubars

	def addButton(self,action=None,label=None,func=None,args=()):
		return self.add(Button(action,label,func,args))
	
	def addGrid(self,query):
		return self.add(Grid(query))
	
	def addEditor(self,row,attr,label=None):
		return self.add(Editor(row,attr,label))


class MainWindow(Window):
	def __init__(self,ui,id,db,parent=None,label=None,desc=None):
		#Describable.__init__(self,**kw)
		Window.__init__(self,ui,parent,label,desc)
		self.db = db
		db.defineMenus(self)

class ReportWindow(Window):
	def __init__(self,ui,id,db,rpt,parent=None,label=None,desc=None):
		#Describable.__init__(self,**kw)
		Window.__init__(self,ui,parent,label,desc)
		self.rpt = rpt
		self.db = db
		rpt.defineMenus(self)

	def getSelectedRows(self):
		raise "TODO"
	

class Action:
	def __init__(self,win,method,args=()):
		#self.target = target
		#if method is not None:
		#	assert type(method) is not type('')
		self.method = method
		
		if not issequence(args):
		#if type(args) is type(''):
			args = (args,)
		self.args = args
		
		self._id = len(win._actions)
		win._actions.append(self)

	def getId(self):
		return self._id

	def execute(self,*args):
		#if self.method is None:
		#	return self.target
		args = args + self.args
		#f = getattr(self.target,self.method)
		f = self.method
		return f(*args)


## class Widget:
## 	pass


class Component(Describable):
	
	def __init__(self,label):
		Describable.__init__(self,None,label)
		self._parent = None
		self._index = None
		
	def register(self,parent,index):
		assert self._parent is None
		self._parent = parent
		self._index = index
		
	def getParent(self):
		return self._parent
		
	def getId(self):
		return self._index

	


class MenuBar(Describable):
	def __init__(self,win,label,description=None):
		self._menus = []
		self._win = win
		Describable.__init__(self,None,label,description)
		
	def addMenu(self,label):
		mnu = Menu(self,label)
		self._menus.append(mnu)
		return mnu
	
	def getMenus(self):
		return self._menus
				  
		
class Menu(Describable):
	def __init__(self,mb,label,description=None):
		Describable.__init__(self,None,label,description)
		self._items = []
		self._mb = mb
		
	def addItem(self,label,method=None,args=()):
		#a = self._bar.addAction(label,func)
		mi = MenuItem(self._mb._win,label,method,args)
		self._items.append(mi)
		return mi
		
	def getItems(self):
		return self._items

class MenuItem(Describable,Action):
	def __init__(self,win,label,method,args=()):
		Describable.__init__(self,None,label)
		Action.__init__(self,win,method,args)





class Label(Component):
	pass

	
class Button(Action,Component):
	def __init__(self,label=None,func=None,args=()):
		#if action is None:
		#	 action = Action(label,func,args)
		#if label is None:
		#	 label = action.getLabel()
		Component.__init__(self,label)
		Action.__init__(self,func,args)
		#self._action = action
		#self.func = func
		#self.args = args

	#def getAction(self):
	#	 return self._action
	
	#def register(self,win,index):
	#	 Component.register(self,win,index)
		#if self._action is None:
		#	 self._action = win.addAction(self._label,self._func)




## class Grid(Component):
##		def __init__(self,query,label=None):
##			if label is None:
##				label = query.getLabel()
##			Component.__init__(self,label)
##			self.query = query
	
##		def getQuery(self):
##			return self.query



	

class Editor(Component):	
	def __init__(self,row,attr,label=None):
		if label is None:
			label = attr.getLabel()
		Component.__init__(self,label)
		self._row = row
		self._attr = attr

	def getRow(self):
		return self._row
	
	def getAttr(self):
		return self._attr

class Form(Component):
	def __init__(self,label=None):
		Component.__init__(self,label)
		self._rows = []

	def addRow(self,*comps):
		self._rows.append(comps)

	def getRows(self):
		return self._rows
	
## class View(Component):

##		""" A View is a combination of a master query with optional slave
##		queries, whose rows are to be displayed as a table or a form.
	
##		"""
	
##		def __init__(self,master,label=None,pageLen=10):
##			assert isinstance(master,Query)
##			if label is None:
##				label = view.getLabel()
##			Component.__init__(self,label)
##			self.master = master
##			self.slaves = []
##			self.pageLen = pageLen # rows per page
	
##		def getMaster(self):
##			return self.master
	
##		def getSlaves(self):
##			return self.slaves

##		def addSlave(



class Grid(Window):
	def __init__(self,query,
					 pageLen=None,
					 asTable=True,
					 isEditing=False):
		Window.__init__(self,query.getLabel())
		self.query = query
		if pageLen is None:
			if asTable: pageLen = 10
			else: pageLen = 10
		self.pageLen = pageLen
		self.currentPage = 1
		self.asTable = asTable
		self.isEditing = isEditing

	
	def setOrderBy(self,ui,columnList):
		self.query.setOrderBy(columnList)
		#return None


	
## class MessageWindow(Window):
##		def __init__(self,label,msg,actions):
##			Window.__init__(self,label)
##			self.add(Label(msg))
##			for a in actions:
##				self.add(a)


