raise "no longer used"

import types

from lino.misc.compat import *

from datatypes import DataVeto
from rowattrs import Pointer
from datasource import Datasource
from widgets import Widget
			
class BaseRow(Widget):
	
	#def __init__(self,rowId,knownValues,complete,new):
	def __init__(self,rowId,atomicValues,new):
		"""
		"""
		
		# note : self._area is a class variable which is set during
		# dynamic creation of a subclass of WritableRow see area.py)
		
		#self.__dict__["_rowId"] = rowId
		self.__dict__["_new"] = new
		if atomicValues is None:
			self.__dict__["_complete"] = False
			atomicValues = [None] * len(self._query.getAtoms())
			atomicValues[0:len(rowId)] = rowId
		else:
			self.__dict__["_complete"] = True
			assert rowId == atomicValues[:self._query._pkaLen]
			
## 		d = {}
## 		if knownValues is not None:
## 			for(k,v) in knownValues.items():
## 				attr = self._area._table.getRowAttr(k)
## 				d[attr.getAttrName()] = attr.validate(self,v)
				#assert
				
## 		if complete:
## 			for k in self._area._table._rowAttrs.keys():
## 				if not knownValues.has_key(k):
## 					knownValues[k] = None
## 			if new:
## 				for k in self._area._table._rowAttrs.keys():
## 				 if not knownValues.has_key(k):
## 					 knownValues[k] = None
## 			else:
## 				for k in self._area._table._rowAttrs.keys():
## 					assert knownValues.has_key(k),\
## 							 "complete claimed but attrib %s missing" % k


				
		self.__dict__["_values"] = atomicValues
		self.__dict__["_isCompleting"] = False
				

##			atomicRow = [None] * len(self.table.getAtoms())
		
##			for col in self.table.getColumns():
##				col.atoms2row(atomicRow,self)
			# self._values[col.name] = col.getDefaultValue(self)
			
##			for (k,v) in initialValues.items():
##				col = self.table.findColumn(k)
##				assert col is not None
##				self._values[k] = v

	def isComplete(self):
		return self.__dict__['_complete']
	
	def isNew(self):
		return self.__dict__['_new']
	
		
## 	def getGrid(self,ui):
## 		# currently not used
## 		#w = ui.openWindow(label="%s (Form)" % repr(self))
## 		q = self._area._table.peekQuery.copy()
## 		id = self.getRowId()
## 		i = 0
## 		for (name,type) in self._area._table.getPrimaryAtoms():
## 			q.setAtomicSample(name,type,id[i])
## 			i += 1
			
## 		#w.add(Grid(q, asTable=False))
		
## 		return Grid(q,asTable=False)

	def getRowId(self):
		return self._values[0:len(self._query._pkaLen)]
		#return self._rowId

		#return str(self._rowId)
		
	
## 	def setValues(self,valueDict):
## 		"initialize values without validation"
## 		for (k,v) in valueDict.items():
## 			assert self._area._table._rowAttrs.has_attr(k)
## 			self.__dict__['_values'][k] = v
		
## 	def getValues(self):
		
## 		"""Returns the value dictionary.	 If you update this, then there
## 		is no validation and the row is not marked dirty."""
		
## 		return self.__dict__['_values']
	
##		def setAtomicValues(self,atomicRow):
##			for attr in self.table.getAttributes():
##				attr.atoms2row(atomicRow,self)
			
##		# def getAtomicRow(self):
##		def getAtomicValues(self):
##			atomicRow = [None] * len(self.table.getAtoms())
##			for col in self.table.getColumns():
##				col.row2atoms(self,atomicRow)
##			return tuple(atomicRow)

	def makeComplete(self,area):
		if self._dirty:
			raise "cannot makeComplete() a dirty row!"
		if not self._complete:
			self._readFromStore(area)

	def _readFromStore(self,area):
		"""
		make this row complete using a single database lookup
		"""
		assert not self.__dict__['_complete'],\
				 "%s : readFromStore() called a second time" % repr(self)
		#assert not self._new,\
		#		 "cannot call readFromStore() for a new row"
		assert not self._isCompleting
		assert area._table == self._query.leadTable


		
		
		# but what if atoms2row() causes __getattr__ to be called
		# again? maybe a switch _isCompleting to check this.
		self.__dict__["_isCompleting"] = True
		
		# print "makeComplete() : %s" % repr(self)
		id = self.getRowId()
		#d = self._values
		atomicRow = area._connection.executePeek(area._table, id)
		if self._new:
			if atomicRow is not None:
				raise DataVeto("Cannot create another %s row %s" \
									% (self.__class__.__name__, id))
		else:
			if atomicRow is None:
				#self.__dict__['_new'] = True
				raise DataVeto("Cannot find %s row %s" \
									% (self.__class__.__name__, id))
				
## 				raise DataVeto("Cannot find %s row %s" \
## 									% (self.__class__.__name__, id))

			
		if atomicRow is None:
			for attr in self._area._table._rowAttrs.values():
				self._values[attr.getAttrName()] = None
		else:
			q = self._area._table.query()
			q.atoms2dict( atomicRow, self._values, self._area)
		#for col in self._area._table.peekQuery.getColumns():
			
		#	col.atoms2dict(atomicRow,d,self._area)
		"""maybe a third argument `fillMode` to atoms2dict() which
		indicates whether existing (known) values should be
		overwritten, checked for equality or ignored...	 """

