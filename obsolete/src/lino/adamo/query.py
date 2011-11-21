## Copyright 2003-2007 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import types
import codecs

from lino.adamo.exceptions import DataVeto, \
     NoSuchField, InvalidRequestError

from lino.misc.compat import *
from lino.misc.etc import issequence

from lino.adamo import datatypes
from lino.adamo.row import DataRow

from lino.adamo.rowattrs import Detail, Pointer, Field, BabelField, \
     is_reserved

FETCHONE=False

class QueryColumn:
    
    def __init__(self,owner,index,name,rowAttr,
                 join=None,atoms=None):
        self._owner = owner
        self.index = index
        self.name = name
        self.rowAttr = rowAttr
        self.join = join
        self._atoms = atoms
        # self._atoms is list of those atoms in ColumnList which have
        # been requested by this column


    def __str__(self):
        return self.name

    def __repr__(self):
        return "<column %d:%s in %r>" % (self.index,self.name,
                                         self._owner)
    
    def canWrite(self,row):
        return self.rowAttr.canWrite(row)

    def getValueClass(self):
        raise NotImplementedError
    
    def isMandatory(self):
        return self.rowAttr in \
               self._owner.getLeadTable()._mandatoryColumns


    def setupColAtoms(self,db):
        #assert self._atoms is None
        atoms = []
        if self.join:
            joinName = self.join._sqlName
        else:
            joinName = None
        for (name,type) in self.rowAttr.getNeededAtoms(db):
            if self.join and len(self.join.pointer._toTables) > 1:
                for toTable in self.join.pointer._toTables:
                    a = self._owner.provideAtom(
                        name, type,
                        joinName+toTable.getTableName())
                    atoms.append(a)
            else:
                a = self._owner.provideAtom(name,type,joinName)
                atoms.append(a)

        self._atoms = tuple(atoms)

    def addFilter(self,fcl,*args,**kw):
        # deprecated : modifies the owner
        flt=fcl(self,*args,**kw)
        self._owner.addFilter(flt)


    def validate(self,value):
        try:
            self.rowAttr.validate(value)
        except DataVeto,e:
            raise DataVeto("%s.%s=%r: %s" % (
                self._owner.getTableName(),self.name,value,e))
        
    def setCellValue(self,row,value):
        #self.rowAttr.canSetValue(row,value)
        row.setDirtyRowAttr(self.rowAttr)
        try:
            self.rowAttr.setCellValue(row,value)
        except DataVeto,e:
            raise DataVeto("%s.%s=%r: %s" % (
                self._owner.getTableName(),self.name,value,e))
        #self.rowAttr.afterSetAttr(row)
        #self.rowAttr.trigger(row)

    def setCellValueFromString(self,row,s):
        # does not setDirty() !
        if len(s) == 0:
            self.setCellValue(row,None)
        else:
            v=self.parse(s)
            self.setCellValue(row,v)
    
    
##     def setCellValueFromString(self,row,s):
##         self.rowAttr.setCellValueFromString(row,s)
##         #self.rowAttr.afterSetAttr(row)
##         self.rowAttr.trigger(row)
        
    def getFltAtoms(self,context):
        return self.rowAttr.getFltAtoms(self._atoms,context)
        
    def getTestEqual(self,ds,value):
        assert len(self._atoms) == 1
        a=self._atoms[0]
        return ds._connection.testEqual(a.name,a.type,value)
        
        
##     def getCellValue(self,row):
##         if self.join is None:
##             return self.rowAttr.getCellValue(row,self)
##         row = getattr(row,self.join.name)
##         if row is None: return None
##         return self.rowAttr.getCellValue(row,self)
        
    def getCellValue(self,row):
        if self.join is not None:
            row = getattr(row,self.join.name)
            if row is None: return None
        return self.extractCellValue(row)
        
    def extractCellValue(self,row):
        # overridden by BabelFieldColumn and DetailColumn
        assert isinstance(row, DataRow),\
            "%s.extractCellValue() : %r is not a DataRow" % (self,row)
        return row.getFieldValue(self.rowAttr.name)


    def col_atoms2row(self,atomicRow,row):
        #print "col_atoms2row()", self.name
        if self.join is None:
            self.rowAttr.atoms2row(atomicRow,self._atoms,row)
        else:
            #print "query.py", joinedRow
            row = getattr(row,self.join.name)
            if row is None: 
                return
            self.rowAttr.atoms2row(atomicRow,self._atoms,row)
        
    def atoms2dict(self,atomicRow,valueDict,area):
        """Fill rowValues with values from atomicRow"""
        self.rowAttr.atoms2dict(atomicRow,valueDict,self._atoms,area)

    def atoms2value(self,atomicValues,dbc):
        #return self.rowAttr.atoms2value(atomicRow,self._atoms,area)
        #atomicValues = [atomicRow[atom.index]
        #                    for atom in self._atoms]
        return self.rowAttr.atoms2value(atomicValues,dbc)
    

    def value2atoms(self,value,atomicRow,context):
        raise NotImplementedError
    
    def row2atoms(self,row,atomicRow):
        raise NotImplementedError
    
##     def row2atoms(self,row,atomicRow):
##         value=row._values.get(self.rowAttr.name)
##         self.value2atoms(value,atomicRow,row.getDatabase())
##     def row2atoms(self,row,atomicRow):
##         values = self.rowAttr.row2atoms(row)
##         self.values2atoms(values,atomicRow)


    def values2atoms(self,values,atomicRow):
        assert len(values) == len(self._atoms)
        i = 0
        for atom in self._atoms:
            atomicRow[atom.index] = values[i]
            i+=1
        
    def getAtoms(self): return self._atoms
    
    def getMaxWidth(self):
        return self.rowAttr.getMaxWidth()
    def getMinWidth(self):
        return self.rowAttr.getMinWidth()
    def getMaxHeight(self):
        return self.rowAttr.getMaxHeight()
    def getMinHeight(self):
        return self.rowAttr.getMinHeight()
    
    def getLabel(self):
        return self.rowAttr.getLabel()

