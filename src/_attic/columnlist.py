#----------------------------------------------------------------------
# $Id: columnlist.py,v 1.2 2004/04/25 18:06:12 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
from lino.misc.compat import *
from rowattrs import Field, Pointer #, AREATYPE


class ColumnList:

	def __init__(self,query):
		self.query = query
		self._columns = []
		#self.editable = False
		self._joins = []
		self._atoms = None
		


 	def mustSetup(self):
 		return self._atoms is None

	def provideColumn(self,name):#,isVisible=False):
		col = self.findColumn(name)
		if col is not None:
			return col

		self._atoms = None # mustSetup()
		
		cns = name.split('.')
		join = None # parent of potential join
		joinName = cns[0]
		table = self.query.leadTable
		while len(cns) > 1:
			pointer = table.getRowAttr(cns[0])
			assert isinstance(pointer,Pointer)
			newJoin = self._provideJoin(joinName,
												 pointer,
												 join)
			table = pointer._toTables[0]
			join = newJoin
			del cns[0]
			joinName += "_" + cns[0]

		cns = cns[0]
## 		if cns.endswith(']'):
## 			i = cns.index('[')
## 			lng = cns[i+1:-1]
## 			# print "TODO", repr(lng)
## 			lngIndex = 0
## 			attrName = cns[:i]
## 			rowAttr = table.getRowAttr(attrName)
## 			col = BabelQueryColumn(self, len(self._columns), name,
## 										  join,rowAttr,lngIndex)
## 		else:
		rowAttr = table.getRowAttr(cns)
		col = QueryColumn(self, len(self._columns), name,
								join,rowAttr)
		self._columns.append(col)
		return col

			
	def setupAtoms(self):
		# called from QueryCtrl.__init__()
		if not self.mustSetup():
			return
		self._atoms = []
		for (name,type) in self.query.leadTable.getPrimaryAtoms():
			self.provideAtom(name,type)
		
		"""first of all the primary key of the leadTable.  in fact this
		is necessary only for writable queries but optimization comes
		later."""

		for join in self._joins:
			join.setupAtoms()
			
		for col in self._columns:
			col.setupAtoms()

		

	def getColumns(self):
		#assert self.isSetup()
		#? self.initQuery()
		return self._columns

	
	def getAtomicNames(self):
		#assert self.isSetup()
		#? self.initQuery()
		return " ".join([a.name for a in self.getAtoms()])

	def getSqlSelectTable(self,
								 conn,
								 ctrl,
								 leadTable,
								 sqlColumnNames=None,
								 limit=None,
								 offset=None) :

		#self.initQuery()
		if sqlColumnNames is None:
			sqlColumnNames = ''
		else:
			sqlColumnNames += ', '
			
		sqlColumnNames += ", ".join([a.getNameInQuery(self)
											  for a in self.getAtoms()])
		#if samples is None:
		#	samples = self.samples
		
		sql = "SELECT " + sqlColumnNames
		
		sql += "\nFROM " + leadTable.name
		
		if self.hasJoins():
			
			sql += " AS lead"
			
			for join in self._joins:
				if len(join.pointer._toTables) == 1:
					toTable = join.pointer._toTables[0]
					sql += '\n	LEFT JOIN ' + toTable.name
					sql += ' AS ' + join.name 
					sql += '\n	  ON ('
					l = []
					for (a,b) in join.getJoinAtoms():
						l.append("%s = %s" % (a.getNameInQuery(self),
													 b.getNameInQuery(self)) )
					sql += " AND ".join(l) + ")"
				else:
					joinAtoms = join.getJoinAtoms()
					if join.parent is None:
						if self.hasJoins():
							parentJoinName = "lead."
						else:
							parentJoinName = ""
					else:
						parentJoinName = join.parent.name+"."
					i = 0
					for toTable in join.pointer._toTables:
						sql += '\n	LEFT JOIN ' + toTable.name
						sql += ' AS ' + join.name + toTable.name
						sql += '\n	  ON ('
						l = []
						#l.append("%s_tableId = %d" % (
						#	parentJoinName+join.name,toTable.getTableId()))
						for (name,type) in toTable.getPrimaryAtoms():
							(a,b) = joinAtoms[i]
							l.append("%s = %s" % (a.getNameInQuery(self),
														 b.getNameInQuery(self)) )
							i += 1
						sql += " AND ".join(l) + ")"
				
		where = []

