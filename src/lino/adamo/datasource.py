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

from lino.misc.etc import issequence
from lino.adamo.query import DataColumnList
from lino.adamo.datatypes import STRING
from lino.adamo.exceptions import DataVeto, InvalidRequestError
from lino.adamo.rowattrs import FieldContainer, NoSuchField, Pointer

class SimpleDatasource:
    # inherited by Datasource

    ANY_VALUE = types.NoneType
    
    def __init__(self, session, store, clist=None, **kw):
        self.rowcount = None
        self._session = session
        for m in ('setBabelLangs','getLangs'):
            setattr(self,m,getattr(session,m))
        
        self._store = store
        if clist is None:
            clist = store._peekQuery
        assert clist.leadTable is store._table
        self._clist = clist
        #for m in 'getColumn', 'getColumnByName':
        #    setattr(self,m,getattr(clist,m))


        # self._db = store._db # shortcut
        self._table = store._table # shortcut
        self._schema = store._db.schema # shortcut
        self._connection = store._connection # shortcut

        #store.registerDatasource(self)
        
        for m in ('startDump','stopDump'):
            setattr(self,m,getattr(store._connection,m))

        self._samples = {}
        
        self.configure(**kw)

    def getDatabase(self):
        return self._store._db

    def getLeadTable(self):
        return self._clist.leadTable

##     def getContext(self):
##         #return self._clist._context
##         return self._session

    def mtime(self):
        return self._store.mtime()

##     def getDoc(self):
##         return self._store._table.doc

##     def getLabel(self):
##         return self._store._table.label

##     def getName(self):
##         return self._store._table.name


    def zap(self):
        self._store.zap()

    def configure(self,viewName=None,**kw):
        """
        
        note: _configure() is a separate method because the viewName
        parameter may control the default values for the other
        keywords.
        
        """
        self._viewName = viewName
        if viewName is not None:
            view = self._table.getView(viewName)
            if view is None:
                raise KeyError,viewName+": no such view"
            for k,v in view.items():
                kw.setdefault(k,v)
        self._configure(**kw)

    def _configure(self,
                   columnNames=None,
                   orderBy=None,
                   sqlFilters=None,
                   search=None,
                   samples=None,
                   label=None,
                   **kw):
        if label is not None:
            assert type(label) == type(""),\
                   "%s not a string" % repr(label)
        self._label = label
        if columnNames is not None:
            #self._clist = self.createColumnList(columnNames)
            
            # 20050119 : new DataColumnList's must have the database,
            # (not the session) as context! see tests/adamo/35.py
            self._clist = DataColumnList(
                self._store,
                self.getDatabase(), 
                columnNames)
        self.setOrderBy(orderBy)
        self.setFilterExpressions(sqlFilters,search)
        
        if samples is None:
            self.setSamples(**kw)
        else:
            #assert len(kw) == 0, "kw is %s, but samples is %s" % (\
            #   repr(kw),repr(samples))
            self._samples = samples
            self.setSamples(**kw)

    def apply_GET(self,**kw):
        """
        apply a (Twisted) GET dict to self
        """
        qryParams = {}
        #csvSamples = {}
        for k,v in kw.items():
            if k == 'ob':
                qryParams['orderBy'] = " ".join(v)
            elif k == 'v':
                viewName = v[0]
                if viewName == '':
                    viewName = None
                qryParams['viewName'] = viewName
            elif k == 'search':
                qryParams['search'] = v[0]
            elif k == 'flt':
                qryParams['sqlFilters'] = v
                #qryParams['sqlFilters'] = (v[0],)
                #qryParams['filters'] = tuple(l)

            else:
                #csvSamples[k] = v[0]
                col = self._clist.provideColumn(k)
                qryParams[k] = col.parse(v[0],self)
                
        self.configure(**qryParams)
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

    def get_GET(self):
        p = {}
        if self._orderBy != None:
            p['ob'] = self._orderBy
        if self._viewName != None:
            p['v'] = self._viewName
        if self._search != None:
            p['search'] = self._search
        if self._sqlFilters != None:
            p['flt'] = self._sqlFilters
        for (key,value) in self._samples.items():
            col = self.getColumnByName(key)
            p[key] = col.format(value,self)
        return p
        
        
    def getColumn(self,i):
        col = self._clist.visibleColumns[i]
    def getColumnByName(self,name):
        self._clist.getColumnByName(name)
        
        