##     def parse(self,s,qry):
##         l1 = s.split(',')
##         assert len(l1) == len(self._atoms)
##         atomicValues = [a.type.parse(s1)
##                         for a,s1 in zip(self._atoms,l1)]
##         return self.atoms2value(atomicValues,qry.getContext())
        
    def format(self,v):
        return self.rowAttr.format(v)
    
    def parse(self,s):
        return self.rowAttr.parse(s)
    
    def getAllowedValues(self,row):
        return None
    # None means that there is no explicit list of allowed values
    
##     def showSelector(self,frm,row):
##         return False


class FieldColumn(QueryColumn):
    
    fieldClass=Field

    def atomize(self,value,ctx):
        return (value,)
    
    def value2atoms(self,value,atomicRow,context):
        self.values2atoms(self.atomize(value,context),atomicRow)
        
    def row2atoms(self,row,atomicRow):
        value=row._values.get(self.rowAttr.name)
        self.value2atoms(value,atomicRow,row.getDatabase())

    def getValueClass(self):
        return self.rowAttr.type
    
class BabelFieldColumn(FieldColumn):
    fieldClass=BabelField
##     def value2atoms(self,value,atomicRow,context):
##         self.values2atoms((value,),atomicRow)
        
##     def row2atoms(self,row,atomicRow):
##         values = self.rowAttr.row2atoms(row)
##         self.values2atoms(values,atomicRow)

##     def row2atoms(self,row,atomicRow):
##         value = row._values.get(self.rowAttr.name)
##         values=self.rowAttr.value2atoms(value, row.getDatabase())
##         self.values2atoms(values,atomicRow)

    def atomize(self,value,ctx):
        # value is a sequence with all langs of db
        dblangs = ctx.getBabelLangs()
        atomicValues = [None] * len(dblangs)
        if value is not None:
            assert issequence(value), \
                   "%s is not a sequence" % repr(value)
            assert len(value) == len(dblangs), \
                   "Expected %d values but got %s" % \
                   (len(dblangs), repr(value))
            i = 0
            for lang in dblangs:
                atomicValues[lang.index] = value[i]
                i += 1
        return atomicValues
        
        
    def row2atoms(self,row,atomicRow):
        value = row._values.get(self.rowAttr.name)
        self.values2atoms(
            self.atomize(value,row.getDatabase()),
            atomicRow)


    def extractCellValue(self,row):
        langs = row.getContext().getBabelLangs()
        dblangs = row.getDatabase().getBabelLangs()
        values = row.getFieldValue(self.rowAttr.name)
        if values is None:
            values = [None] * len(dblangs)
        else:
            assert issequence(values), \
                   "%s is not a sequence" % repr(values)
            assert len(values) == len(dblangs), \
                   "Expected %d values but got %s" % \
                   (len(dblangs), repr(values))
        
        if len(langs) > 1:
            l = []
            for lang in langs:
                if lang.index != -1:
                    l.append(values[lang.index])
                else:
                    l.append(None)
            return l
        else:
            assert langs[0].index != -1,\
                   "Context language %r not supported by %s" \
                   % (langs[0].id,row.getDatabase().getSupportedLangs())
            #print __name__, values[index], langs
            return values[langs[0].index]
        
    def getTestEqual(self,qry,value):
        langs = qry.getContext().getBabelLangs()
        lang = langs[0] # ignore secondary languages
        a = self._atoms[lang.index]
        return qry._connection.testEqual(a.name,a.type,value)
        
        
        
class PointerColumn(FieldColumn):
    fieldClass=Pointer
        
    def row2atoms(self,row,atomicRow):
        value=row._values.get(self.rowAttr.name)
        self.value2atoms(value,atomicRow,row.getDatabase())

##     def value2atoms(self,value,atomicRow,context):
##         values = self.rowAttr.value2atoms(value,context)
##         self.values2atoms(values,atomicRow)

    def atomize(self,value,ctx):
        if value is None:
            return [None]*len(self._atoms)
        if len(self.rowAttr._toTables) == 1:
            return value.getRowId()
        
        values = [None] * len(self._atoms)
        i = 0
        tableId = value._store.getTable().getTableId()
        rid = value.getRowId()
        for toTable in self.rowAttr._toTables:
            if toTable.getTableId() == tableId:
                ai = 0
                for a in toTable.getPrimaryAtoms():
                    values[i] = rid[ai]
                    i+=1
                    ai+=1
                return values
            else:
                i += len(toTable.getPrimaryAtoms())
                
        raise "something wrong?"
        
    def value2atoms(self,value,atomicRow,context):
        values=self.atomize(value,context)
##         if pointedRow is None:
##             values = [None] * len(self._atoms)
##             return self.values2atoms(values,atomicRow)
        
##         if len(self.rowAttr._toTables) == 1:
##             return self.values2atoms(pointedRow.getRowId(),atomicRow)
        
        self.values2atoms(values,atomicRow)

    def getTestEqual(self,ds,value):
        av = [None] * len(ds.getAtoms()) 
        self.value2atoms(value,av,ds.getContext())
        i = 0
        l = []
        for (n,t) in self.rowAttr.getNeededAtoms(ds.getContext()):
            l.append(ds._connection.testEqual(n,t,av[i]))
            i += 1
        return " AND ".join(l)

    def getAllowedValues(self,row):
        dbc=row.getContext()
        return dbc.query(self.rowAttr.type)
        #return self.rowAttr.getTargetSource(row.getContext())
    
    def parse(self,s):
        dbc=self._owner.getContext()
        qry=dbc.query(self.rowAttr.type)
        return qry.parse(s)
##         if self._deleted: return None
##         elif len(self._toTables) > 1:
##             raise NotImplementedError
##         else:
        

##     def showSelector(self,frm,row):
##         sess=frm.session
##         row.lock()
##         ds = self.rowAttr.getTargetSource(row)
##         selectedRow = sess.chooseDataRow(ds,row)
##         if selectedRow is not None:
##             sess.notice("you selected: "+str(row))
##             self.setCellValue(row,selectedRow)
##             #row.setDirty()
##         row.unlock()
##         return True

    def getReachableData(self,row):
        pointedRow = self.getCellValue(row)
        if pointedRow is None:
            return 
        #d = { self.rowAttr.name : pointedRow }
        #return pointedRow._query.child(**d)
        
    def getValueClass(self):
        return self.rowAttr.type # _toClass
    