## 		if len(ctrl.atomicSamplesColumns) > 0:
## 			for (atom,value) in ctrl.atomicSamplesColumns:
## 				where.append("%s = %s" % (atom.name,
## 												  conn.value2sql(value,
## 																	  atom.type)))

		for (atom,value) in ctrl.sampleColumns:
			where.append(conn.testEqual(atom.name,atom.type,value))			
			
## 		for (col,value) in self.getSampleColumns(samples):
## 			w = col.
## 			if isinstance(col.rowAttr,Pointer):
## 				avalues = value.getRowId()
## 			else:
## 				avalues = (value,)

## 			i = 0
## 			for atom in col.getAtoms():
## 				where.append("%s = %s" % (atom.name,
## 												  conn.value2sql(avalues[i],
## 																	  atom.type)))
## 				i += 1
					

		where += ctrl.filterExpressions
		
		if len(where):
			sql += "\n	WHERE " + "\n	  AND ".join(where)

				
		if len(ctrl.orderByColumns) >  0 :
			l = []
			for col in ctrl.orderByColumns:
				#col = self.findColumn(colName)
				#if col:
					for atom in col.getAtoms():
						l.append(atom.getNameInQuery(self))
				#else:
				#	raise "%s : no such column in %s" % \
				#			(colName,
				#			 [col.name for col in self.getColumns()])
			sql += "\n	ORDER BY " + ", ".join(l)

		if limit is not None:
			if offset is None:
				sql += " LIMIT %d" % limit
				#offset = 0
			else:
				sql += " LIMIT %d OFFSET %d" % (limit,offset)
				
		return sql
	




	#def initQuery(self):
	#	pass
	
	def findColumn(self,name):
		#assert self.isSetup(),\
		#		 "%s.findColumn() before setup()" % self.getName()
		# ... self.setupAtoms()
		#for col in self.getColumns():
		for col in self._columns:
			if col.name == name:
				return col
		return None

	def getColumn(self,name):
		col = self.findColumn(name)
		if col is None:
			raise "No column '%s' in %s" % (
				name, repr([col.name for col in self._columns]))
		return col


## 	def isEditable(self):
## 		return self.editable


	def getAtoms(self):
		#assert self.isSetup()
		#self.initQuery()
		#assert self._atoms is not None
		return self._atoms
	

##  	def isSetup(self):
##  		return self._atoms is not None
	
## 	def isSetup(self):
## 		return not self.mustInit()
	

	def provideAtom(self,name,type,joinName=None):
		
		"""Return the atom with specified name if already present.	type
		must match in this case.  Create the atom if not present. """

		assert not self.mustSetup()
		
		# 20030816 self.setupAtoms()
		for atom in self._atoms:
			if atom.name == name:
				if atom.joinName == joinName:
					assert atom.type == type,\
							 "%s is not type %s" % (repr(atom),str(type))
					#if alias != name:
					#	 if atom.alias is None:
					#		 atom.alias = alias
					#	 else:
					#		 assert atom.alias == alias
					return atom
		a = Atom(joinName,name,type,len(self._atoms))
		self._atoms.append(a)
		return a

	def getAtom(self,name):
		for a in self._atoms:
			if a.name == name:
				return a
		raise "%s : no such atomic column" % name

		
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
		return j


			
	def hasJoins(self):
		return len(self._joins) != 0


	def findAtom(self,joinName,name):
		for atom in self._atoms:
			if atom.name == name and atom.joinName == joinName:
				return atom
		return None


	def atoms2dict(self,atomicRow,rowValues,area):
		for col in self._columns:
			if col.join is None:
				col.atoms2dict(atomicRow,rowValues,area)
			
## 	def atoms2values(self,atomicRow,area):
## 		raise "replaced by datasource.atoms2values?"
## 		cl = [self.getColumn(colName)
## 				for colName in self._columnList.split()]
##  		return [col.atoms2value(atomicRow,area)
##  				  for col in cl]
		






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
		return "Atom(%s,%s,%d)" % (#repr(self.join),
											self.name,
											self.type,
											self.index)


		