##  def getView(self,viewName):
##      return self._table.getView(viewName)

##  def createColumnList(self,columnNames):
##      # (no longer) overridden by report.Report
##      return DataColumnList(self._store, self._session, columnNames)
    
##  def createColumn(self,colIndex, name, join,fld):
##      # overridden by report.Report
##      return DataColumn(self,colIndex, name, join,fld)


##  def clearSample(self,*names):
##      for name in names:
##          del self._samples[name]
    
    #def __getattr__(self,name):
##     def field(self,name):
##         return self._table._rowAttrs[name]

    
    def query(self,columnNames=None,**kw):
        self.setdefaults(kw)
        return self.__class__( self._session,
                               self._store,
                               self._clist,
                               columnNames=columnNames,
                               **kw)


    def setupReport(self,rpt,**kw):
        for dc in self.getVisibleColumns():
            rpt.addDataColumn(dc,
                              width=dc.getPreferredWidth(),
                              label=dc.getLabel())
        kw.setdefault('name',self._table.getName())
        kw.setdefault('label',self._table.getLabel())
        kw.setdefault('doc',self._table.getDoc())
        rpt.configure(**kw)
        
    
    def executeReport(self,rpt=None,**kw):
        if rpt is None:
            rpt = self._session.report()
        self.setupReport(rpt,**kw)
        rpt.execute(self)


##     def setupTableEditor(self,e):
##         frm = e.getForm()
##         m = frm.addMenu("file",label="&File")
##         m.addItem(label="&Exit",frm.close)
##         m = frm.addMenu("row",label="&Row")
##         def printRow(frm):
##             for row in r.getSelectedRows():
                
##         m.addItem(label="&Print",self.printRow)

##     def printRow(self,ui):
##         self._table.ui_printRow(ui)
        
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
        kw.setdefault('name',self._table.getName())
        kw.setdefault('label',self._table.getLabel())
        kw.setdefault('doc',self._table.getDoc())
        frm.configure(**kw)

        
    
##     def report(self,columnNames=None,**kw):
##         kw.setdefault("name",self._table.getTableName())
##         kw.setdefault("label",self._table.getLabel())
##         rpt = self._session.report(self,**kw)
        
##         if columnNames is None:
##             for dc in self.getVisibleColumns():
##                 rpt.addDataColumn(dc)
##         else:
##             for colName in columnNames.split():
##                 dc = self.getColumn(colName)
##                 rpt.addDataColumn(dc)
                
##         return rpt
        
##         from report import Report
##         return Report( self._session,
##                        self._store,
##                        self._clist,
##                        columnNames=columnNames,
##                        **kw)

        

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
        kw.setdefault('orderBy',self._orderBy)
        kw.setdefault('search',self._search)
        if self._label is not None:
            kw.setdefault('label',self._label)
        if self._sqlFilters is not None:
            kw.setdefault('sqlFilters',tuple(self._sqlFilters))
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
    
##  def getContext(self):
##      return self._session

    def getSession(self):
        return self._session

    def getTableName(self):
        return self._table.getTableName()
    
    def getLabel(self):
        if self._label is None:
            lbl = self._table.getLabel()
            if len(self._samples) > 0:
                lbl += " ("
                for (k,v) in self._samples.items():
                    col = self._clist.getColumnByName(k)
                    lbl += col.name + "=" \
                             + col.rowAttr.format(v)
                lbl += ")"
            return lbl
        if callable(self._label):
            raise "not yet tested"
            return self._label(self)
        return self._label
            

    def setOrderBy(self,orderBy):
        #assert type(orderBy) is type('')
        self._orderBy = orderBy
        l = []
        if orderBy is not None:
            for colName in orderBy.split():
                l.append(self._clist.provideColumn(colName))
        self.orderByColumns = tuple(l)

    def setSamples(self,**kw):
        "each value is a Python object"
        self._samples.update(kw)
        for (name,value) in self._samples.items():
            if value == self.ANY_VALUE:
                del self._samples[name]
            else:
                col = self._clist.provideColumn(name)
        return
    
    
