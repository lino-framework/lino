#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#import types

from lino.misc.descr import Describable
from lino.misc.etc import issequence
from rowattrs import RowAttribute, FieldContainer
from query import BaseColumnList
from table import SchemaComponent
from datasource import DataRow
#from widgets import WindowComponent, Menu, Command
from widgets import Menu, Command


class FormInstance(DataRow):
	"instanciated by Session"
	def __init__(self,session,formTemplate,**values):
		self.__dict__['_session'] = session
		self.__dict__['_formTemplate'] = formTemplate
		self.__dict__['_clist'] = FormColumnList(self) 

		DataRow.__init__(self,formTemplate, self._clist,values)

		self._clist.setVisibleColumns(None)

		#
		for name,attr in formTemplate._rowAttrs.items():
			if name != attr._name:
				print "TODO: form name (%s) != attr name (%s)" \
						% (name, attr._name)
			self._values.setdefault(attr._name,None)

		# forward some methods::
		for m in ('getFormName', 'getMenus'):
			self.__dict__[m] = getattr(formTemplate,m)
		#for m in ('notifyMessage',):
		#	self.__dict__[m] = getattr(session,m)

	def getSession(self):
		return self._session
	
## 	def getContext(self):
## 		return self._session.getContext()
	

	def getLabel(self):
		return self._formTemplate.getLabel()

	def help(self):
		"user forms must override this"
		self._session.warning("help is not implemented")

	def getButtons(self):
		l = []
		if self._formTemplate._buttonNames is not None:
			for name in self._formTemplate._buttonNames.split():
				m = getattr(self,name)
				assert callable(m)
				l.append( (name,m) )
		return l


## class ContextForm:
## 	"a concrete Form instanciated by a Context"
## 	def __init__(self,formTemplate,context):
## 		self._formTemplate = formTemplate
## 		self._context = context
	


#class FormTemplate(FieldContainer,SchemaComponent,WindowComponent):
class FormTemplate(FieldContainer,SchemaComponent,Describable):
	"instanciated by a Schema"
	
	class Instance(FormInstance):
		pass
	
	def __init__(self,name=None,label=None,doc=None):
		if name is None:
			name = self.__class__.__name__
		if label is None:
			label = name
		#WindowComponent.__init__(self,name,label,doc)
		Describable.__init__(self,name,label,doc)
		SchemaComponent.__init__(self)
		FieldContainer.__init__(self)
		self._menus = []
		self._buttonNames = None
		
	def init(self):
		"user forms must override this"
		raise NotImplementedError

	def init1(self):
		"code similar to Table.init1()"
		#print "%s : init1()" % str(self)
		self.init()
		
		for (name,attr) in self.__dict__.items():
			if isinstance(attr,RowAttribute):
				self.addField(name,attr)
			if isinstance(attr,Menu):
				self._rowAttrs[name] = attr
				self._menus.append(attr)
				attr.setOwner(self,name)
				
		for name,attr in self._rowAttrs.items():
			attr.onOwnerInit1(self,name)
		#for attr in self._rowAttrs.values():
		#	attr.onTableInit2(self,self._schema)

	def setButtonNames(self,buttonNames):
		self._buttonNames = buttonNames


	def getFormName(self):
		return self._name

	def open(self,session,**values):
		#	values.setdefault(col.name,None)
		return self.Instance(session,self,**values)
	
	def getMenus(self):
		return self._menus


class FormColumnList(BaseColumnList):

	def __init__(self, form): #, columnNames=None):
		self._form = form
		BaseColumnList.__init__(self,form.getSession())
		#self.setVisibleColumns(columnNames)

	def getFieldContainer(self):
		return self._form._formTemplate

## 	def getContext(self):
## 		return self._form.getContext()













class TableForm(FormTemplate):
	def __init__(self,table):
		FormTemplate.__init__(self,table.getTableName(),
									 table.getLabel())
		self._table = table
		
	def init(self):
		self.file = Menu("&File")
		self.file.exit = Command(self.close,label="E&xit")

		#self.data = Skipper(self)

	def close(self):
		raise "TODO"
		





	
