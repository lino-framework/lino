#----------------------------------------------------------------------
# $Id: query.py,v 1.26 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
#from new import classobj

from datatypes import DataVeto

from lino.misc.compat import *
from lino.misc.etc import issequence

#from datasource import Datasource
#from row import WritableRow
#from columnlist import ColumnList
from paramset import ParamOwner
import datatypes

from rowattrs import Detail, Pointer, NoSuchField


class BaseColumnList: 
	
	def __init__(self,context):
		# a context is either a session or a database
		self._columns = []
		self._joins = []
		self._atoms = []
		self._context = context

	def getContext(self):
		return self._context
		
	def setVisibleColumns(self,columnNames):
		l = []
		if columnNames is None:
			fc = self.getFieldContainer()
			for fld in fc.getFields():
				col = self.findColumn(fld.getName())
				if col is None:
					col = self.addColumn(fld,None,fld.getName())
				l.append(col)
		else:
			assert type(columnNames) is types.StringType
			for colName in columnNames.split():
				l.append(self.provideColumn(colName))
		self.visibleColumns = tuple(l)
			

	def atoms2values(self,atomicRow,sess):
		raise "won't work?"
		atomicValues = [atomicRow[atom.index] for atom in self._atoms]
 		return [col.atoms2value(atomicValues,sess)
 				  for col in self.visibleColumns]


##  	def report(self,name,**kw):
## 		try:
## 			r = self._reports[name]
## 		except KeyError,e:
			
## 			# todo : here we define a new report. This should be
## 			# prohibited after schema startup...
			
## 			r = Report(self,name=name,**kw)
## 			self._reports[name] = r
## 			return r
## 		if len(kw) == 0:
## 			return r
## 		return r.child(name,**kw)

	def getName(self):
		return self.name

	def getLeadColumnList(self):
		raise NotImplementedError




 	def mustSetup(self):
 		return self._atoms is None

	def provideColumn(self,name):#,isVisible=False):
		col = self.findColumn(name)
		if col is not None:
			return col
		
		#print "provide new column", name
		cns = name.split('.')
		join = None # parent of potential join
		joinName = cns[0]
		fc = self.getFieldContainer()
		while len(cns) > 1:
			pointer = fc.getRowAttr(cns[0])
			assert isinstance(pointer,Pointer)
			newJoin = self._provideJoin(joinName,
												 pointer,
												 join)
			fc = pointer._toTables[0]
			join = newJoin
			del cns[0]
			joinName += "_" + cns[0]

		cns = cns[0]
		rowAttr = getattr(fc,cns,None)
		if rowAttr is None:
			raise NoSuchField,name
		return self.addColumn(rowAttr,join,name)
	
	def addColumn(self,fld,join,name):
		#col = self._ds.columnClass(self, len(self._columns),
		#									name, join,fld)
		col = self.createColumn(len(self._columns), name, join,fld)
		self._columns.append(col)
		col.setupAtoms()
		return col

	def createColumn(self,colIndex,name,join,fld):
		# overridden by Report
		return DataColumn(self,colIndex,name,join,fld)

			
	def getColumns(self,columnNames=None):
		if columnNames is None:
			return self._columns
		l = []
		for name in columnNames.split():
			col = self.findColumn(name)
			if col is not None:
				l.append(col)
		return l

	def getFltAtoms(self,context):
		l = []
		for col in self._columns:
			l += col.getFltAtoms(context)
		return l

	
	def getAtomicNames(self):
		#assert self.isSetup()
		#? self.initQuery()
		return " ".join([a.name for a in self.getAtoms()])


	def findColumn(self,name):
		for col in self._columns:
			if col.name == name:
				return col
		#print "query.py: ", [col.name for col in self._columns]
		return None

	def getColumn(self,name):
		col = self.findColumn(name)
		if col is None:
			msg = "No column '%s' in %s (%s)" % (
				name,
				self.leadTable.getTableName(),
				', '.join([col.name for col in self._columns]))
			raise DataVeto(msg)
		return col


	def getAtoms(self):
		return self._atoms
	
	

	def provideAtom(self,name,type,joinName=None):
		
		"""Return the atom with specified name if already present.	type
		must match in this case.  Create the atom if not present. """

		a = self.findAtom(joinName,name)
		if a is not None:
			assert a.type == type,\
					 "%s is not type %s" % (repr(a),str(type))
			return a
		a = Atom(joinName,name,type,len(self._atoms))
		self._atoms.append(a)
		return a

		
	#def getJoins(self): return self._joins

  
	def getJoinList(self):
		l = [j.name for j in self._joins]
		return " ".join(l)

		
	def _provideJoin(self,name,pointer,parent):
		for j in self._joins:
			if j.name == name:
				assert j.pointer == pointer
				# assert j.table == table
				assert j.parent == parent
				return j
		j = Join(self,name,pointer,parent)
		self._joins.append(j)
		j.setupAtoms()
		return j


			
	def hasJoins(self):
		return len(self._joins) != 0


	def findAtom(self,joinName,name):
		for atom in self._atoms:
			if atom.name == name and atom.joinName == joinName:
				return atom
		return None

	def getAtom(self,name):
		for a in self._atoms:
			if a.name == name:
				return a
		raise "%s : no such atomic column" % name






	def updateRow(self,row,*args,**kw):
		i = 0
		for col in self.visibleColumns:
			if i == len(args):
				break
			col.setCellValue(row,args[i])
			#row._values[col.rowAttr._name] = args[i]
			i += 1
			
		for k,v in kw.items():
			col = self.getColumn(k)
			col.setCellValue(row,v)
			#rowattr = self.leadTable.getRowAttr(k)
			#row._values[rowattr._name] = v
			#rowattr.setCellValue(row,v)
			
		row.setDirty()
			
	


	def atoms2dict(self,atomicRow,rowValues,area):
		for col in self._columns:
			if col.join is None:
				col.atoms2dict(atomicRow,rowValues,area)
			
	def atoms2row(self,atomicRow,row):
		#for join in self._joins:
		#	join.atoms2row(atomicRow,row)
		for col in self._columns:
			col.atoms2row(atomicRow,row)
			

	def ad2t(self,d):
		"atomic dict to tuple"
		atomicTuple = [None] * len(self._atoms)
		for k,v in d.items():
			a = self.getAtom(k)
			atomicTuple[a.index] = v
		return atomicTuple
	