class Join:
	
	def __init__(self,query,name,pointer,parent=None):
		self.name = name
		self.query = query
		self.parent = parent
		# self.table = pointer.toTable
		self.pointer = pointer
		self._joinedTables = []
		#	jt = JoinedTable(toTable)
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
				a = self.query.provideAtom(
					shortJoinName+"_"+name,
					type,parentJoinName)
				b = self.query.provideAtom( name, type, self.name)
				self._atoms.append((a,b))
		else:
			#self.query.provideAtom(self.name+"_tableId",
			#							  AREATYPE, self.parent)
			for toTable in self.pointer._toTables:
				for (name,type) in toTable.getPrimaryAtoms():
					a = self.query.provideAtom(
						shortJoinName+toTable.name+"_"+name,
						type,parentJoinName)
					b = self.query.provideAtom( name,
														 type,
														 self.name+toTable.name)
														 # 20040319
					self._atoms.append((a,b))

	def getJoinAtoms(self):
		return self._atoms

## 	def getJoinedRowId(self,atomicRow):
## 		raise "not used?"
## 		pk = self.toTable.getPrimaryAtoms()
## 		rid = []
## 		for (name,type) in pk:
## 			atom = self.query.findAtom(self,name)
## 			assert atom.type == type,\
## 					 "%s != %s" % (repr(atom.type),repr(type))
## 			rid.append(atomicRow[atom.index])
## 		return tuple(rid)

	def __repr__(self):
		return "Join(%s,%s)" % (self.name,repr(self.parent))



class QueryColumn:
	
	def __init__(self,query,index,name,join,rowAttr):
		# Describable.__init__(self,rowAttr)
		self.query = query
		self.index = index
		self.name = name
		self.sticky = False
		self.rowAttr = rowAttr
		self.join = join
		#self.isVisible = isVisible
		#self.width = rowAttr.width
		
		self._atoms = None

		# self._atoms is list of those atoms in query which have been
		# requested for this column


	def __str__(self):
		return self.name

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
		l = self.getNeededAtoms()
		#print repr(l)
		for (name,type) in self.getNeededAtoms():
			if self.join and len(self.join.pointer._toTables) > 1:
				for toTable in self.join.pointer._toTables:
					a = self.query.provideAtom( name, type,
														 joinName+toTable.name)
					atoms.append(a)
			else:
				a = self.query.provideAtom( name, type,joinName)
				atoms.append(a)

		self._atoms = tuple(atoms)


	#def preferredWidth(self):
	#	return self.rowAttr.type.width

	#def atoms2row(self,atomicRow,rowValues):
	def atoms2dict(self,atomicRow,valueDict,area):
		"""Fill rowValues with values from atomicRow"""
		self.rowAttr.atoms2dict(atomicRow,valueDict,self._atoms,area)
## 		attr = self.rowAttr
## 		valueDict[attr.name] = attr.atoms2value(atomicRow,
## 															 self._atoms,
## 															 area)

	def atoms2value(self,atomicRow,area):
		return self.rowAttr.atoms2value(atomicRow,self._atoms,area)
	


	#def row2atoms(self,rowValues,atomicRow):
	def dict2atoms(self,rowValues,atomicRow):
		self.rowAttr.dict2atoms(rowValues,atomicRow,self._atoms)


	def getAtoms(self): return self._atoms

	def getNeededAtoms(self):
		return self.rowAttr.getNeededAtoms()
	
	
##		def atoms2row(self,atomicRow,row):
##			values = row.getValues()
##			id = []
##			for atom in self._atoms:
##				id.append(atomicRow[atom.index])
##			values[self.name] = tuple(id)

	
	  


		#return self.query.provideRow(atomicRow)

			






class BabelQueryColumn(QueryColumn):
	
	def __init__(self,query,index,name,join,rowAttr,lngIndex):
		raise 'BabelQueryColumn is not usable'
		QueryColumn.__init__(self,query,index,name,join,rowAttr)
		self.lngIndex = lngIndex
		
	def getNeededAtoms(self):
		a = self.rowAttr.getNeededAtoms()
		return (a[self.lngIndex],)