##  def setSamples_unused(self):
##      sampleColumns = []
##      atomicSamples = []
##      atomicRow = self._clist.makeAtomicRow(self._context) 

##      #tmpRow = self._table.Row(self,{},False,pseudo=True)
        
##      for (name,value) in self._samples.items():
##          col = self._clist.getColumn(name)
##          #attr = self._table.getRowAttr(name)
##          sampleColumns.append( (col,value) )
##          #setattr(tmpRow,name,value)
##          #attr.setCellValue(tmpRow,value)
##          col.value2atoms(value,atomicRow,self._db)
            
##      self.sampleColumns = tuple(sampleColumns)
        
##      #atomicRow = self.row2atoms(tmpRow)
##      for col,value in self.sampleColumns:
##          for atom in col.getAtoms():
##              atomicSamples.append((atom,atomicRow[atom.index]))
## ##           for aname,atype in attr.getNeededAtoms(self._db):
## ##               atomicSamples.append(
## ##                   (aname,atype, tmpRow.getAtomicValue(aname)) )
                
##      self.atomicSamples = tuple(atomicSamples)
        
    def getAtomicSamples(self):
        l = []
        atomicRow = self._clist.makeAtomicRow() 
        for (name,value) in self._samples.items():
            col = self._clist.getColumnByName(name)
            col.value2atoms(value,atomicRow,self.getDatabase())
            # 20050110
            # col.value2atoms(value,atomicRow,self.getContext())
            for atom in col.getAtoms():
                l.append((atom,atomicRow[atom.index]))
        return l
            
##  def setCsvSamples(self,**kw):
##      "each value is a (comma-separated) string"
##      sampleColumns = []
##      atomicSamples = []
##      tmpRow = self._table.Row(self,{},False,pseudo=True)
##      for (name,value) in kw.items():
##          attr = self._table.getRowAttr(name)

##          rid = value.split(',')
##          i = 0
##          for aname,atype in attr.getNeededAtoms(self._db):
##              tmpRow.setAtomicValue(aname,atype.parse(rid[i]))
##              i += 1
                
##          value = attr.getCellValue(tmpRow)
##          sampleColumns.append( (attr,value) )
##          self._samples[name] = value
                
##          for aname,atype in attr.getNeededAtoms(self._db):
##              atomicSamples.append(
##                  (aname,atype, tmpRow.getAtomicValue(aname)) )
                
##      self.sampleColumns = tuple(sampleColumns)
##      self.atomicSamples = tuple(atomicSamples)


    def setSqlFilters(self,*sqlFilters):
        self.setFilterExpressions(sqlFilters,self._search)
        
    def setSearch(self,search):
        self.setFilterExpressions(self._sqlFilters,search)
        
    def getVisibleColumns(self):
        return self._clist.visibleColumns
    
    def getAttrList(self):
        return self._table.getAttrList()
    
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
            atoms = self._clist.getSearchAtoms()
            for expr in self._search:
                l.append(" OR ".join(
                    [a.name+" LIKE '%"+expr+"%'" for a in atoms]))
                
        self.filterExpressions = tuple(l)
        


##  def __str__(self,):
##      return self._table.__class__.__name__+"Datasource"

    def __repr__(self,):
        return self._table.__class__.__name__+"Datasource"

    def getAtoms(self):
        return self._clist.getAtoms()


    def getName(self):
        return self._table.getTableName()+"Source"