## 	def at2d(self,atomicTuple):
## 		"atomic tuple to dict"
## 		joinedRows = {}
## 		d = {}
## 		i = 0
## 		for a in self._atoms:
## 			if a.join is None:
## 				d[a.name] = atomicTuple[i]
## 			else:
## 				pointedRow = a.join.pointer
## 				joinedRows.setdefault(a.join.name,a.join.pointer)
## 				joinedRows[a.join.name][a.name] = atomicTuple[i]
## 			i += 1
## 		return d

	def makeAtomicRow(self,context=None,*args,**kw):
		atomicRow = [None] * len(self._atoms) 
		i = 0
		for col in self.visibleColumns:
			if i == len(args):
				break
			#col.setCellValue(row,args[i])
			col.value2atoms(args[i],atomicRow,context)
			i += 1
			
		for k,v in kw.items():
			col = self.getColumn(k)
			col.value2atoms(v,atomicRow,context)
		return atomicRow

		
	def row2atoms(self,row,atomicRow=None):
		if atomicRow is None:
			atomicRow = [None] * len(self._atoms) # _pkaLen
		for col in self._columns:
			col.row2atoms(row,atomicRow)
		return atomicRow








		

class DataColumnList(BaseColumnList):
	
	def __init__(self, store, context, columnNames=None):
		self.leadTable = store._table 

		BaseColumnList.__init__(self,context)
		
		l = []
		for name in self.leadTable.getPrimaryKey():
			l.append(self.provideColumn(name))
		self._pkColumns = tuple(l)

		self.setVisibleColumns(columnNames)
		

	def __repr__(self):
		return self.leadTable.getTableName()+"Query(%s)" % \
				 [col.name for col in self._columns]