##			for atom in self.table.peekQuery.getAtoms():
##				if d.has_key(atom.name):
##					assert d[atom.name] == atomicRow[atom.index]
##				else:
##					d[atom.name] = atomicRow[atom.index]
		
		self.__dict__['_complete'] = True
		self.__dict__["_isCompleting"] = False

	def exists(self):
		if not self._complete:
			self._readFromStore()
		return not self.isNew()

	def checkIntegrity(self):
		if not self._complete:
			self._readFromStore()
		for name,attr in self._area._table._rowAttrs.items():
			if isinstance(attr,Pointer):
				pointedRow = getattr(self,name)
				if pointedRow is not None:
					if not pointedRow.exists():
						return "%s points to non-existing row %s" % (
							name,str(pointedRow.getRowId()))
		
	def getAttrValues(self,columnNames=None):
		l = []
		if columnNames is None:
			q = self._area._table.query()
			for col in q.getColumns():
				attr = col.rowAttr 
				l.append( (attr,attr.getValueFromRow(self)) )
		else:
			for name in columnNames.split():
				attr = self._area._table.__getattr__(name) 
				l.append( (attr,attr.getValueFromRow(self)) )
		return tuple(l)
		
	
	def __repr__(self):
		return self.__class__.__name__ + repr(self.getRowId())

	def __str__(self):
		return str(self.getLabel())



##			d = {}
##			for k,v in self._values.items():
##				if v is not None:
##					# col = self.table.findColumn(k)
##					#if isinstance(col,Field):
##					d[k] = v
##			return "%s <%s>" % (self.__class__.__name__,
##									 repr(d))

								  
##			from textwrap import wrap
##			rows = []
##			w1 = 4
##			for k,v in self._values.items():
##				rows.append( (k, repr(v) ) )
##				if len(k) > w1:
##					w1 = len(k)
##			lines = []
##			for row in rows:
##				cellLines = wrap(row[1],70-w1)
##				lines.append("%s : %s" % (row[0],cellLines[0]))
##				for cl in cellLines[1:]:
##					lines.append(" "*w1+"	"+cl)

##			return "%s:\n%s" % (self.__class__.__name__,
##									  "\n".join(lines))

	def asBody(self,renderer):
		self.asPage(renderer)
		self.asFooter(renderer)

	def asLeftMargin(self,renderer):
		renderer.write('<p><a href="add">add row</a>')
		renderer.write('<br><a href="delete">delete row</a></p>')
		self._area._db.asLeftMargin(renderer)


	def asPreTitle(self,renderer):
		pass
	
	def asFooter(self,renderer):
		pass

	def asFormCell(self,renderer):
		self.asParagraph(renderer)

	def asLabel(self,renderer):
		renderer.renderLink(
			url=renderer.uriToRow(self),
			label=self.getLabel())
		
	def asPage(self,renderer):
		renderer.writeForm(self.getAttrValues())

	def renderDetails(self,renderer):
		pass
## 		wr = renderer.write
## 		if False:
## 			wr("<ul>")
## 			for (name,dtl) in self._area._table._details.items():
## 				rpt = dtl.query(self)
## 				wr('<li>')
## 				rpt.asParagraph(renderer)
## 				wr("</li>")

## 			wr("</ul>")
		
			
	def asParagraph(self,renderer):
		return self.asLabel(renderer)
## 		wr = renderer.write
## 		for name,attr in self._area._table._rowAttrs.items():
## 			if not name in ('body'):
## 				value = getattr(self,name)
## 				if value is not None:
## 					wr('<b>%s:</b> ' % name)
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
## 					wr(" ")


	


class WritableRow(BaseRow):

	def __init__(self,
					 rowId,
					 knownValues=None,
					 #complete=False,
					 new=False):
		BaseRow.__init__(self,rowId,knownValues,new)
		#BaseRow.__init__(self,rowId,knownValues,complete,new)
		assert type(new) == types.BooleanType
		self.__dict__["_dirty"] = new
		self.__dict__["_lockedBy"] = None


	def setDirty(self,dirty=True):
		self.__dict__["_dirty"] = dirty

	def isDirty(self):
		return self.__dict__['_dirty']
	
	def registerLock(self,ds):
		if self._lockedBy is None:
			self.__dict__["_lockedBy"] = ds
			return True
		

	def unregisterLock(self,ds):
		if self._lockedBy is not ds:
			raise "this row was not locked by this ds"
		self.__dict__["_lockedBy"] = None
		# self._area.unlockRow(self)
		


	def defineMenus(self,win):
		#self.initQuery()
		mb = win.addMenuBar("row","&Row menu")
		mnu = mb.addMenu("&Row")
		mnu.addItem("&Edit",self.mnu_toggleEdit,win)
		# mnu.addItem("&Delete",self.mnu_deleteRow)
		# w.addGrid(self)
		# return mb
		mnu = mb.addMenu("&File")
		mnu.addItem("E&xit",win.close)

	def mnu_toggleEdit(self,win):
		pass

	def vetoDelete(self):
		for name,attr in self._area._table._rowAttrs.items():
			msg = attr.vetoDeleteIn(self)
			if msg:
				return msg


