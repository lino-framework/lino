## Copyright 2003-2005 Luc Saffre

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

from lino.adamo.exceptions import DataVeto, \
     NoSuchField, InvalidRequestError

from lino.misc.compat import *
from lino.misc.etc import issequence

from lino.adamo import datatypes

from lino.adamo.rowattrs import Detail, Pointer, Field, BabelField

#MS_COLUMN=1
#MS_MASTER=1


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

class QueryColumn:
    
    def __init__(self,owner,index,name,rowAttr,
                 join=None,atoms=None):
        self._owner = owner
        self.index = index
        self.name = name
        self.rowAttr = rowAttr
        self.join = join
        #self.sticky = False
        #self.isVisible = isVisible
        #self.width = rowAttr.width
        
        self._atoms = atoms

        # self._atoms is list of those atoms in ColumnList which have
        # been requested by this column


    def __str__(self):
        return self.name

    def __repr__(self):
        return "<column %d:%s in %s>" % (self.index,self.name,
                                         repr(self._owner))
    def canWrite(self,row):
        return self.rowAttr.canWrite(row)

    def getValueClass(self):
        raise NotImplementedError
    

    def setupColAtoms(self,db):
        #assert self._atoms is None
        atoms = []
        if self.join:
            joinName = self.join.name
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

    def vetoDeleteRow(self,row):
        pass

    def addFilter(self,fcl,*args,**kw):
        flt=fcl(self,*args,**kw)
        self._owner.addFilter(flt)


    def setCellValue(self,row,value):
        #self.rowAttr.canSetValue(row,value)
        try:
            self.rowAttr.setCellValue(row,value)
        except DataVeto,e:
            raise DataVeto(repr(value)+": "+str(e))
        self.rowAttr.afterSetAttr(row)

    def setCellValueFromString(self,row,s):
        self.rowAttr.setCellValueFromString(row,s)
        self.rowAttr.afterSetAttr(row)
        
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
        # overridden by BabelField and Detail
        return row.getFieldValue(self.rowAttr.name)


    def atoms2row(self,atomicRow,row):
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

    def atoms2value(self,atomicValues,sess):
        #return self.rowAttr.atoms2value(atomicRow,self._atoms,area)
        #atomicValues = [atomicRow[atom.index]
        #                    for atom in self._atoms]
        return self.rowAttr.atoms2value(atomicValues,sess)
    

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

    def parse(self,s,ds):
        l1 = s.split(',')
        assert len(l1) == len(self._atoms)
        atomicValues = [a.type.parse(s1)
                             for a,s1 in zip(self._atoms,l1)]
        return self.atoms2value(atomicValues,ds._session)
        
    def format(self,v):
        return self.rowAttr.format(v)
        
    def showSelector(self,frm,row):
        return False


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
        values = [None] * len(dblangs)
        if value is not None:
            assert issequence(value), \
                   "%s is not a sequence" % repr(value)
            assert len(value) == len(dblangs), \
                   "Expected %d values but got %s" % \
                   (len(dblangs), repr(value))
            i = 0
            for lang in dblangs:
                values[lang.index] = value[i]
                i += 1
        return values
        
        
    def row2atoms(self,row,atomicRow):
        value = row._values.get(self.rowAttr.name)
        self.values2atoms(
            self.atomize(value,row.getDatabase()),
            atomicRow)


    def extractCellValue(self,row):
        langs = row.getSession().getBabelLangs()
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
                   "Session language %r not supported by %s" \
                   % (langs[0].id,row.getDatabase().getSupportedLangs())
            #print __name__, values[index], langs
            return values[langs[0].index]
        
    def getTestEqual(self,ds,value):
        langs = ds.getSession().getBabelLangs()
        lang = langs[0] # ignore secondary languages
        a = self._atoms[lang.index]
        return ds._connection.testEqual(a.name,a.type,value)
        
        
        