## 	def getContext(self):
## 		return self._ds.getContext()
## 		#return self._store._db
	
	def getFieldContainer(self):
		return self.leadTable

	def getSearchAtoms(self):
		l = []
		for col in self.visibleColumns:
			if hasattr(col.rowAttr,'type'):
				if isinstance(col.rowAttr.type,datatypes.StringType):
					l += col.getAtoms()
		return tuple(l)
		
	
	def atoms2instance(self,atomicRow,area):

		"""returns a leadTable row instance which contains the values of
		the specified atomic row. """

		d = {}
		self.atoms2dict(atomicRow,d,area)
		#print d
		
		# the primary key atoms of the leadTable are always the first
		# ones
		pklen = len(self.leadTable.getPrimaryAtoms())
		row = area.provideRowInstance(atomicRow[:pklen],
												knownValues=d,
												new=False)
		
		# todo : `fillMode` to indicate that known atoms are expected to
		# match if row was in cache

		
		
		return row



	def commit(self):
		self.leadTable.commit()


	def values2id(self,knownValues):
		"convert dict of knownValues to sequence of pk atoms"
		#print knownValues
		#pka = self.leadTable.getPrimaryAtoms()
		#id = [None] * len(pka)
		
		id = [None] * len(self.leadTable.getPrimaryAtoms()) # _pkaLen
		#print self.name, knownValues
		for col in self._pkColumns:
			col.dict2atoms(knownValues,id)
		return id

	



class Atom:
	"""
	An Atom represents one SQL column
	"""
	def __init__(self,joinName,name,atype,index):
		#self.join = join
		self.type = atype
		self.index = index
		self.name = name
		self.joinName = joinName
		assert (joinName is None) or type(joinName) is types.StringType
		

	def getNameInQuery(self,query):
		
		""" the name of an unjoined atom (that is, an atom in the
		leadTable) depends on whether the query has Joins or not. And
		this is not known when the first atoms are being setup."""
		
		if self.joinName is None:
			if query.hasJoins():
				return "lead." + self.name
			else:
				return self.name
		return self.joinName+'.'+self.name
		#return self.name # 20040319

	def __repr__(self):
## 		return "Atom(%s,%s,%d)" % (#repr(self.join),
## 											self.name,
## 											self.type,
## 											self.index)

		return "<atom %d:%s>" % (self.index,self.name)




		
class Join:
	
	def __init__(self,query,name,pointer,parent=None):
		self.name = name
		self.query = query
		self.parent = parent
		self.pointer = pointer
		self._joinedTables = []
		self._atoms = None
		
		"""self._atoms is a list of (a,b) couples where a and b are
		atoms used for the join.  """

		
	def setupAtoms(self):
		assert self._atoms is None
		self._atoms = []
		shortJoinName = self.name.split("_")[-1]
		if self.parent is None:
			parentJoinName = None
		else:
			parentJoinName = self.parent.name
			
		if len(self.pointer._toTables) == 1:
			for (name,type) in self.pointer._toTables[0].getPrimaryAtoms():
				a = self.query.provideAtom( shortJoinName+"_"+name,
													 type,
													 parentJoinName)
				b = self.query.provideAtom( name,
													 type,
													 self.name)
				self._atoms.append((a,b))
		else:
			for toTable in self.pointer._toTables:
				for (name,type) in toTable.getPrimaryAtoms():
					a = self.query.provideAtom(
						shortJoinName+toTable.getTableName()+"_"+name,
						type,
						parentJoinName)
					b = self.query.provideAtom(
						name,
						type,
						self.name+toTable.getTableName())
					self._atoms.append((a,b))

	def getJoinAtoms(self):
		return self._atoms


	def __repr__(self):
		return "Join(%s,%s)" % (self.name,repr(self.parent))














class DataColumn:
	
	def __init__(self,query,index,name,join,rowAttr):
		self.query = query
		self.index = index
		self.name = name
		self.sticky = False
		self.rowAttr = rowAttr
		self.join = join
		#self.isVisible = isVisible
		#self.width = rowAttr.width
		
		self._atoms = None

		# self._atoms is list of those atoms in ColumnList which have
		# been requested for this column


	def __str__(self):
		return self.name

	def __repr__(self):
		return "<column %d:%s in %s>" % (self.index,self.name,
													repr(self.query))

