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

from lino.adamo.rowattrs import Detail, Pointer


class BaseColumnList: 
    
    def __init__(self,parent,columnNames):
        if parent is not None and columnNames is None:
            self._frozen=True
            self._columns = tuple(parent._columns)
            self._joins = tuple(parent._joins)
            self._atoms = tuple(parent._atoms)
            self._pkColumns = parent._pkColumns
            self.visibleColumns=tuple(parent.visibleColumns)
            return
        
        self._frozen=False
        self._columns = []
        self._joins = []
        self._atoms = []

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
        l = []
        assert type(columnNames) is types.StringType
        for colName in columnNames.split():
            if colName == "*":
                for fld in self.getLeadTable().getFields():
                    col = self.findColumn(fld.getName())
                    if col is None:
                        col = self.addColumn(fld.getName(),fld)
                    l.append(col)
            else:
                l.append(self.provideColumn(colName))
        self.visibleColumns = tuple(l)
            

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
        #if rowAttr is None:
        #    raise NoSuchField,name
        return self.addColumn(name,rowAttr,join)
    
    def addColumn(self,name,fld,join=None,**kw):
        if self._frozen:
            raise InvalidRequestError(
                "Cannot append columns to frozen %r" % self)
        #col = self._ds.columnClass(self, len(self._columns),
        #                                   name, join,fld)
        if len(kw):
            fld=fld.child(kw)
        col = DataColumn(self,len(self._columns),
                         name, fld, join)
        self._columns.append(col)
        col.setupAtoms()
        return col

##     def createColumn(self,colIndex,name,join,fld):
##         return DataColumn(self,colIndex,name,join,fld)

            
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
    
    def getSearchAtoms(self):
        l = []
        for col in self.visibleColumns:
            if hasattr(col.rowAttr,'type'):
                if isinstance(col.rowAttr.type,datatypes.StringType):
                    l += col.getAtoms()
        return tuple(l)
        
    

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
            col = self.getColumnByName(k)
            col.setCellValue(row,v)
            #rowattr = self.leadTable.getRowAttr(k)
            #row._values[rowattr._name] = v
            #rowattr.setCellValue(row,v)
            
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
    
##  def at2d(self,atomicTuple):
##      "atomic tuple to dict"
##      joinedRows = {}
##      d = {}
##      i = 0
##      for a in self._atoms:
##          if a.join is None:
##              d[a.name] = atomicTuple[i]
##          else:
##              pointedRow = a.join.pointer
##              joinedRows.setdefault(a.join.name,a.join.pointer)
##              joinedRows[a.join.name][a.name] = atomicTuple[i]
##          i += 1
##      return d

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
    
    def __init__(self,parent,store,columnNames):

        assert store.__class__.__name__ == "Store", \
               store.__class__.__name__+" is not a Store"
        self._store=store
        BaseColumnList.__init__(self,parent,columnNames)

        #self.leadTable = store._table 
        
        

    def __repr__(self):
        return self.__class__.__name__+\
               "(%s,columnNames='%s')" % (\
               self.getLeadTable().getTableName(),\
               " ".join([col.name for col in self._columns]))


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
        







class SimpleQuery(LeadTableColumnList):

    ANY_VALUE = types.NoneType
    
    def __init__(self, parent, store, session,
                 columnNames=None,
                 viewName=None,
                 orderBy=None,
                 sortColumns=None,
                 sqlFilters=None,
                 filters=None,
                 search=None,
                 samples=None,
                 label=None,
                 **kw):
        self._session = session
        LeadTableColumnList.__init__(self,parent,store,columnNames)
        self.rowcount = None
        
        for m in ('setBabelLangs','getLangs'):
            setattr(self,m,getattr(session,m))
        

        #self._table = store._table # shortcut
        self._schema = store._db.schema # shortcut
        self._connection = store._connection # shortcut

        for m in ('startDump','stopDump'):
            setattr(self,m,getattr(store._connection,m))
        self.rowcount = None

        
        
        #print "Datasource.configure()", self
        
        self._viewName = viewName
        if label is not None:
            assert type(label) == type(""),\
                   "%s not a string" % repr(label)
        self._label = label
            
        if orderBy is not None:
            assert sortColumns is None
            self.setOrderBy(orderBy)
        else:
            if sortColumns is None:
                if parent is not None:
                    sortColumns=parent.sortColumns
                else:
                    sortColumns=tuple()
            self.sortColumns=sortColumns
            #self.setSortColumns(sortColumns)
            
        self.setFilterExpressions(sqlFilters,search)

        if filters is None:
            if parent is not None:
                if parent._filters is not None:
                    filters=list(parent._filters)
        self._filters=filters
            
        
        if parent is None:
            self._samples = {}
        else:
            self._samples = dict(parent._samples)
        
        if samples is None:
            self.setSamples(**kw)
        else:
            #assert len(kw) == 0, "kw is %s, but samples is %s" % (\
            #   repr(kw),repr(samples))
            self._samples.update(samples)
            self.setSamples(**kw)

            