class PointerColumn(QueryColumn):
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
        tableId = value._query.getLeadTable().getTableId()
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
        self.value2atoms(value,av,ds.getSession())
        i = 0
        l = []
        for (n,t) in self.rowAttr.getNeededAtoms(ds.getSession()):
            l.append(ds._connection.testEqual(n,t,av[i]))
            i += 1
        return " AND ".join(l)

    def showSelector(self,frm,row):
        sess=frm.session
        row.lock()
        ds = self.rowAttr.getTargetSource(row)
        selectedRow = sess.chooseDataRow(ds,row)
        if selectedRow is not None:
            sess.notice("you selected: "+str(row))
            self.setCellValue(row,selectedRow)
            row.setDirty()
        row.unlock()
        return True

    def getReachableData(self,row):
        pointedRow = self.getCellValue(row)
        if pointedRow is None:
            return 
        #d = { self.rowAttr.name : pointedRow }
        #return pointedRow._query.child(**d)
        
    def getValueClass(self):
        return self.rowAttr.type # _toClass
    
        
        
class DetailColumn(QueryColumn):
    fieldClass=Detail
    def __init__(self,owner,index,name,rowAttr,
                 join=None,atoms=None,depth=0,**kw):
        QueryColumn.__init__(self,owner,index,name,rowAttr,join,atoms)
        for k,v in self.rowAttr._queryParams.items():
            kw.setdefault(k,v)
        self._queryParams=kw
        self.detailQuery=None
        self.depth=depth

    def prepare(self):
        # lazy instanciation for self.detailQuery 
        if self.detailQuery is None:
            self.detailQuery=self._owner.getSession().query(
                self.rowAttr.pointer._owner.__class__,
                **self._queryParams)
            #print "DetailColumn created ", self.detailQuery,\
            #      self.detailQuery._search
        

    def extractCellValue(self,row,**kw):
        self.prepare()
        kw[self.rowAttr.pointer.name]=row
        return self.detailQuery.child(**kw)
        #return self.detailQuery.child(masters=(row,))

    def getDetailQuery(self):
        self.prepare()
        return self.detailQuery


    def vetoDeleteRow(self,row):
        detailDs = self.getCellValue(row)
        if len(detailDs) == 0:
            return 
        #return "%s : %s not empty (contains %d rows)" % (
        #   str(row),self.name,len(ds))
        return "%s : %s not empty" % (str(row),self.name)
            
        

    def value2atoms(self,value,atomicRow,context):
        values = self.rowAttr.value2atoms(value,context)
        self.values2atoms(values,atomicRow)
        

    def row2atoms(self,row,atomicRow):
        pass

    def format(self,v):
        if self.depth == 0:
            return str(len(v))+" "+v.getLeadTable().getName()
        return ", ".join([r.__str__() for r in v])



    def showSelector(self,frm,row):
        ds = self.getCellValue(row)
        ds.showReport()
        #frm.session.showDataGrid(ds)
        return True


    def getValueClass(self):
        return Query
        #self.prepare()
        #return self.detailQuery
    






class Calendar:
    def __init__(self,session,columnNames,
                 year=None,
                 month=None,
                 week=None):
        self._session=session
        self._columns = []
        if columnNames is None:
            self.visibleColumns=[]
        else:
            self.setVisibleColumns(columnNames)

    def getContext(self):
        return self._session
    
    def getDatabase(self):
        return self._session.db


