raise "no longer used"

#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#import types

from lino.misc.descr import Describable
from lino.misc.etc import issequence
from lino.adamo.rowattrs import RowAttribute, FieldContainer, Match
from lino.adamo.query import BaseColumnList
from lino.adamo.table import SchemaComponent
from lino.adamo.row import DataRow
#from widgets import WindowComponent, Menu, Command
from lino.adamo.widgets import Menu, Command


class Form(DataRow,
			  FieldContainer,
			  #SchemaComponent,
			  Describable):
	name = None
	label = None
	def __init__(self,session,
					 **values):
		
		if self.name is None:
			self.name = self.__class__.__name__
		if self.label is None:
			self.label = self.__class__.__name__
		Describable.__init__(self,
									self.name,
									self.label,
									self.__doc__)
		#SchemaComponent.__init__(self)
		FieldContainer.__init__(self)
		
		self.__dict__['_menus'] = []
		self.__dict__['_buttonNames'] = None
		self.__dict__['_session'] = session
		self.__dict__['_clist'] = FormColumnList(self) 

		DataRow.__init__(self, self, self._clist,values)

		self._clist.setVisibleColumns(None)
		
		self.__dict__['Instance'] = self.__class__ # indicates to FieldContainer that self is
# also the valueContainer
		
		self.init()
		
		for name,attr in self._rowAttrs.items():
			#if name != attr._name:
			#	print "TODO: form name (%s) != attr name (%s)" \
			#			% (name, attr._name)
			self._values.setdefault(attr._name,None)

	def getSession(self):
		return self._session
	
	def help(self):
		"user forms must override this"
		self._session.warning("help is not implemented")

	def getButtons(self):
		l = []
		if self._buttonNames is not None:
			for name in self._buttonNames.split():
				m = getattr(self,name)
				assert callable(m)
				l.append( (name,m) )
		return l

		
	def init(self):
		"user forms must override this"
		raise NotImplementedError

	def addMenu(self,label): #,*args,**kw):
		mnu = Menu(label) #,*args,**kw))
		self._menus.append(mnu)
		return mnu

	def addField(self,name,originField,**kw):
		return FieldContainer.addField(self,name,Match(originField,**kw))

	def setButtonNames(self,buttonNames):
		self._buttonNames = buttonNames


	def getFormName(self):
		return self._name

	def getMenus(self):
		return self._menus


class FormColumnList(BaseColumnList):

	def __init__(self, form): #, columnNames=None):
		self._form = form
		BaseColumnList.__init__(self,form.getSession())
		#self.setVisibleColumns(columnNames)

	def getFieldContainer(self):
		return self._form

## 	def getContext(self):
## 		return self._form.getContext()













class TableForm(Form):
	def __init__(self,sess,table,**kw):
		if self.name is None:
			self.name = table.getTableName()
		if self.label is None:
			self.label = table.getLabel()
		Form.__init__(self,sess,**kw)
		self.__dict__['_table'] = table
		
	def init(self):
		mnu = self.addMenu("&File")
		mnu.addCommand(sess.close,label="E&xit")

	def close(self):
		raise "TODO"
		





	