##     def getContext(self):
##         #return self._clist._context
##         return self._session


    def getContext(self):
        return self._session

    def report(self,**kw):
        from lino.reports.reports import createReport
        rpt=createReport(self,**kw)
        self._session.ui.report(rpt)
    

    def zap(self):
        self._store.zap()

    def addFilter(self,cls,*args,**kw):
        flt=cls(self,*args,**kw)
        if self._filters is None:
            self._filters=[]
        self._filters.append(flt)
        self.rowcount=None

    def deleteAll(self):
        self._connection.executeDeleteAll(self)
        

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
        return self.__class__(self,self._store,self._session,
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


    def setupForm(self,frm,row=None,**kw):
        if row is None:
            row = self[0]
        for dc in self.getVisibleColumns():
            frm.addDataEntry(dc)
##         for cell in row:
##             dc = cell.col
##             frm.addDataEntry(dcname=dc.name,
##                          label=dc.getLabel(),
##                          enabled=cell.canWrite(),
##                          getter=cell.__str__,
##                          setter=cell.setValueFromString)

        def afterSkip(nav):
            row = self[nav.currentPos]
            frm.data = row
            #frm.refresh()
##             for cell in row:
##                 setattr(frm.entries,cell.col.name,cell.format())
        frm.addNavigator(self,afterSkip=afterSkip)
        kw.setdefault('data',row)
        kw.setdefault('name',self.getLeadTable().getName())
        kw.setdefault('label',self.getLeadTable().getLabel())
        kw.setdefault('doc',self.getLeadTable().getDoc())
        frm.configure(**kw)

        
    
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

    def setdefaults(self,kw):
        if not kw.has_key('orderBy'):
            kw.setdefault('sortColumns',self.sortColumns)
        kw.setdefault('search',self._search)
        if self._label is not None:
            kw.setdefault('label',self._label)
        if self._sqlFilters is not None:
            kw.setdefault('sqlFilters',tuple(self._sqlFilters))
        if self._filters is not None:
            kw.setdefault('filters',list(self._filters))
            #print self._filters
        #if samples is None:
        #kw.setdefault('samples',self._samples)
        for k,v in self._samples.items():
            kw.setdefault(k,v)
        

##  def child(self,cl,columnNames=None,samples=None,**kw):
        
##      """creates a child (a detached copy) of this.  Modifying the
##      child won't affect the parent.  columnNames can optionally be
##      specified as first (non-keyword) argument.  if arguments are
##      given, then they override the corresponding value in the parent.
        
##      """
##      self.setdefaults(kw)
##      clist = self._clist
##      if columnNames is not None:
##          clist = DataColumnList(self,columnNames)            
##          #clist = clist.child(columnNames)
##      #query = self._area._table.query(columnNames=columnNames,**kw)

        
##      return cl(self._session,
##                   self._store,
##                   clist,
##                   samples=samples,
##                   **kw)


    def getRenderer(self,rsc,req,writer=None):
        return self._schema._datasourceRenderer(rsc,req,
                                                self.query(),
                                                writer)
    
    def getSession(self):
        return self._session

    def getTableName(self):
        return self.getLeadTable().getTableName()
    
    def getLabel(self):
        if self._label is None:
            lbl = self.getLeadTable().getLabel()
            if len(self._samples) > 0:
                lbl += " ("
                for (k,v) in self._samples.items():
                    col = self.getColumnByName(k)
                    lbl += col.name + "=" \
                             + col.rowAttr.format(v)
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

    def setSamples(self,**kw):
        "each value is a Python object"
        self._samples.update(kw)
        for (name,value) in self._samples.items():
            if value == self.ANY_VALUE:
                del self._samples[name]
            else:
                col = self.provideColumn(name)
    
    
    def getAtomicSamples(self):
        l = []
        atomicRow = self.makeAtomicRow() 
        for (name,value) in self._samples.items():
            col = self.getColumnByName(name)
            col.value2atoms(value,atomicRow,self.getDatabase())
            # 20050110
            # col.value2atoms(value,atomicRow,self.getContext())
            for atom in col.getAtoms():
                l.append((atom,atomicRow[atom.index]))
        return l
            
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
        filters must be a sequence of strings containing SQL expressions
        """
        self._sqlFilters = sqlFilters
        self._search = search
        
        l = []
        if self._sqlFilters is not None:
            assert issequence(self._sqlFilters), repr(self._sqlFilters)
            for expr in self._sqlFilters:
                assert type(expr) == types.StringType
                l.append(expr)
        #self.filterExp = tuple(l)

        if self._search is not None:
            if not issequence(self._search):
                self._search = (self._search,)
            # search is a tuple of strings to search for
            atoms = self.getSearchAtoms()
            for expr in self._search:
                l.append(" OR ".join(
                    [a.name+" LIKE '%"+expr+"%'" for a in atoms]))
                
        self.filterExpressions = tuple(l)
        


##  def __str__(self,):
##      return self._table.__class__.__name__+"Datasource"


    def getName(self):
        return self.getLeadTable().getTableName()+"Query"

##  def getRowId(self,values):
##      return [values.get(name,None)
##                for (name,type) in self._table.getPrimaryAtoms()]

    def executePeek(self,id):
        return self._connection.executePeek(self, id, self._session)

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
        kw.update(self._samples)
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
        return self._connection.csr2atoms(self,
                                          sqlatoms,
                                          self._session)
    
    def peek(self,*id):
        assert len(id) == len(self._pkColumns),\
                 "expected %d values but got %s" % \
                 ( len(self._pkColumns), repr(id))
        # flatten the id :
        l = []
        i = 0
        for col in self._pkColumns:
            l += col.rowAttr.value2atoms(id[i],self.getDatabase())
            i+=1
            
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
            self.rowcount = self._connection.executeCount(self)
        return self.rowcount
        
    def executeSelect(self,**kw):
        # overridden by Report
        return self._connection.executeSelect(self, **kw )




class Query(SimpleQuery):

    def __init__(self, parent, store, session,
                 columnNames=None,
                 pageNum=None,
                 pageLen=None,
                 **kw):
        
        
        SimpleQuery.__init__(self,parent,store,session,columnNames,
                             **kw)
        if parent is not None:
            if pageNum is None: pageNum=parent.pageNum
            if pageLen is None: pageLen=parent.pageLen
            
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
        
        return self._connection.executeSelect(self,
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














class DataColumn:
    
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
        # been requested for this column


    def __str__(self):
        return self.name

    def __repr__(self):
        return "<column %d:%s in %s>" % (self.index,self.name,
                                         repr(self._owner))
    def canWrite(self,row):
        return self.rowAttr.canWrite(row)

##      def getLabel(self):
##          return self.name

    def setupAtoms(self):
        #assert self._atoms is None
        atoms = []
##          if self.join is None:
##              if self._owner.hasJoins(): # len(query._joins) == 0:
##                  atomprefix = "lead."
##              else:
##                  atomprefix = ""
##          else:
##              atomprefix = join.name + "." 

        if self.join:
            joinName = self.join.name
        else:
            joinName = None
        #l = self.getNeededAtoms()
        #print repr(l)
        ctx = self._owner.getContext()
        for (name,type) in self.rowAttr.getNeededAtoms(ctx):
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


    def setCellValue(self,row,value):
        #print self, value
        self.rowAttr.setCellValue(row,value)
        self.rowAttr.afterSetAttr(row)

    def setValueFromString(self,row,s):
        self.rowAttr.setValueFromString(row,s)
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
##          try:
##              joinedRow = row._values[self.join.name]
##          except KeyError:
##              joinedRow = self.join.pointer.
##              row._values[self.join.name] = joinedRow
        
    def atoms2dict(self,atomicRow,valueDict,area):
        """Fill rowValues with values from atomicRow"""
        self.rowAttr.atoms2dict(atomicRow,valueDict,self._atoms,area)
##      attr = self.rowAttr
##      valueDict[attr.name] = attr.atoms2value(atomicRow,
##                                                           self._atoms,
##                                                           area)

    def atoms2value(self,atomicValues,sess):
        #return self.rowAttr.atoms2value(atomicRow,self._atoms,area)
        #atomicValues = [atomicRow[atom.index]
        #                    for atom in self._atoms]
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
    def getMaxWidth(self):
        return self.rowAttr.getMaxWidth()
    def getMinWidth(self):
        return self.rowAttr.getMinWidth()
    def getLabel(self):
        return self.rowAttr.getLabel()

#   def getNeededAtoms(self,db):
#       return
    
##     def format(self,value,context):
##         raise "no longer used?"
##         values = self.rowAttr.value2atoms(value,context)
##         #print self, ":", values
##         #if len(self._atoms) == 1:
##         #   return self._atoms[0].type.format(values[0])
##         assert len(values) == len(self._atoms)
##         l = [a.type.format(v) for v,a in zip(values,self._atoms)]
##         return ",".join(l)
        
    def parse(self,s,ds):
        l1 = s.split(',')
        assert len(l1) == len(self._atoms)
        atomicValues = [a.type.parse(s1)
                             for a,s1 in zip(self._atoms,l1)]
        return self.atoms2value(atomicValues,ds._session)
        
    def format(self,v):
        return self.rowAttr.format(v)
        
##  def parse(self,s):
##      return self.rowAttr.parse(v)
        















def trigger(events,*args):
    for e in events:
        if not e(*args): return False
    return True
            

class DataIterator:

    def __init__(self,ds,**kw):
        self.ds = ds
        self.csr = ds.executeSelect(**kw)
        self.recno = 0
        

        
    def __iter__(self):
        return self
    
    def next(self):
##         while True:
            sqlatoms = self.csr.fetchone()
            if sqlatoms == None:
                raise StopIteration
            atomicRow = self.ds.csr2atoms(sqlatoms)
            row=self.ds.atoms2row(atomicRow,new=False)
##             if self.ds._filters is not None:
##                 if not trigger(self.ds._filters,row):
##                     continue
                    
            self.recno += 1
            return row


