class BaseColumnList(Datasource): 
    
    #ANY_VALUE = types.NoneType
    
    columnClasses=( PointerColumn,
                    BabelFieldColumn,
                    FieldColumn,
                    )
    
    
    def __init__(self,_parent,columnNames):
        if _parent is not None and columnNames is None:
            if _parent.getContext() == self.getContext():
                self._frozen=True
                self._columns = tuple(_parent._columns)
                self._joins = tuple(_parent._joins)
                self._atoms = tuple(_parent._atoms)
                self._pkColumns = _parent._pkColumns
                self.visibleColumns=tuple(_parent.visibleColumns)
                if _parent._searchAtoms is None:
                    self._searchAtoms = None
                else:
                    self._searchAtoms = tuple(_parent._searchAtoms)
                return
        
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

                

    def getContext(self):
        # a context is either a session or a database
        raise NotImplementedError
    
    def getLeadTable(self):
        # the leadTable 
        raise NotImplementedError

    def setVisibleColumns(self,columnNames):
        assert type(columnNames) in (str,unicode) #is types.StringType
        l = []
        groups = []
        for ln in columnNames.splitlines():
            grp=[]
            for colName in columnNames.split():
                if colName == "*":
                    for fld in self.getLeadTable().getFields():
                        col = self.findColumn(fld.getName())
                        if col is None:
                            col = self._addColumn(fld.getName(),fld)
                        grp.append(col)
                else:
                    grp.append(self.provideColumn(colName))
            l += grp
            groups.append(grp)
        self.visibleColumns = tuple(l)
        self.formColumnGroups = tuple(groups)
            

    def getName(self):
        return self.name


##     def mustSetup(self):
##         return self._atoms is None

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
        col=self._addColumn(*args,**kw)
        self.visibleColumns= self.visibleColumns + (col,)
        return col
    
    def _addColumn(self,name,rowAttr=None,join=None,**kw):
        if self._frozen:
            raise InvalidRequestError(
                "Cannot append columns to frozen %r" % self)
        if rowAttr is None:
            rowAttr=self.getLeadTable().getRowAttr(name)
        #    visible=True
        #else:
        #    visible=False
        for ccl in self.columnClasses:
            if isinstance(rowAttr,ccl.fieldClass):
                col=ccl(self,len(self._columns),
                        name, rowAttr, join,**kw)
                self._columns.append(col)
                col.setupColAtoms(self.getDatabase())
                #if visible:
                #    self.visibleColumns.append(col)
                return col
##         print "%s ignores addColumn for %r" % (
##             self.__class__.__name__,
##             rowAttr)

            
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