class DetailValue:
    def __init__(self,row,col):
        self.row=row
        self.col=col

    def __call__(self,*args,**kw):
        for k,v in self.col._queryParams.items():
            kw.setdefault(k,v)
        kw[self.col.rowAttr.pointerName]=self.row
        return self.row.getContext().query(
            self.col.rowAttr.tcl,*args,**kw)
        

        
class DetailColumn(QueryColumn):
    fieldClass=Detail
    def __init__(self,owner,index,name,rowAttr,
                 join=None,atoms=None,depth=0,**kw):
        QueryColumn.__init__(self,owner,index,name,rowAttr,join,atoms)
        for k,v in self.rowAttr._queryParams.items():
            kw.setdefault(k,v)
        self._queryParams=kw
        #self.detailQuery=None
        self.depth=depth

##     def prepare(self):
##         # lazy instanciation of self.detailQuery 
##         if self.detailQuery is None:
##             self.detailQuery=self._owner.getSession().query(
##                 self.rowAttr.pointer._owner._instanceClass,
##                 **self._queryParams)
##             #print "DetailColumn created ", self.detailQuery,\
##             #      self.detailQuery._search
        

    def extractCellValue(self,row):
        #self.prepare()
        return DetailValue(row,self)
        #return self.detailQuery.child(masters=(row,))

##     def getDetailQuery(self):
##         self.prepare()
##         return self.detailQuery


##     def vetoDeleteRow(self,row):
##         detailDs = self.getCellValue(row)
##         if len(detailDs) == 0:
##             return 
##         #return "%s : %s not empty (contains %d rows)" % (
##         #   str(row),self.name,len(ds))
##         return "%s : %s not empty" % (str(row),self.name)
            
        

    def value2atoms(self,value,atomicRow,context):
        values = self.rowAttr.value2atoms(value,context)
        self.values2atoms(values,atomicRow)
        

    def row2atoms(self,row,atomicRow):
        pass

    def format(self,v):
        q=v()
        if self.depth == 0:
            return str(len(q))+" "+q.getLeadTable().getName()
        return ", ".join([unicode(r) for r in q])



    def showSelector(self,frm,row):
        ds = self.getCellValue(row)
        ds.showReport()
        #frm.session.showDataGrid(ds)
        return True


    def getValueClass(self):
        return Query
        #self.prepare()
        #return self.detailQuery
    





class Datasource:
    # abstract base for Query and Report
    def __xml__(self,wr):
        raise NotImplementedError
    
    def setupMenu(self,navigator):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError

    def __getitem__(self,i):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def canWrite(self):
        return False
    
    def canSort(self):
        return False

    def getVisibleColumns(self):
        raise NotImplementedError






class BaseColumnList(Datasource): 
    
    columnClasses=( PointerColumn,
                    BabelFieldColumn,
                    DetailColumn,
                    FieldColumn,
                    )
    
    
    def __init__(self,_parent,columnNames):
        self.rowcount = None
        if _parent is not None and columnNames is None:
            if _parent.getContext() == self.getContext():
                self._frozen=True
                self._columns = tuple(_parent._columns)
                self._joins = tuple(_parent._joins)
                self._atoms = tuple(_parent._atoms)
                self._pkColumns = _parent._pkColumns
                self.visibleColumns=tuple(_parent.visibleColumns)
                self._columnsByName=dict(_parent._columnsByName)
                if _parent._searchAtoms is None:
                    self._searchAtoms = None
                else:
                    self._searchAtoms = tuple(_parent._searchAtoms)
                return
        
        self._columnsByName={}
        self._frozen=False
        self._columns = []
        self._joins = []
        self._atoms = []
        self._searchAtoms = None

        l = []
        for name in self.getLeadTable().getPrimaryKey():
            l.append(self.provideColumn(name))
        self._pkColumns = tuple(l)

        if columnNames is None:
            self.visibleColumns=[]
        else:
            self.setVisibleColumns(columnNames)

                

    def setVisibleColumns(self,columnNames):
        assert type(columnNames) is types.StringType
        #assert type(columnNames) in (str,unicode) 
        l = []
        for colName in columnNames.split():
            if colName == "*":
                for fld in self.getLeadTable().getFields():
                    col = self.findColumn(fld.getName())
                    if col is None:
                        col = self._addColumn(fld.getName(),fld)
                    # may still be None if Detail field is ignored
                    if col is not None:
                        l.append(col)
            else:
                l.append(self.provideColumn(colName))
        self.visibleColumns = tuple(l)
            


    def provideColumn(self,name):#,isVisible=False):
        col = self.findColumn(name)
        if col is not None:
            return col
        
        #print "provide new column", name
        cns = name.split('.')
        join = None # parent of potential join
        joinName = cns[0]
        table = self.getLeadTable()
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
        rowAttr = table.getRowAttr(cns)
        return self._addColumn(name,rowAttr,join)

    
    def addColumn(self,*args,**kw):
        # used in docs/examples/filters2.py
        col=self._addColumn(*args,**kw)
        self.visibleColumns= self.visibleColumns + (col,)
        return col
    
    def _addColumn(self,name,rowAttr=None,join=None,**kw):
        if self._frozen:
            raise InvalidRequestError(
                "Cannot append columns to frozen %r" % self)
        if rowAttr is None:
            rowAttr=self.getLeadTable().getRowAttr(name)
        for ccl in self.columnClasses:
            if isinstance(rowAttr,ccl.fieldClass):
                col=ccl(self,len(self._columns),
                        name, rowAttr, join,**kw)
                self._columns.append(col)
                col.setupColAtoms(self.getDatabase())
                self._columnsByName[name]=col
                return col
        #raise InvalidRequestError("No columnClass")

            
    def getColumns(self,columnNames=None):
        if columnNames is None:
            return self._columns
        
        l = []
        for name in columnNames.split():
            col = self.findColumn(name)
            if col is not None:
                l.append(col)
        return l

    def getVisibleColumns(self):
        return self.visibleColumns
    
    def getFltAtoms(self,context):
        l = []
        for col in self._columns:
            l += col.getFltAtoms(context)
        return l