##  def getRowId(self,values):
##      return [values.get(name,None)
##                for (name,type) in self._table.getPrimaryAtoms()]

    def executePeek(self,id):
        return self._connection.executePeek(self._clist,id)

    def commit(self):
        self._session.commit()


    def appendRow(self,*args,**kw):
        #if self._table.getTableName() == "PARTNERS":
        #   print "datasource.py", args
        #   print [col.name for col in self._clist.visibleColumns]
        #self.startDump()
        row = self._table.Instance(self,{},True)
        #row.lock()
        kw.update(self._samples)
        self._clist.updateRow(row,*args,**kw)
        
        self.rowcount = None
        self._store.setAutoRowId(row)
        row.writeToStore()
        #row.unlock()
        self._store.fireUpdate()
        #print self.stopDump()
        return row


    def __getitem__(self,offset):
        row = self.getRowAt(offset)
        if row is None:
            msg = "%s[%d] (%d) rows" % (self._table.getTableName(),
                                                 offset,len(self))
            raise IndexError,msg
        
        return row

    def getRowAt(self,offset):
        assert type(offset) is types.IntType
        if offset < 0:
            offset = len(self) + offset 
        csr = self.executeSelect(offset=offset,limit=1)
        if csr.rowcount == 0:
            return None
        assert csr.rowcount == 1
        atomicRow = csr.fetchone()
        # d = self._clist.at2d(atomicRow)
        # return self._table.Row(self,d,False)
        return self.atoms2row(atomicRow,False)


    def peek(self,*id):
        assert len(id) == len(self._clist._pkColumns),\
                 "expected %d values but got %s" % \
                 ( len(self._clist._pkColumns), repr(id))
        # flatten the id :
        l = []
        i = 0
        for col in self._clist._pkColumns:
            l += col.rowAttr.value2atoms(id[i],self.getDatabase())
            i+=1
            
        atomicRow = self._connection.executePeek(self._clist,l)
        if atomicRow is None:
            return None
        #d = self._clist.at2d(atomicRow)
        #return self._table.Row(self,d,False)
        return self.atoms2row(atomicRow,False)

    def getInstance(self,atomicId,new):
        row = self._table.Instance(self,{},new)
        i = 0
        for col in self._clist._pkColumns:
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
            col = self._clist.visibleColumns[i]
            flt.append(col.getTestEqual(self,arg))
            i+=1
        for k,v in knownValues.items():
            col = self._clist.getColumnByName(k)
            flt.append(col.getTestEqual(self,v))
        ds = self.query(sqlFilters=(' AND '.join(flt),))
        return ds
        
    def findone(self,**knownValues):
        ds = self.find(**knownValues)
        #print [a.name for a in ds.query._atoms]
        #q = self._table.query(filters=' AND'.join(flt))
        #csr = self._connection.executeSelect(q)
        csr = ds.executeSelect()
        if csr.rowcount != 1:
            #print "findone(%s) found %d rows" % (
            #    repr(knownValues), csr.rowcount)
            return None
            #raise DataVeto("findone(%s) found %d rows" % (
            #   repr(knownValues), csr.rowcount))
        
        atomicRow = csr.fetchone()
        assert atomicRow is not None, repr(csr.rowcount)
        #d = self._clist.at2d(atomicRow)
        #return self._table.Row(self,d,False)
        return self.atoms2row(atomicRow,False)
    

        
    def atoms2row(self,atomicRow,new):
        row = self._table.Instance(self,{},new)
        self._clist.atoms2row(atomicRow,row)
        return row
##      return DataRow(self,atomicRow,new)
##      assert atomicRow is not None
##      atomicDict = self._query.at2d(atomicRow)
##      return self._store.ad2row(atomicDict,new)


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
        self.rowcount = None
    
    def __len__(self):
        if self.rowcount is None:
            self.rowcount = self._connection.executeCount(self)
        return self.rowcount
        
    def executeSelect(self,**kw):
        # overridden by Report
        return self._connection.executeSelect(self, **kw )