##     def getColumn(self,i):
##         return self.visibleColumns[i]
    
    def getColumnByName(self,name):
        col = self.findColumn(name)
        if col is None:
            msg = "No column '%s' in %s (%s)" % (
                name,
                self.getLeadTable().getTableName(),
                ', '.join([col.name for col in self._columns]))
            raise DataVeto(msg)
        return col


    def getAtoms(self):
        return self._atoms
    

    def provideAtom(self,name,type,joinName=None):
        
        """Return the atom with specified name if already present.  type
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
        j.setupJoinAtoms()
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



    def canWrite(self):
        return True
    
    def updateRow(self,row,*args,**kw):
        i = 0
        for col in self.visibleColumns:
            if i == len(args):
                break
            col.setCellValue(row,args[i])
            #row._values[col.rowAttr._name] = args[i]
            i += 1
            
        for k,v in kw.items():
            col = self.getColumnByName(k)
            col.setCellValue(row,v)

        row.setDirty()
            
    


    def atoms2dict(self,atomicRow,rowValues,area):
        for col in self._columns:
            if col.join is None:
                col.atoms2dict(atomicRow,rowValues,area)
            

    def ad2t(self,d):
        "atomic dict to tuple"
        atomicTuple = [None] * len(self._atoms)
        for k,v in d.items():
            a = self.getAtom(k)
            atomicTuple[a.index] = v
        return atomicTuple
    

    def makeAtomicRow(self,context=None,*args,**kw):
        atomicRow = [None] * len(self._atoms) 
        i = 0
        for col in self.visibleColumns:
            if i == len(args):
                break
            col.value2atoms(args[i],atomicRow,context)
            i += 1
            
        for k,v in kw.items():
            col = self.getColumnByName(k)
            col.value2atoms(v,atomicRow,context)
        return atomicRow

        
    def row2atoms(self,row,atomicRow=None):
        if atomicRow is None:
            atomicRow = [None] * len(self._atoms) # _pkaLen
        for col in self._columns:
            col.row2atoms(row,atomicRow)
        return atomicRow





class LeadTableColumnList(BaseColumnList):
    
    def __init__(self,_parent,store,columnNames):

        assert store.__class__.__name__ == "Store", \
               store.__class__.__name__+" is not a Store"
        self._store=store
        BaseColumnList.__init__(self,_parent,columnNames)

        #self.leadTable = store._table 
        
        


##     def getFieldContainer(self):
##         return self._store._table # self.leadTable

    
    def atoms2instance(self,atomicRow,area):

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
        "convert dict of knownValues to sequence of pk atoms"
        #print knownValues
        #pka = self.leadTable.getPrimaryAtoms()
        #id = [None] * len(pka)
        
        id = [None] * len(self.getLeadTable().getPrimaryAtoms()) # _pkaLen
        #print self.name, knownValues
        for col in self._pkColumns:
            col.dict2atoms(knownValues,id)
        return id


    def getDatabase(self):
        return self._store._db

    def getLeadTable(self):
        return self._store._table
    
    def getView(self,name):
        return self._store._table.getView(name)

    def setupMenu(self,navigator):
        self._store._table.setupMenu(navigator)

    def mtime(self):
        return self._store.mtime()
    
    def atoms2row(self,atomicRow,new):
        row = self.getLeadTable().Instance(self,{},new)
        self.atoms2row1(atomicRow,row)
        return row
    
    def atoms2row1(self,atomicRow,row):
        #for join in self._joins:
        #   join.atoms2row(atomicRow,row)
        for col in self._columns:
            col.atoms2row(atomicRow,row)
            

    

    
class PeekQuery(LeadTableColumnList):
    def __init__(self,store):
        LeadTableColumnList.__init__(self,None,store,"*")
        assert len(self._columns) > 1

    def getContext(self):
        return self._store._db

    def getSession(self):
        return self._store._db._startupSession
        







class SimpleQuery(LeadTableColumnList):

    columnClasses=( PointerColumn,
                    DetailColumn,
                    BabelFieldColumn,
                    FieldColumn,
                    )
##     columnClasses={ Detail: DetailColumn,
##                     Pointer: PointerColumn,
##                     Field: FieldColumn,
##                     }
    def __init__(self, _parent, store, sess,
                 columnNames=None,
                 #viewName=None,
                 orderBy=None,
                 sortColumns=None,
                 sqlFilters=None,
                 filters=None,
                 search=None,
                 masterColumns=None,
                 masters=[],
                 label=None,
                 **kw):
        self.session = sess
        LeadTableColumnList.__init__(self,_parent,store,columnNames)
        self.rowcount = None
        
        for m in ('setBabelLangs','getLangs'):
            setattr(self,m,getattr(sess,m))
        

        #self._table = store._table # shortcut
        self.app = store._db.app # shortcut
        self._connection = store._connection # shortcut

        for m in ('startDump','stopDump'):
            setattr(self,m,getattr(store,m))
        self.rowcount = None

        
        
        #print "Datasource.configure()", self
        
        #self._viewName = viewName
        if label is not None:
            assert type(label) == type(""),\
                   "%s not a string" % repr(label)
        self._label = label
            
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
            
##     def setSamples(self,**kw):
##         "each value is a Python object"
##         self._samples.update(kw)
##         for (name,value) in self._samples.items():
##             if value == self.ANY_VALUE:
##                 del self._samples[name]
##             else:
##                 col = self.provideColumn(name)
    
    
##     def getAtomicSamples(self):
##         l = []
##         atomicRow = self.makeAtomicRow() 
##         for (name,value) in self._samples.items():
##             col = self.getColumnByName(name)
##             col.value2atoms(value,atomicRow,self.getDatabase())
##             # 20050110
##             # col.value2atoms(value,atomicRow,self.getContext())
##             for atom in col.getAtoms():
##                 l.append((atom,atomicRow[atom.index]))
##         return l


    def __repr__(self):
        return self.__class__.__name__+\
               "(%s,'%s',masterColumns='%s')" % (\
               self.getLeadTable().getTableName(),\
               " ".join([col.name for col in self._columns]),
               " ".join([col.name for col in self._masterColumns]),
               )

    def getContext(self):
        return self.session

    def createReport(self,name=None,**kw):
        raise "moved to dbsession"
    
    def showReport(self,**kw):
        self.session.showQuery(self,**kw)

    def zap(self):
        self._store.zap()

    def clearFilters(self):
        self._filters=None
        
    def addFilter(self,flt): # cls,*args,**kw):
        #flt=cls(self,*args,**kw)
        if self._filters is None:
            self._filters=[]
        self._filters.append(flt)
        self.rowcount=None

    def deleteAll(self):
        for row in self:
            row.delete()
        # volume.directories.deleteAll() did not delete the files in each directory. 
        #self._connection.executeDeleteAll(self)
        #
        

##     def apply_GET(self,**kw):
##         """
##         apply a (Twisted) GET dict to self
##         """
##         qryParams = {}
##         #csvSamples = {}
##         for k,v in kw.items():
##             if k == 'ob':
##                 qryParams['orderBy'] = " ".join(v)
##             elif k == 'v':
##                 viewName = v[0]
##                 if viewName == '':
##                     viewName = None
##                 qryParams['viewName'] = viewName
##             elif k == 'search':
##                 qryParams['search'] = v[0]
##             elif k == 'flt':
##                 qryParams['sqlFilters'] = v
##                 #qryParams['sqlFilters'] = (v[0],)
##                 #qryParams['filters'] = tuple(l)