##     def vetoDeleteRow(self,row):
##         return self.getLeadTable().vetoDeleteRow(row)

    
    def getContext(self):
        # a context is either a session or a database
        raise NotImplementedError
    def getLeadTable(self):
        # the leadTable 
        raise NotImplementedError
    def getName(self):
        return self.name
    def getAtomicNames(self):
        return " ".join([a.name for a in self.getAtoms()])
    def getJoinList(self):
        return " ".join([j.name for j in self._joins])
    def getAtoms(self):
        return self._atoms
    def hasJoins(self):
        return len(self._joins) != 0
    def canWrite(self):
        return True
    

    def findColumn(self,name):
        try:
            return self._columnsByName[name]
        except KeyError,e:
            return None

##     def findColumn(self,name):
##         for col in self._columns:
##             if col.name == name:
##                 return col
##         return None

    def getColumn(self,i):
        return self.visibleColumns[i]
    
    def getColumnByName(self,name):
        col = self.findColumn(name)
        if col is None:
            msg = "No column '%s' in %sQuery(%s)" % (
                name,
                self.getLeadTable().getTableName(),
                ', '.join([col.name for col in self._columns]))
            raise NoSuchField(msg)
        return col


    def provideAtom(self,name,type,joinName=None):
        
        """Return the atom with specified name if already present.
        type must match in this case.
        Create the atom if not present. """

        a = self.findAtom(joinName,name)
        if a is not None:
            assert a.type == type,\
                   "%s: %r is type %s but %s is required" \
                   % (self.getLeadTable().getTableName(),
                      a,a.type,type)
            return a
        a = Atom(joinName,name,type,len(self._atoms))
        self._atoms.append(a)
        return a

        
        
    def _provideJoin(self,name,pointer,parent):
        for j in self._joins:
            if j.name == name:
                assert j.pointer == pointer
                # assert j.table == table
                assert j.parent == parent
                return j
        j = Join(self,name,pointer,parent)
        self._joins.append(j)
        j.setupJoinAtoms()
        return j


            



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




    def atoms2dict(self,atomicRow,rowValues,area):
        raise "not used?"
        for col in self._columns:
            if col.join is None:
                col.atoms2dict(atomicRow,rowValues,area)
            

    def ad2t(self,d):
        "atomic dict to tuple"
        raise "not used?"
        atomicTuple = [None] * len(self._atoms)
        for k,v in d.items():
            a = self.getAtom(k)
            atomicTuple[a.index] = v
        return atomicTuple
    

##     def makeAtomicRow(self,context=None,*args,**kw):
##         atomicRow = [None] * len(self._atoms) 
##         i = 0
##         for col in self.visibleColumns:
##             if i == len(args):
##                 break
##             col.value2atoms(args[i],atomicRow,context)
##             i += 1
            
##         for k,v in kw.items():
##             col = self.getColumnByName(k)
##             col.value2atoms(v,atomicRow,context)
##         return atomicRow

        
    def row2atoms(self,row,atomicRow=None):
        if atomicRow is None:
            atomicRow = [None] * len(self._atoms) # _pkaLen
        for col in self._columns:
            col.row2atoms(row,atomicRow)
        return atomicRow


    def peek(self,*id):
        assert len(id) == len(self._pkColumns),\
                 "expected %d values but got %s" % \
                 ( len(self._pkColumns), repr(id))
        
        # atomize the id :
        l = [None] * len(self.getLeadTable().getPrimaryAtoms())
        i=0
        for col in self._pkColumns:
            col.value2atoms(id[i],l,self.getDatabase())
            i+=1
            
        #print "foo"
        atomicRow = self.executePeek(l)
        if atomicRow is None:
            return None
        #print "bar"    
        row = self.createRow({},False)
        # complete=None: don't know whether it's complete
        # new=False: it certainly exists
        #print "baz"
        self.atoms2row(atomicRow,row)
        #print "brr"
        return row

    def getInstance(self,atomicId,new):
        #row = self.getLeadTable().Instance(self,{},new)
        row = self.createRow({},new)
        i = 0
        for col in self._pkColumns:
            col.col_atoms2row(atomicId,row)
            #col.setCellValue(row,atomicId[i])
            i+=1
        return row
            



class LeadTableColumnList(BaseColumnList):
    
    def __init__(self,_parent,store,columnNames):

        assert store.__class__.__name__ == "Store", \
               store.__class__.__name__+" is not a Store"
        self._store=store
        BaseColumnList.__init__(self,_parent,columnNames)


    
    def atoms2instance(self,atomicRow,area):
        raise "is this still used?"
    
        """returns a leadTable row instance which contains the values of
        the specified atomic row. """

        d = {}
        self.atoms2dict(atomicRow,d,area)
        #print d
        
        # the primary key atoms of the leadTable are always the first
        # ones
        pklen = len(self.getLeadTable().getPrimaryAtoms())
        row = area.provideRowInstance(atomicRow[:pklen],
                                                knownValues=d,
                                                new=False)
        
        # todo : `fillMode` to indicate that known atoms are expected to
        # match if row was in cache

        
        
        return row



##     def commit(self):
##         self.leadTable.commit()


    def values2id(self,knownValues):
        raise "used?"
        "convert dict of knownValues to sequence of pk atoms"
        #print knownValues
        #pka = self.leadTable.getPrimaryAtoms()
        #id = [None] * len(pka)
        
        id = [None] * len(self.getLeadTable().getPrimaryAtoms()) # _pkaLen
        #print self.name, knownValues
        for col in self._pkColumns:
            col.dict2atoms(knownValues,id)
        return id
    
    #def atoms2row1(self,atomicRow,row):
    def atoms2row(self,atomicRow,row):
        #for join in self._joins:
        #   join.atoms2row(atomicRow,row)
        for col in self._columns:
            col.col_atoms2row(atomicRow,row)
            



    def getDatabase(self):
        return self._store._db

    def getLeadTable(self):
        return self._store._table
    
    def getTableName(self):
        return self._store._table.getTableName()
    
    def getView(self,name):
        return self._store._table.getView(name)

    def setupMenu(self,frm):
        self._store._table.setupMenu(frm)

    def mtime(self):
        return self._store.mtime()
    

    def executePeek(self,id):
        return self._store.executePeek(self, id)