class Datasource(SimpleDatasource):

    def __init__(self, session, store, clist=None,
                 pageNum=None,
                 pageLen=None,
                 **kw):
        
        SimpleDatasource.__init__(self,session, store, clist, **kw)
        
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
        default to either 1 OR lastPage with a future option
        "fromBottom" """


        if self.pageLen is None:
            self.startOffset = 0
        else:
            if self.pageNum is None:
                self.pageNum=1
            elif self.pageNum < 0:
                self.pageNum = self.lastPage + self.pageNum - 1
            elif self.pageNum > self.lastPage:
                raise "pageNum > lastPage",self.lastPage
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
        SimpleDatasource.apply_GET(self,**p)
        #self.config(**rptParams)
        
    def get_GET(self):
        p = SimpleDatasource.get_GET(self)
        if self.pageNum != None:
            p['pg'] = self.pageNum
        if self.pageLen != None:
            p['pl'] = self.pageLen
        return p
        

    def setdefaults(self,kw):
        kw.setdefault('pageNum',self.pageNum)
        kw.setdefault('pageLen',self.pageLen)
        SimpleDatasource.setdefaults(self,kw)

    def executeSelect(self,
                      limit=None,
                      offset=None,**kw):
        # overrides SimpleDatasource.executeSelect()
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

    

    
            

class DataIterator:

    def __init__(self,ds,**kw):
        self.ds = ds
        self.csr = ds.executeSelect(**kw)
        self.recno = 0
        

        
    def __iter__(self):
        return self
    
    def next(self):
        atomicRow = self.csr.fetchone()
        if atomicRow == None:
            raise StopIteration
        self.recno += 1
        return self.ds.atoms2row(atomicRow,new=False)


class DataRow:
    def __init__(self,fc,clist,values,dirty=False):
        assert isinstance(fc,FieldContainer)
        #assert isinstance(clist,BaseColumnList)
        assert type(values) == types.DictType
        self.__dict__["_values"] = values 
        self.__dict__["_fc"] = fc
        self.__dict__["_clist"] = clist
        self.__dict__["_dirty"] = dirty
        
    def __getattr__(self,name):
        assert self.__dict__.has_key("_fc")
        #print repr(self._fc)
        rowattr = self._fc.getRowAttr(name)
        return rowattr.getCellValue(self)
    
    def __setattr__(self,name,value):
      #def setAtomicValue(self,name,value)
        if self.__dict__.has_key(name):
            self.__dict__[name] = value
            return
        if not self.isLocked():
            raise InvalidRequestError("row is not locked")
        #assert self._locked
        rowattr = self._fc.getRowAttr(name)
        rowattr.setCellValue(self,value)
##      try:
##          rowattr.acceptTrigger(self,value)
##          rowattr.setCellValue(self,value)
##      except DataVeto,e:
##          self.getSession().errorMessage(str(e))
##          return
        rowattr.afterSetAttr(self)
        self.__dict__['_dirty'] = True

    def getFieldValue(self,name):
        try:
            return self._values[name]
        except KeyError:
            raise NoSuchField,name


    def makeDataCell(self,colIndex,col):
        #return self.getSession()._dataCellFactory(self,colIndex,col)
        return DataCell(self,colIndex,col)


    def setDirty(self):
        self.__dict__["_dirty"] = True

    def __getitem__(self,i):
        col = self._clist.visibleColumns[i]
        return self.makeDataCell(i,col)
        #return col.getCellValue(self)
        
##  def __getitem__(self,i):
##      col = self._clist.visibleColumns[i]
##      return col.getCellValue(self)
        
    def __setitem__(self,i,value):
        col = self._clist.visibleColumns[i]
        assert self._pseudo or self._locked or self._new
        col.rowAttr.setCellValue(self,value)
        self.__dict__["_dirty"] = True
        
    def __iter__(self):
        return RowIterator(self,self._clist.visibleColumns)
    
    def __len__(self):
        return len(self._clist.visibleColumns)
    
    def getCells(self,columnNames=None):
        return RowIterator(self,self._clist.getColumns(columnNames))
        
    def update(self,**kw):
        self.lock()
        for (k,v) in kw.items():
            setattr(self,k,v)
        self.validate()
        self.unlock()


    def canWrite(self):
        return True
    
    def validate(self):
        pass

    def lock(self):
        pass
    
    def unlock(self):
        pass
    
    
    def isLocked(self):
        return True

    def isDirty(self):
        return self.__dict__['_dirty']

    def makeComplete(self):
        pass


class StoredDataRow(DataRow):
    # base class for Table.Row
    
    def __init__(self,ds,values,new,pseudo=False):
        """
        """
        assert type(new) == types.BooleanType
        DataRow.__init__(self,ds._table,ds._clist,values,dirty=new)

        self.__dict__["_ds"] = ds
        self.__dict__["_new"] = new
        self.__dict__["_pseudo"] = pseudo
        self.__dict__["_complete"] = False #ds.isComplete()
        self.__dict__["_locked"] = False
        self.__dict__["_isCompleting"] = False

    def __eq__(self, other):
        if (other is None) or (other is self._ds.ANY_VALUE):
            return False
        return self.getRowId() == other.getRowId()
        #return tuple(self.getRowId()) == tuple(other.getRowId())
        
    def __ne__(self, other):
        if (other is None) or (other is self._ds.ANY_VALUE):
            return True
        return self.getRowId() != other.getRowId()
        #return tuple(self.getRowId()) == tuple(other.getRowId())
        
    def getRenderer(self,rsc,req,writer=None):
        return self._ds._table._rowRenderer(rsc,req,self,writer)

##  def writeParagraph(self,parentResponder):
##      rsp = self.getRenderer(parentResponder.resource,
##                                    parentResponder.request,
##                                    parentResponder._writer)
##      #assert rsp.request is self.request
##      rsp.writeParagraph()
    
    def getSession(self):
        return self._ds._session

    def getDatabase(self):
        return self._ds.getDatabase()

    def getTableName(self):
        return self._ds.getTableName()
    
##     def getContext(self):
##         return self._ds.getContext()
    
    def writeReport(self,doc):
        rpt = doc.report(label=self.getLabel())
        for c in self:
            rpt.addColumn(lambda cell: cell.col.getLabel(),
                          width=20,
                          label="fieldName")
            rpt.addColumn(lambda cell: str(cell),
                          width=50,
                          label="value")
        rpt.execute(self)
    
    def isComplete(self):
        return self._complete
    
    def isLocked(self):
        return (self._locked or self._new or self._pseudo)

    def isNew(self):
        return self._new
    
    def getRowId(self):
        id = [None] * len(self._clist.leadTable.getPrimaryAtoms())
        for col in self._clist._pkColumns:
            col.row2atoms(self,id)
##      if self._ds._table.getTableName() == "CITIES":
##          print [(col.name,col.rowAttr) for col in self._ds._clist._pkColumns]
##          print [atom.name for atom in self._ds._clist._atoms]
##          print id
        return id
        #return self._ds.getRowId(self._values)
        
    def getLabel(self):
        return str(tuple(self.getRowId()))
        #return self._ds._table.getRowLabel(self)
        
    def getFieldValue(self,name):
        try:
            return self._values[name]
        except KeyError:
            if self._isCompleting:
                return None
            self.makeComplete()
            try:
                return self._values[name]
            except KeyError:
                raise NoSuchField,name


    def _readFromStore(self):
        """
        make this row complete using a single database lookup
        """
        assert not self._pseudo,\
                 "%s : readFromStore() called for a pseudo row" % repr(self)
        assert not self._complete,\
                 "%s : readFromStore() called a second time" % repr(self)
        assert not self._isCompleting
        
        # but what if atoms2row() causes __getattr__ to be called
        # again? maybe a switch _isCompleting to check this.
        self.__dict__["_isCompleting"] = True
        
        # print "makeComplete() : %s" % repr(self)
        id = self.getRowId()
        #leadRow = self._ds._store._peekQuery.peek(id)
        #d = self._values
        atomicRow = self._ds._connection.executePeek(
            self._ds._store._peekQuery,id)
        if self._new:
            if atomicRow is not None:
                raise DataVeto("Cannot create another %s row %s" \
                                    % (self.__class__.__name__, id))
            #for a in self._ds._store._peekQuery.getAtoms():
            for attrname in self._ds._table.getAttrList():
                self._values.setdefault(attrname,None)
        else:
            if atomicRow is None:
                #self.__dict__['_new'] = True
                raise DataVeto("Cannot find %s row %s" \
                                    % (self._ds._table.getTableName(), id))
            self._ds._store._peekQuery.atoms2row(atomicRow,self)
            #for a in self._ds._store._peekQuery.getAtoms():
            #   self._values.setdefault(a.name,atomicRow[a.index])
            #if self._dirty:
            #   raise "cannot yet call readFromStore() for a dirty row"
                
        #self.__dict__['_values'] = atomicRow
        
        """maybe a third argument `fillMode` to atoms2dict() which
        indicates whether existing (known) values should be
        overwritten, checked for equality or ignored...  """

        self.__dict__['_complete'] = True
        self.__dict__["_isCompleting"] = False

    def checkIntegrity(self):
        #if not self._complete:
        self.makeComplete()
        for name,attr in self._ds._table._rowAttrs.items():
            msg = attr.checkIntegrity(self)
            if msg is not None:
                return msg
        
##  def getAtomicValue(self,i):
##      return self._values[i]

##  def atomicValues(self):
##      return self._values
        

    def getAttrValues(self,columnNames=None):
        l = []
        if columnNames is None:
            q = self._area._query()
            for col in q.getColumns():
                attr = col.rowAttr 
                l.append( (attr,attr.getValueFromRow(self)) )
        else:
            for name in columnNames.split():
                col = q.getColumn(name)
                attr = col.rowAttr
                #attr = self._area._table.__getattr__(name) 
                l.append( (attr,attr.getValueFromRow(self)) )
        return tuple(l)
        
    
    def __repr__(self):
        if self._isCompleting:
            return "Uncomplete " + repr(self._ds) + "Row(" \
                     + str(self._values)+")"
        return self._ds._table.getTableName() + "Row(" + str(self._values)+")"
        #return repr(self._ds) + "Row" + repr(tuple(self.getRowId()))

    def __str__(self):
        return str(self.getLabel())





    def lock(self):
        assert not self._new, "Cannot lock a new row"
        assert not self._locked, "already locked"
        self.__dict__["_locked"] = True
        self._ds._store.lockRow(self)
            

    def unlock(self):
        assert self._locked, "this row was not locked"
        
            
##          msg = self.validate()
##          if msg:
##              raise DataVeto(repr(self) + ': ' + msg)
            
        #assert not None in self.getRowId(), "incomplete pk"
        self.__dict__["_locked"] = False
        self._ds._store.unlockRow(self)
        if self._dirty:
            self.writeToStore()
        

    def writeToStore(self):
        #print "commit: ", self
        #assert not self._locked
        #if self._locked:
        #   self.unlock()
        try:
            self.validate()
        except DataVeto,e:
            raise DataVeto(repr(self) + ': ' + str(e))
        if self._new:
            self._ds._connection.executeInsert(self)
            self.__dict__["_new"] = False
        else:
            if not self._dirty: return
            self._ds._connection.executeUpdate(self)
        self.__dict__["_dirty"] = False
        

            

    def makeComplete(self):
        if self._pseudo or self._complete or self._isCompleting:
            return False
        self._readFromStore()
        return True

    def exists(self):
        if not self._complete:
            self._readFromStore()
        return not self.isNew()

    
    


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
        for name,attr in self._ds._table._rowAttrs.items():
            msg = attr.vetoDeleteIn(self)
            if msg:
                return msg


class RowIterator:

    def __init__(self,row,columns):
        self.row = row
        self.colIndex = 0
        self._columns = columns
        
    def __iter__(self):
        return self
    
    def next(self):
        if self.colIndex == len(self._columns):
            raise StopIteration
        col = self._columns[self.colIndex]
        self.colIndex += 1
        return self.row.makeDataCell(self.colIndex,col) 


class DataCell:
    def __init__(self,row,colIndex,col):
        #self.colIndex = colIndex
        self.row = row
        self.col = col

    def getValue(self):
        return self.col.getCellValue(self.row)
        
##     def __str__(self):
##         return str(self.col.getCellValue(self.row))
##         #~ v = self.col.getCellValue(self.row)
##         #~ if v is None:
##             #~ return "None"
##         #~ return self.col.rowAttr.format(v)
    
##     def format(self):
##         v = self.col.getCellValue(self.row)
##         if v is None:
##             return ""
##         return self.col.rowAttr.format(v)

    def canWrite(self):
        if self.row.canWrite():
            return self.col.canWrite(self.row)
        return False
    
    def __repr__(self):
        return repr(self.col.getCellValue(self.row))
        #~ v = self.col.getCellValue(self.row)
        #~ if v is None:
            #~ return "None"
        #~ return self.col.rowAttr.format(v)
    
    def __str__(self):
        v = self.col.getCellValue(self.row)
        if v is None:
            return ""
        return self.col.rowAttr.format(v)
    
    #def parseAndSet(self,s):
    def setValueFromString(self,s):
        if len(s) == 0:
            self.setValue(None)
        else:
            v=self.col.rowAttr.parse(s)
            self.setValue(v)
        
    def setValue(self,value):
        self.col.setCellValue(self.row,value)