##             else:
##                 #csvSamples[k] = v[0]
##                 col = self.provideColumn(k)
##                 qryParams[k] = col.parse(v[0],self)
                
##         self.configure(**qryParams)
        #if len(csvSamples) > 0:
        #   self.setCsvSamples(**csvSamples)
            
##  def setCsvSamples(self,**kw):
##      "each value is a string to be parsed by column"
##      #self._samples.update(kw)
##      for (name,value) in kw.items():
##          if value == self.ANY_VALUE:
##              del self._samples[name]
##          else:
##              col = self._clist.provideColumn(name)
##              self._samples[name] = col.parse(value,self)
##      return

##     def get_GET(self):
##         p = {}
##         if self._orderBy != None:
##             p['ob'] = self._orderBy
##         if self._viewName != None:
##             p['v'] = self._viewName
##         if self._search != None:
##             p['search'] = self._search
##         if self._sqlFilters != None:
##             p['flt'] = self._sqlFilters
##         for (key,value) in self._samples.items():
##             col = self.getColumnByName(key)
##             p[key] = col.format(value,self)
##         return p
        
        
    def getColumn(self,i):
        return self.visibleColumns[i]
        
        
    def child(self,columnNames=None,**kw):
        #self.setdefaults(kw)
        return self.__class__(self,self._store,self.session,
                              columnNames=columnNames,
                              **kw)
    # alias for child() of a Query:
    query=child


    def __xml__(self,wr):
        wr("<datasource>")
        for row in self:
            wr("<row>")
            for col in self.getVisibleColumns():
                wr("<td>")
                v = v = col.getCellValue(row)
                if v is not None:
                    wr(col.format(v))
                wr("</td>")
            wr("</row>")
        wr("</datasource>")


        
    
##  def child(self,cl,**kw):
        
##      """creates a child (a detached copy) of this.  Modifying the
##      child won't affect the parent.  columnNames can optionally be
##      specified as first (non-keyword) argument.  if arguments are
##      given, then they override the corresponding value in the parent.
        
##      """
##      self.setdefaults(kw)
##      return cl( self._session,
##                    self._store,
##                    self._clist,
##                    **kw)