##     def unlock(self):
##         self._store.unlockQuery(self)
        
##     def unlock(self):
##         return self._store.unlockQuery(self)

    
    def createRow(self,*args,**kw):
        return self._store._table._instanceClass(
            self.getContext(),self._store,*args,**kw)

    #def atoms2row(self,atomicRow,new):
    def appendRowFromAtoms(self,atomicRow):
        #row = self.getLeadTable()._instanceClass(self,{},new)
        row = self._appendRow()
        self.atoms2row(atomicRow,row)
        row.unlock()
        return row
    
    
    def appendRow(self,*args,**kw):
        row = self._appendRow(*args,**kw)
        self.updateRow(row,*args,**kw)
        row.unlock()
        #self._store.fireUpdate()
        return row

    def appendRowForEditing(self,*args,**kw):
        row = self._appendRow(*args,**kw)
        self.updateRow(row,*args,**kw)
        return row
        
        
    def _appendRow(self,*args,**kw):
        row = self.createRow({},True)
        #row = self.getLeadTable().Instance(self,{},True)
        for mc in self._masterColumns:
            mc.setCellValue(row,self._masters[mc.name])
        self.rowcount = None
        #self._store.setAutoRowId(row)
        return row
        
    def updateRow(self,row,*args,**kw):
        i = 0
        for col in self.visibleColumns:
            if i == len(args):
                break
            col.setCellValue(row,args[i])
            i += 1
            
        for k,v in kw.items():
            col = self.getColumnByName(k)
            col.setCellValue(row,v)

        #row.setDirty() # statt row.setDirty() muessen die 


    def parse(self,s):
        strings = s.split(',')
        i=0
        rowid=[]
        for col in self._pkColumns:
            rowid.append(col.parse(strings[i]))
            i+=1
        return self.peek(*rowid)
    
##         pka=self.getLeadTable().getPrimaryAtoms()
##         atomicValues=[]
##         for name,type in pka:
##             atomicValues.append(type.parse(strings[i]))
##             i+=1
##         return self.atoms2value(atomicValues,self.getContext())
        
##         id = [None] * len(pka)
##         for col in self._pkColumns:
##             col.dict2atoms(knownValues,id)
##         return id
        
##         l1 = s.split(',')
##         assert len(l1) == len(self._pkaLen)
##         atomicValues = [a.type.parse(s1)
##                         for a,s1 in zip(self._atoms,l1)]
##         return self.atoms2value(atomicValues,qry.getContext())


    
    
class PeekQuery(LeadTableColumnList):
    def __init__(self,store):
        LeadTableColumnList.__init__(self,None,store,"*")
        self._frozen=True
        #print self.getLeadTable().getTableName(),\
        #      ','.join([col.name for col in self._columns])
        #for col in self._columns:
        #    self._columnsByName[col.name]=col


    #def getContext(self):
    #    return self._store._db

    def getContext(self):
        return self._store._db._startupContext

##     def getSession(self):
##         return self._store._db.getSession()

    def child(self,*args,**kw):
        raise InvalidRequestError("Cannot child() a PeekQuery!")
        







class SimpleQuery(LeadTableColumnList):

##     columnClasses=(PointerColumn,
##                    DetailColumn,
##                    BabelFieldColumn,
##                    FieldColumn
##                    )

    def __init__(self, _parent, _store, _dbc,
                 columnNames=None,
                 orderBy=None,
                 sortColumns=None,
                 sqlFilters=None,
                 filters=None,
                 search=None,
                 searchColumns=None,
                 masterColumns=None,
                 masters=[],
                 **kw):
        self.dbc = _dbc # a DbContext, not a session
        LeadTableColumnList.__init__(self,_parent,_store,columnNames)
        
        for m in ('setBabelLangs','getLangs'):
            setattr(self,m,getattr(_dbc,m))
        
        #self.app = store._db.schema # shortcut
        self._connection = _store._connection # shortcut

        for m in ('startDump','stopDump'):
            setattr(self,m,getattr(_store,m))
        self.rowcount = None
        
##         if label is not None:
##             assert type(label) == type(""),\
##                    "%s not a string" % repr(label)
##         self._label = label
            
        if orderBy is not None:
            assert sortColumns is None
            self.setOrderBy(orderBy)
        else:
            if sortColumns is None:
                if _parent is not None:
                    sortColumns=_parent.sortColumns
                else:
                    sortColumns=tuple()
            self.sortColumns=sortColumns
            #self.setSortColumns(sortColumns)
            
        
        if _parent is None:
            #self._samples = {}
            self._masterColumns=[]
            self._masters={}
        else:
            #self._samples = dict(parent._samples)
            self._masterColumns=list(_parent._masterColumns)
            self._masters=dict(_parent._masters)
            if search is None:
                search=_parent._search
            if filters is None:
                if _parent._filters is not None:
                    filters=list(_parent._filters)

        if searchColumns is not None:
            self.setSearchColumns(searchColumns)
            
        self._filters=filters
        self.setFilterExpressions(sqlFilters,search)
        
        if masterColumns is not None:
            self.setMasterColumns(masterColumns)
            
        self.setMasters(*masters,**kw)

##         if self.getTableName() == "Quotes":
##             print "created", self
        
