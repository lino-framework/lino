#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.misc.descr import Describable
from lino.misc.etc import issequence
from rowattrs import RowAttribute, FieldContainer
from query import BaseColumnList
from table import SchemaComponent
from datasource import DataRow
from widgets import WindowComponent, Menu, Command

class FormTemplate(FieldContainer,SchemaComponent,WindowComponent):
	"instanciated by a Schema"
	
	class Row(DataRow):
		"instanciated by Session"
		def __init__(self,session,ctxForm,**values):
			#assert isinstance(session,Session)
			self.__dict__['_ctxForm'] = ctxForm
			self.__dict__['_session'] = session
			
			DataRow.__init__(self,ctxForm._formTemplate,
								  ctxForm._clist,values)

			#
			for name,attr in ctxForm._formTemplate._rowAttrs.items():
				if name != attr._name:
					print "TODO: form name (%s) != attr name (%s)" \
							% (name, attr._name)
				self._values.setdefault(attr._name,None)
				
			# forward some methods::
			for m in ('getContext','getFormName', 'getMenus'):
				self.__dict__[m] = getattr(ctxForm,m)
				
		def getSession(self):
 			return self._session
	
## 		def getContext(self):
## 			return self._ctxForm._context
	
## 		def getFormName(self):
## 			return self._ctxForm._name

		
	def __init__(self,name=None,label=None,doc=None):
		if name is None:
			name = self.__class__.__name__
		if label is None:
			label = name
		WindowComponent.__init__(self,name,label,doc)
		SchemaComponent.__init__(self)
		FieldContainer.__init__(self)
		self._menus = []
		
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


	def getFormName(self):
		return self._name

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
		


class ContextForm:
	"a concrete Form instanciated by a Context"
	def __init__(self,formTemplate,context):
		self._formTemplate = formTemplate
		self._context = context
		self._clist = FormColumnList(self) #,form.getPeekColumnNames())
	
	def open(self,session,**values):
		#	values.setdefault(col.name,None)
		return self._formTemplate.Row(session,self,**values)

	def getContext(self):
		return self._context
	
	def getFormName(self):
		return self._formTemplate.getFormName()

	def getMenus(self):
		return self._formTemplate._menus


class FormColumnList(BaseColumnList):

	def __init__(self, ctxForm, columnNames=None):
		self._ctxForm = ctxForm
		BaseColumnList.__init__(self)
		self.setVisibleColumns(columnNames)

	def getFieldContainer(self):
		return self._ctxForm._formTemplate

	def getContext(self):
		return self._ctxForm._context



	