##     def setdefaults(self,kw):
##         if not kw.has_key('orderBy'):
##             kw.setdefault('sortColumns',self.sortColumns)
##         kw.setdefault('search',self._search)
##         if self._label is not None:
##             kw.setdefault('label',self._label)
##         if self._sqlFilters is not None:
##             kw.setdefault('sqlFilters',tuple(self._sqlFilters))
##         if self._filters is not None:
##             kw.setdefault('filters',list(self._filters))
##             #print self._filters
##         #if samples is None:
##         #kw.setdefault('samples',self._samples)
##         for k,v in self._samples.items():
##             kw.setdefault(k,v)
        


    def getRenderer(self,rsc,req,writer=None):
        return self.app._datasourceRenderer(rsc,req,
                                            self.query(),
                                            writer)
    
    def getSession(self):
        return self.session

    def getTableName(self):
        return self.getLeadTable().getTableName()
    
    def getLabel(self):
        if self._label is None:
            lbl = self.getLeadTable().getLabel()
            if len(self._masterColumns) > 0:
                lbl += " ("
                for mc in self._masterColumns:
                    v=self._masters[mc.name]
                    lbl += mc.name + "=" \
                           + mc.rowAttr.format(v)
                lbl += ")"
            if self._filters is not None:
                lbl += " where "
                lbl += " and ".join(
                    [f.getLabel() for f in self._filters])
            return lbl
        if callable(self._label):
            raise "not yet tested"
            return self._label(self)
        return self._label
            

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
        
    def getVisibleColumns(self):
        return self.visibleColumns
    
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
            for col in self.visibleColumns:
                if hasattr(col.rowAttr,'type'):
                    if isinstance(col.rowAttr.type,
                                  datatypes.StringType):
                        l += col.getAtoms()
            self._searchAtoms=tuple(l)
        return self._searchAtoms
        
    


##  def __str__(self,):
##      return self._table.__class__.__name__+"Datasource"


    def getName(self):
        return self.getLeadTable().getTableName()+"Query"

##  def getRowId(self,values):
##      return [values.get(name,None)
##                for (name,type) in self._table.getPrimaryAtoms()]

    def executePeek(self,id):
        return self._store.executePeek(self, id)

    def commit(self):
        self._store.unlockDatasource(self)
        
##     def commit(self):
##         for row in self._lockedRows:
##             row.writeToStore()
        
##     def close(self):
##         #print "close()", self
##         self.unlockAll()
##         assert len(self._lockedRows) == 0
##         self._store.removeDatasource(self)

##     def __del__(self):
##         if len(self._lockedRows):
##             print "%s had %d locked rows" % (
##                 str(self),
##                 len(self._lockedRows))
##         #self.close()

    def unlock(self):
        return self._store.unlockDatasource(self)
        
    def appendRow(self,*args,**kw):
        row = self._appendRow(*args,**kw)
        row.commit()
        self._store.fireUpdate()
        return row

    def appendRowForEditing(self,*args,**kw):
        return self._appendRow(*args,**kw)
        
        
    def _appendRow(self,*args,**kw):
        row = self.getLeadTable().Instance(self,{},True)
        for mc in self._masterColumns:
            #v = mc.getCellValue(self._masters[mc.name])
            #kw[mc.name] = v
            #kw[mc.name] = self._masters[mc.name]
            mc.setCellValue(row,self._masters[mc.name])
        #kw.update(self._samples)
        self.updateRow(row,*args,**kw)
        self.rowcount = None
        self._store.setAutoRowId(row)
        return row
        


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
            offset = len(self) + offset 
        csr = self.executeSelect(offset=offset,limit=1)
        sqlatoms=csr.fetchone()
        if sqlatoms is None:
            return None
        assert csr.fetchone() is None, \
               "Datasource.getRowAt() got more than one row"
        
        atomicRow = self.csr2atoms(sqlatoms)
        return self.atoms2row(atomicRow,False)

    def csr2atoms(self,sqlatoms):
        return self._store.csr2atoms(self,sqlatoms)
    
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
            