##         if samples is None:
##             self.setSamples(**kw)
##         else:
##             #assert len(kw) == 0, "kw is %s, but samples is %s" % (\
##             #   repr(kw),repr(samples))
##             #self._samples.update(samples)
##             self.setSamples(samples)
##             self.setSamples(**kw)

            
##     def getContext(self):
##         #return self._clist._context
##         return self._session

    def setMasterColumns(self,columnNames):
        self._masterColumns = [
            self.provideColumn(name)
            for name in columnNames.split()]

    def getMaster(self,name):
        return self._masters[name]

    def canSort(self):
        return True

            
    def setMasters(self,*masters,**kw):
        #self._masters={}
        if len(masters):
            # masterColumns have been set previously
            assert len(kw) == 0
            assert len(self._masterColumns) == len(masters),\
                   str([c.name for c in self._masterColumns])\
                   + " != " + str(masters)
            i=0
            for mc in self._masterColumns:
                self._masters[mc.name]=masters[i]
                i+=1
            return
        if len(kw) == 0: return
        if len(self._masterColumns) == 0:
            for name,master in kw.items():
                self._masterColumns.append(self.provideColumn(name))
                self._masters[name]=master
        else:
            l=[col.name for col in self._masterColumns]
            for name,master in kw.items():
                if not name in l:
                    self._masterColumns.append(self.findColumn(name))
                #l=[col.name for col in self._masterColumns]
                #assert name in l, \
                #       "%s not in %s" % (name,l)
                self._masters[name]=master


##             col=self.provideColumn(name)
##             for ms in self._masters:
##                 if ms[MS_COLUMN] == col:
##                     ms[MS_MASTER]=master
##                     return
##             self._masters.append( (col,master) ) # MS_COLUMN, MS_MASTER
            


    def __repr__(self):
        s=self.__class__.__name__+\
               "(%s,columnNames='%s'" % (\
               self.getLeadTable().getTableName(),\
               " ".join([col.name for col in self._columns]))
        if len(self._masters) > 0:
            s += ", masters="+repr(self._masters)
        return s+')'

##     def getContext(self):
##         return self.session

    def show(self,**kw):
        from lino.adamo.dbreports import QueryReport
        QueryReport(self,**kw).show()

##     def showReport(self,**kw):
##         self.session.showQuery(self,**kw)

    def report(self,*args,**kw):
        rpt=self.dbc.createDataReport(self,*args,**kw)
        #rpt.beginReport(None)
        return rpt
        

    def zap(self):
        self._store.zap()

    def clearFilters(self):
        self._filters=None
        
    def addColFilter(self,colName,fcl,*args,**kw):
        col=self.provideColumn(colName)
        #col=self.getColumnByName(colName)
        self.addFilter(fcl(col,*args,**kw))
        
    def addFilter(self,flt): # cls,*args,**kw):
        #flt=cls(self,*args,**kw)
        if self._filters is None:
            self._filters=[]
        self._filters.append(flt)
        self.rowcount=None

    def deleteAll(self):
        
        """cannot use self._connection.executeDeleteAll(self) here
        because volume.directories.deleteAll() did not delete the
        files in each directory."""
        
        for row in self:
            row.delete()
            

    def child(self,*args,**kw):
        #self.setdefaults(kw)
        return self.__class__(self,self._store,self.dbc,*args,**kw)
    
    # alias for child() of a Query:
    query=child




##     def getRenderer(self,rsc,req,writer=None):
##         return self.app._datasourceRenderer(rsc,req,
##                                             self.query(),
##                                             writer)
    
##     def getSession(self):
##         return self.session

    def getContext(self):
        return self.dbc

    def getLabel(self):
        raise "replaced by buildLabel"
##         if self._label is None:
##             lbl = self.getLeadTable().getLabel()
##             if len(self._masterColumns) > 0:
##                 lbl += " ("
##                 for mc in self._masterColumns:
##                     v=self._masters[mc.name]
##                     lbl += mc.name + "=" \
##                            + mc.rowAttr.format(v)
##                 lbl += ")"
##             if self._filters is not None:
##                 lbl += " where "
##                 lbl += " and ".join(
##                     [f.getLabel() for f in self._filters])
##             return lbl
##         if callable(self._label):
##             raise "not yet tested"
##             return self._label(self)
##         return self._label
    
    def buildTitle(self):
        lbl = self.getLeadTable().getLabel()
        if len(self._masterColumns) > 0:
            lbl += " ("
            sep=""
            for mc in self._masterColumns:
                lbl+=sep
                sep=","
                v=self._masters[mc.name]
                if v is None:
                    lbl += mc.name + "=None"
                else:
                    lbl += mc.name + "=" + mc.rowAttr.format(v)
            lbl += ")"
        if self._filters is not None:
            lbl += " where "
            lbl += " and ".join(
                [f.getLabel() for f in self._filters])
        return lbl
            

    def setOrderBy(self,orderBy):
        #assert type(orderBy) is type('')
        #self._orderBy = orderBy
        l = []
        if orderBy is not None:
            for colName in orderBy.split():
                l.append(self.provideColumn(colName))
        self.sortColumns = tuple(l)