##  	def getLabel(self):
##  		return self.name

	def setupAtoms(self):
		#assert self._atoms is None
		atoms = []
##			if self.join is None:
##				if self.query.hasJoins(): # len(query._joins) == 0:
##					atomprefix = "lead."
##				else:
##					atomprefix = ""
##			else:
##				atomprefix = join.name + "." 

		if self.join:
			joinName = self.join.name
		else:
			joinName = None
		#l = self.getNeededAtoms()
		#print repr(l)
		ctx = self.query.getContext()
		for (name,type) in self.rowAttr.getNeededAtoms(ctx):
			if self.join and len(self.join.pointer._toTables) > 1:
				for toTable in self.join.pointer._toTables:
					a = self.query.provideAtom(
						name, type,
						joinName+toTable.getTableName())
					atoms.append(a)
			else:
				a = self.query.provideAtom( name, type,joinName)
				atoms.append(a)

		self._atoms = tuple(atoms)


	def setCellValue(self,row,value):
		#print self, value
		self.rowAttr.setCellValue(row,value)
		self.rowAttr.afterSetAttr(row)

	def getFltAtoms(self,context):
		return self.rowAttr.getFltAtoms(self._atoms,context)
		
	def getTestEqual(self,ds,value):
		return self.rowAttr.getTestEqual(ds,self._atoms,value)
		
		
 	def getCellValue(self,row):
		if self.join is None:
			return self.rowAttr.getCellValue(row)
		row = getattr(row,self.join.name)
		if row is None: return None
		return self.rowAttr.getCellValue(row)
		

	def atoms2row(self,atomicRow,row):
		if self.join is None:
			self.rowAttr.atoms2row(atomicRow,self._atoms,row)
		else:
			#print "query.py", joinedRow
			row = getattr(row,self.join.name)
			if row is None: 
				return
			self.rowAttr.atoms2row(atomicRow,self._atoms,row)
## 			try:
## 				joinedRow = row._values[self.join.name]
## 			except KeyError:
## 				joinedRow = self.join.pointer.
## 				row._values[self.join.name] = joinedRow
		
	def atoms2dict(self,atomicRow,valueDict,area):
		"""Fill rowValues with values from atomicRow"""
		self.rowAttr.atoms2dict(atomicRow,valueDict,self._atoms,area)
## 		attr = self.rowAttr
## 		valueDict[attr.name] = attr.atoms2value(atomicRow,
## 															 self._atoms,
## 															 area)

	def atoms2value(self,atomicValues,sess):
		#return self.rowAttr.atoms2value(atomicRow,self._atoms,area)
		#atomicValues = [atomicRow[atom.index]
		#					 for atom in self._atoms]
		return self.rowAttr.atoms2value(atomicValues,sess)
	

	def value2atoms(self,value,atomicRow,context):
		values = self.rowAttr.value2atoms(value,context)
		self.values2atoms(values,atomicRow)
		
	def row2atoms(self,row,atomicRow):
		values = self.rowAttr.row2atoms(row)
		self.values2atoms(values,atomicRow)


	def values2atoms(self,values,atomicRow):
		assert len(values) == len(self._atoms)
		i = 0
		for atom in self._atoms:
			atomicRow[atom.index] = values[i]
			i+=1
		
	def getAtoms(self): return self._atoms

#	def getNeededAtoms(self,db):
#		return 
	
	def format(self,value,context):
		raise "no longer used?"
		values = self.rowAttr.value2atoms(value,context)
		#print self, ":", values
		#if len(self._atoms) == 1:
		#	return self._atoms[0].type.format(values[0])
		assert len(values) == len(self._atoms)
		l = [a.type.format(v) for v,a in zip(values,self._atoms)]
		return ",".join(l)
		
	def parse(self,s,ds):
		l1 = s.split(',')
		assert len(l1) == len(self._atoms)
		atomicValues = [a.type.parse(s1)
							 for a,s1 in zip(self._atoms,l1)]
		return self.atoms2value(atomicValues,ds._session)
		
## 	def format(self,v):
## 		return self.rowAttr.format(v)
		
## 	def parse(self,s):
## 		return self.rowAttr.parse(v)
		