##         # atomize the id :
##         l = []
##         i = 0
##         for col in self._pkColumns:
##             l += col.rowAttr.value2atoms(id[i],self.getDatabase())
##             i+=1
            
        atomicRow = self.executePeek(l)
        if atomicRow is None:
            return None
        #d = self._clist.at2d(atomicRow)
        #return self._table.Row(self,d,False)
        return self.atoms2row(atomicRow,False)

    def getInstance(self,atomicId,new):
        row = self.getLeadTable().Instance(self,{},new)
        i = 0
        for col in self._pkColumns:
            col.atoms2row(atomicId,row)
            #col.setCellValue(row,atomicId[i])
            i+=1
        return row
            
        

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
        
    def find(self,*args,**knownValues):
        flt = []
        i = 0
        for arg in args:
            col = self.visibleColumns[i]
            flt.append(col.getTestEqual(self,arg))
            i+=1
        for k,v in knownValues.items():
            col = self.getColumnByName(k)
            flt.append(col.getTestEqual(self,v))
        ds = self.query(sqlFilters=(' AND '.join(flt),))
        return ds
        
    def findone(self,**knownValues):
        ds = self.find(**knownValues)
        #print [a.name for a in ds.query._atoms]
        #q = self._table.query(filters=' AND'.join(flt))
        #csr = self._connection.executeSelect(q)
        csr = ds.executeSelect()
        
        sqlatoms = csr.fetchone()
        if sqlatoms is None:
            return None

        assert csr.fetchone() is None, \
               "Datasource.findone() found more than one row"
               #"%s.findone(%r) found more than one row" % (
               #    self._table.getTableName(), knownValues)
        
        atomicRow = self.csr2atoms(sqlatoms)
        return self.atoms2row(atomicRow,False)
    

        

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

    def onStoreUpdate(self):
        print __file__,"onStoreUpdate()"
        self.rowcount = None
    
    def __len__(self):
        if self.rowcount is None:
            self.rowcount = self._store.executeCount(self)
        return self.rowcount
        
    def executeSelect(self,**kw):
        return self._store.executeSelect(self, **kw )




class Query(SimpleQuery):

    def __init__(self, _parent, store, sess,
                 columnNames=None,
                 pageNum=None,
                 pageLen=None,
                 **kw):
        
        
        SimpleQuery.__init__(
            self, _parent,store,sess,columnNames,**kw)
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
        #self.join = join
        self.type = atype
        self.index = index
        self.name = name
        self.joinName = joinName
        assert (joinName is None) or type(joinName) in (str, unicode) # is types.StringType
        

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
        
        """self._atoms is a list of (a,b) couples where a and b are
        atoms used for the join.  """

        
    def setupJoinAtoms(self):
        assert self._atoms is None
        self._atoms = []
        shortJoinName = self.name.split("_")[-1]
        if self.parent is None:
            parentJoinName = None
        else:
            parentJoinName = self.parent.name
            
        if len(self.pointer._toTables) == 1:
            for (name,type) in self.pointer._toTables[0].getPrimaryAtoms():
                a = self._owner.provideAtom( shortJoinName+"_"+name,
                                            type,
                                            parentJoinName)
                b = self._owner.provideAtom( name,
                                            type,
                                            self.name)
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
                        self.name+toTable.getTableName())
                    self._atoms.append((a,b))

    def getJoinAtoms(self):
        return self._atoms


    def __repr__(self):
        return "Join(%s,%s)" % (self.name,repr(self.parent))













def trigger(events,*args):
    for e in events:
        if not e(*args): return False
    return True


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
    
    def next(self):
        sqlatoms = self.csr.fetchone()
        if sqlatoms == None:
            self.ds._store.removeIterator(self)
            raise StopIteration
        atomicRow = self.ds.csr2atoms(sqlatoms)
        row=self.ds.atoms2row(atomicRow,new=False)
        self.recno += 1
        return row