##     def setSortColumns(self,sortColumns):
##         if sortColumns is None:
##             self.sortColumns=[]
##         else:
##             #self._orderBy=" ".join([col.name
##             #                        for col in sortColumns])
##             self.sortColumns=sortColumns

            
    def setSqlFilters(self,*sqlFilters):
        self.setFilterExpressions(sqlFilters,self._search)
        
    def setSearch(self,search):
        self.setFilterExpressions(self._sqlFilters,search)
        
    def getAttrList(self):
        return self.getLeadTable().getAttrList()
    
    def setFilterExpressions(self, sqlFilters, search):
        """
        sqlFilters must be a sequence of strings containing SQL expressions
        """
        self._sqlFilters = sqlFilters
        self._search = search
        
        l = []
        if self._sqlFilters is not None:
            assert issequence(self._sqlFilters), repr(self._sqlFilters)
            for expr in self._sqlFilters:
                assert type(expr) in (str, unicode),\
                       "Expected list of strings, got "+\
                       repr(self._sqlFilters)
                l.append(expr)
        #self.filterExp = tuple(l)

        if self._search is not None:
            if not issequence(self._search):
                self._search = (self._search,)
            # search is a tuple of strings to search for
            atoms = self.getSearchAtoms()
            assert len(atoms) > 0
            for expr in self._search:
                l.append(" OR ".join(
                    [a.name+" LIKE '%"+expr+"%'" for a in atoms]))
                
        self.filterExpressions = tuple(l)
        
    def setSearchColumns(self,columnNames):
        l = []
        for colName in columnNames.split():
            col=self.provideColumn(colName)
            l += col.getAtoms()
        assert len(l) > 0
        self._searchAtoms=tuple(l)
        
    def getSearchAtoms(self):
        if self._searchAtoms is None:
            l = []
            for col in self._columns: # visibleColumns:
                if hasattr(col.rowAttr,'type'):
                    if isinstance(col.rowAttr.type,
                                  datatypes.StringType):
                        l += col.getAtoms()
            self._searchAtoms=tuple(l)
        return self._searchAtoms
        
    


    def getName(self):
        return self.getLeadTable().getTableName()+"Query"


    def appendfrom(self,filename,encoding=None):
        if encoding is None:
            encoding="cp1252"
        f=codecs.open(filename,encoding=encoding)
        atomicNames=f.readline().strip().split('\t')
        atoms=[]
        for name in atomicNames:
            a=self.findAtom(None,name)
            
            #if a is None:
            #    print "Note: no atom '%s' in %s" % (name,self)
            
            # note: if findAtom returns None we simply ignore values
            # in this column
            
            atoms.append(a)
        #self.setBabelLangs()
        for ln in f:
            
            row = self._appendRow()
            atomicRow=self.row2atoms(row)
            i=0
            #d={}
            for s in ln.split('\t'):
                a=atoms[i]
                i+=1
                if a is not None:
                    s=s.strip()
                    if s == '':
                        atomicRow[a.index]=None
                    else:
                        atomicRow[a.index]=a.type.parse(s)
            self.atoms2row(atomicRow,row)
            row.unlock()
            #if filename.endswith("cities_de.txt"):
            #    print atomicRow
            
    


    def __getitem__(self,offset):
        row = self.getRowAt(offset)
        if row is None:
            msg = "%s[%d] (%d) rows" % (
                self.getLeadTable().getTableName(),
                offset,len(self))
            raise IndexError,msg
        
        return row
    
    def getRowAt(self,offset):
        assert type(offset) is types.IntType
        if offset < 0:
            offset += len(self) 
        csr = self.executeSelect(offset=offset,limit=1)
        if FETCHONE:
            sqlatoms=csr.fetchone()
            if sqlatoms is None:
                csr.close()
                return None

            assert csr.fetchone() is None, \
                   "Query.getRowAt() got more than one row"
            csr.close()
        else:
            if not csr.first():
                return None
            sqlatoms=[csr.value(i) for i in range(len(self._atoms))]
            assert not csr.next(), \
                   "Query.getRowAt() got more than one row"
        atomicRow = self.csr2atoms(sqlatoms)
        row = self.createRow({},False)
        self.atoms2row(atomicRow,row)
        return row
        #return self.atoms2row(atomicRow,False)



    def csr2atoms(self,sqlatoms):
        return self._store.csr2atoms(self,sqlatoms)
    
        

##  def find(self,**knownValues):
##      atomicRow = self._clist.makeAtomicRow()
##      flt = []
##      atoms = []
##      for k,v in knownValues.items():
##          col = self._clist.getColumn(k)
##          col.value2atoms(v,atomicRow,self._context)
##          atoms += col.getFltAtoms(self._context)
##      for a in atoms: 
##          flt.append(self._connection.testEqual(a.name,
##                                                            a.type,
##                                                            atomicRow[a.index]))
##      ds = self.query(sqlFilters=(' AND '.join(flt),))
##      return ds

        
    def filter(self,*args,**knownValues):
        #raise QueryColumn._owner muss weg
        flt = []
        i = 0
        for arg in args:
            col = self.visibleColumns[i]
            flt.append(col.getTestEqual(self,arg))
            i+=1
##         for k,v in knownValues.items():
##             col = self.getColumnByName(k)
##             flt.append(col.getTestEqual(self,v))
##         if len(flt):
##             return self.child(sqlFilters=(' AND '.join(flt),))
        
        if len(flt):
            return self.child(
                sqlFilters=' AND '.join(flt),**knownValues)
        if len(knownValues): return self.child(**knownValues)
        return self
        
    def findone(self,*args,**knownValues):
        
        qry = self.filter(*args,**knownValues)
        csr = qry.executeSelect()
        
        if FETCHONE:
            sqlatoms = csr.fetchone()
            if sqlatoms is None:
                csr.close()
                return None

            if csr.fetchone() is not None:
                print knownValues
                raise InvalidRequestError(
                    "findone() found more than one row in %s" % qry)

            csr.close()
        else:
            if not csr.first():
                return None
            sqlatoms=[csr.value(i) for i in range(len(self._atoms))]
            assert not csr.next(), \
                   "findone() got more than one row in %s" % qry
        
        atomicRow = self.csr2atoms(sqlatoms)
        row = self.createRow({},False)
        self.atoms2row(atomicRow,row)
        return row
        #return self.atoms2row(atomicRow,False)
    
        

    def getSqlSelect(self,**kw):
        return self._connection.getSqlSelect(self,**kw)
        #return self._clist.getSqlSelect(self._connection,**kw)

##  def setCsvSamples(self,**kw):
##      self._query.setCsvSamples(self._area,**kw)

    def rows(self,doc):
        return DataIterator(self)
        
    def __iter__(self):
        return DataIterator(self)
    
    def iterate(self,**kw):
        
        """ like __iter___() but possible to specify keyword
        parameters. E.g. offset and limit.
        
        """
        
        return DataIterator(self,**kw)

    def fetchall(self):
        #if FETCHONE:
        return [x for x in self]
        #raise NotImplementedError

    def onStoreUpdate(self):
        #print __file__,"onStoreUpdate()"
        self.rowcount = None
    
    def __len__(self):
        if self.rowcount is None:
            self.rowcount = self._store.executeCount(self)
        return self.rowcount
        
    def executeSelect(self,**kw):
        return self._store.executeSelect(self, **kw )




class Query(SimpleQuery):

    def __init__(self, _parent, _store, _dbc,
                 columnNames=None,
                 pageNum=None,
                 pageLen=None,
                 **kw):
        
        
        SimpleQuery.__init__(
            self, _parent,_store,_dbc,columnNames,**kw)
        if _parent is not None:
            if pageNum is None: pageNum=_parent.pageNum
            if pageLen is None: pageLen=_parent.pageLen
            
        self.pageNum = pageNum
        self.pageLen = pageLen
        if self.pageLen is None:
            self.lastPage = 1
        elif len(self) == 0:
            self.lastPage = 1
        else:
            self.lastPage = int((len(self)-1) / self.pageLen) + 1
            """
            if pageLen is 10:
            - [0..10] rows --> 1 page
            - [11..20] rows --> 2 pages
            - [21..30] rows --> 2 pages
            - 10 rows --> 1 page
            - 11 rows --> 2 pages
            """

        """note: pageNum can be None even if pageLen isn't.  This will
        default to either 1 *or* lastPage if reverse.
        (but reverse not yet implemented)
        """


        if self.pageLen is None:
            self.startOffset=0
            self.pageNum=1
        else:
            if self.pageNum is None:
                self.pageNum=1
            elif self.pageNum < 0:
                self.pageNum = self.lastPage + self.pageNum - 1
            elif self.pageNum > self.lastPage:
                raise InvalidRequestError(\
                    "pageNum=%d > lastPage=%d" % (self.pageNum,
                                                  self.lastPage))
            self.startOffset = self.pageLen * (self.pageNum-1)
        
        
        
    def apply_GET(self,**kw):
        #rptParams = {}
        #dsParams = {}
        p = {}
        for k,v in kw.items():
            if k == 'pg':
                p['pageNum'] = str(v[0])
            elif k == 'pl':
                p['pageLen'] = str(v[0])
            else:
                p[k] = v
        SimpleQuery.apply_GET(self,**p)
        #self.config(**rptParams)
        
    def get_GET(self):
        p = SimpleQuery.get_GET(self)
        if self.pageNum != None:
            p['pg'] = self.pageNum
        if self.pageLen != None:
            p['pl'] = self.pageLen
        return p
        

    def setdefaults(self,kw):
        kw.setdefault('pageNum',self.pageNum)
        kw.setdefault('pageLen',self.pageLen)
        SimpleQuery.setdefaults(self,kw)

    def executeSelect(self,
                      limit=None,
                      offset=None,**kw):
        # overrides SimpleQuery.executeSelect()
        """
        modify limit and offset to contain self.pageNum and self.pageLen
        
        """
        if offset is None:
            offset = self.startOffset
        else:
            offset += self.startOffset
        if limit is None:
            limit = self.pageLen
        
        return self._store.executeSelect(self,
                                         limit=limit,
                                         offset=offset,
                                         **kw )

    









class Atom:
    """
    An Atom represents one SQL column
    """
    def __init__(self,joinName,name,atype,index):
        self.joinName = joinName
        assert (joinName is None) or type(joinName) in (str, unicode) 
        self.type = atype
        self.index = index
        self.name = name
        

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
##      return "Atom(%s,%s,%d)" % (#repr(self.join),
##                                          self.name,
##                                          self.type,
##                                          self.index)

        return "<atom %d:%s>" % (self.index,self.name)




        
class Join:
    
    def __init__(self,owner,name,pointer,parent=None):
        self.name = name
        self._owner = owner
        self.parent = parent
        self.pointer = pointer
        self._joinedTables = []
        self._atoms = None
        if is_reserved(name):
            self._sqlName = "x"+name
        else:
            self._sqlName = name
        
        """self._atoms is a list of (a,b) couples where a and b are
        atoms used for the join.  """

        
    def setupJoinAtoms(self):
        assert self._atoms is None
        self._atoms = []
        shortJoinName = self.name.split("_")[-1]
        if self.parent is None:
            parentJoinName = None
        else:
            parentJoinName = self.parent._sqlName
            
        if len(self.pointer._toTables) == 1:
            for (name,type) in self.pointer._toTables[0].getPrimaryAtoms():
                a = self._owner.provideAtom(shortJoinName+"_"+name,
                                            type,
                                            parentJoinName)
                b = self._owner.provideAtom(name,
                                            type,
                                            self._sqlName)
                self._atoms.append((a,b))
        else:
            for toTable in self.pointer._toTables:
                for (name,type) in toTable.getPrimaryAtoms():
                    a = self._owner.provideAtom(
                        shortJoinName+toTable.getTableName()+"_"+name,
                        type,
                        parentJoinName)
                    b = self._owner.provideAtom(
                        name,
                        type,
                        self._sqlName+toTable.getTableName())
                    self._atoms.append((a,b))

    def getJoinAtoms(self):
        return self._atoms


    def __repr__(self):
        return "Join(%s,%s)" % (self.name,repr(self.parent))













## def trigger(events,*args):
##     for e in events:
##         if not e(*args): return False
##     return True


from traceback import print_stack
from cStringIO import StringIO

def calledfrom():
    f=StringIO()
    print_stack(limit=4,file=f)
    lines=f.getvalue().splitlines()
    return ":".join(lines[:2])
            

class DataIterator:

    def __init__(self,ds,**kw):
        self.ds = ds
        self.csr = ds.executeSelect(**kw)
        self.recno = 0
        self.ds._store.addIterator(self)
        self._calledfrom = calledfrom()
        
        
    def __repr__(self):
        return 'Iterator on row %d in "%s" (called from %s)' % (
            self.recno,self.ds.getSqlSelect(),self._calledfrom)
    def __iter__(self):
        return self

    def close(self):
        self.ds._store.removeIterator(self)
        if FETCHONE:
            self.csr.close()
        
    
    def next(self):
        if FETCHONE:
            sqlatoms = self.csr.fetchone()
            if sqlatoms == None:
                self.close()
                raise StopIteration

        else:
            if not self.csr.next():
                self.close()
                raise StopIteration
            sqlatoms=[self.csr.value(i) for i in range(len(self.ds._atoms))]
            #sqlatoms=[self.csr.value(a.index) for a in self.ds._atoms]
        
        atomicRow = self.ds.csr2atoms(sqlatoms)
        #row=self.ds.atoms2row(atomicRow,False)
        row = self.ds.createRow({},False)
        self.ds.atoms2row(atomicRow,row)
        row.validate()
        self.recno += 1
        return row










