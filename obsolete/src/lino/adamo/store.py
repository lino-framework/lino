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

from time import time

from lino.misc.descr import Describable
#from lino.console import syscon

from lino.adamo.exceptions import \
     DataVeto, InvalidRequestError, RowLockFailed
#from lino.adamo.datasource import Datasource
from lino.adamo.query import PeekQuery, Query
from lino.adamo import datatypes 

## class Lock:
##     def __init__(self,row):
##         self._row = row

class BaseStore:
    def __init__(self,db,table):
        self._mtime=None
        self._dirty = False
        self._db = db
        self._table = table
        
        self._iterators=[]
        self._lockedRows = {}
        
        if len(self._table.getPrimaryAtoms()) == 1:
            self._lastId = None
        else:
            self._lastId = {}

        self._peekQuery = PeekQuery(self)

    
    def __repr__(self):
        return "Store(%s.%s)"%(self._db.name,self._table)

    def mtime(self):
        return self._mtime

    def touch(self):
        self._mtime = time()
        self._dirty = True
        
    def onConnect(self):
        self._table.onConnect(self)
        
    def getTable(self):
        return self._table
        #return self.schema.getTable(self._table.getTableId())
    
    def onStartup(self):
        pass
    
    def fireUpdate(self):
        pass
        #for ds in self._datasources:
        #    ds.onStoreUpdate()

        

    def addIterator(self,i):
        self._iterators.append(i)
        
    def removeIterator(self,i):
        self._iterators.remove(i)

    def query(self,sess,columnNames=None,**kw):
        if columnNames is None and len(kw) == 0:
            return self._peekQuery
        return Query(None,self,sess,columnNames,**kw)


    def checkIntegrity(self,sess):
        #if self._status != self.SST_MUSTCHECK:
        #    return
        if self.mustCheckTables():
            q = self.query()
            l = len(q)
            def f(task):
                for row in q:
                    task.increment()
                    msg = row.checkIntegrity()
                    if msg is not None:
                        task.error("%s[%s] : %s",
                                  q._table.getTableName(),
                                  str(row.getRowId()),
                                  msg)
            sess.loop(f, "Checking Table %s : %d rows" % (
                q._table.getTableName(),l),maxval=l)
            
        #self._status = self.SST_READY
        
    def lockRow(self,row):
        k = tuple(row.getRowId())
        if self._lockedRows.has_key(k):
            raise RowLockFailed("Row is locked by another process")
        self._lockedRows[k] = row
        #print self,"lock row", row

    def isLockedRow(self,*k):
        return self._lockedRows.has_key(k)
    
    def unlockRow(self,row):
        k = tuple(row.getRowId())
        try:
            return self._lockedRows.pop(k)
        except KeyError,e:
            raise RowLockFailed("Row was not locked")
        #print self,"unlock row", row
        #return row
        #assert x._locked == dbc
        #assert x._query == qry
        #self.touch()
        #if row.isDirty():
        #    self._dirtyRows[k] = row
        
##     def lockRow(self,row):
##         # todo: use getLock() / releaseLock()
##         self.removeFromCache(row)
##         self._lockedRows.append(row)
        
##     def unlockRow(self,row):
##         self.addToCache(row)
##         self._lockedRows.remove(row)
##         self.touch()
##         #row.writeToStore()
##         #if row.isDirty():
##         #   key = tuple(row.getRowId())
##         #   self._dirtyRows[key] = row

    def unlockAll(self):
        #assert len(self._lockedRows) == 0
##         #print "Datasource.unlockAll()",self
        for row in self._lockedRows.values():
            print "forced unlock:", row
            #row.getSession().debug("forced unlock: %r",row)
            row.unlock()
##         #assert len(self._lockedRows) == 0
        
    #def unlockQuery(self,dbc):
    def unlockContext(self,dbc):
        for row in self._lockedRows.values():
            if row._context == dbc:
                print "forced unlock:", row
                row.unlock()
##         #print "Datasource.unlockAll()",self
##         for row in self._lockedRows:
##             if row._ds == ds:
##                 row.unlock()
    
        
        
    def csr2atoms(self,qry,sqlatoms):
        raise NotImplementedError
    
    def zap(self):
        raise NotImplementedError

    def executeCount(self,qry):
        raise NotImplementedError
    
    def executePeek(self,qry,id):
        raise NotImplementedError

    def executeSelect(self,qry,**kw):
        raise NotImplementedError


        

class Store(BaseStore):
    """
    One instance per Database and Table.
    Distributes auto-incrementing keys for new rows.
    """

    SST_MUSTCHECK = 1
    SST_VIRGIN = 2 # must populate with default data?
    #SST_MUSTLOAD = 3 # must load mirror?
    SST_READY = 3
    
    def __init__(self,conn,db,table):
        self._connection = conn 
        for m in ('startDump','stopDump'):
            setattr(self,m,getattr(conn,m))
        self._mtime = conn.getModificationTime(table)
        self._virgin=None
        BaseStore.__init__(self,db,table)

    def zap(self):
        self._connection.executeZap(self._table)
        self.touch()

    def executeCount(self,qry):
        return self._connection.executeCount(qry)
    
    def executePeek(self,qry,id):
        return self._connection.executePeek(qry,id)

    def executeSelect(self,qry,**kw):
        return self._connection.executeSelect(qry, **kw )

    def csr2atoms(self,qry,sqlatoms):
        return self._connection.csr2atoms(qry,sqlatoms)
    
    def mustCheckTables(self):
        return self._connection.mustCheckTables()

    def onStartup(self):
        if self._virgin is None:
            if self._connection.mustCreateTables():
                self._connection.executeCreateTable(self._peekQuery)
                self._virgin=True
            else:
                self._virgin=False

    def isVirgin(self):
        return self._virgin
                
        
        
        
    def removeFromCache(self,row):
        pass
    
    def addToCache(self,row):
        pass

    def commit(self):
        ""
        if len(self._lockedRows) > 0:
            #print [id for id in self._lockedRows.keys()]
            raise InvalidRequestError(
                "Cannot commit %s while %d rows are locked" \
                % (self,len(self._lockedRows)))
##         for row in self._lockedRows:
##             row.writeToStore()
        self._connection.commit()
            
    def close(self):
        for i in self._iterators:
            print "Forced Cursor.close() for %r" % i
            i.close()
        self.unlockAll()
        #for ds in self._datasources:
        #    ds.close()


##     def removeDatasource(self,ds):
##         self._datasources.remove(ds)
        

    def setAutoRowId(self,row):
        "set auto-incrementing row id"
        autoIncCol = self._peekQuery._pkColumns[-1]
##         if autoIncCol.rowAttr.type is not ROWID:
##             return
##         if self._table.getTableName() == "Invoices":
##             print autoIncCol.rowAttr.type
##             raise "foo"
        #assert isinstance(autoIncCol.rowAttr.type,AutoIncType)
        assert len(autoIncCol._atoms) == 1
        autoIncAtom = autoIncCol._atoms[0]
        
        if not isinstance(autoIncAtom.type,datatypes.AutoIncType):
            return
        
##         if self._table.getTableName() == "Partners":
##             print repr(autoIncAtom.type)
##             raise "foo"
        
        pka = self._table.getPrimaryAtoms()
        id = row.getRowId()
        #id = atomicRow[:len(pka)]
        #print "area.py:%s" % repr(id)
        front, tail = id[:-1], id[-1]
        if None in front:
            raise DataVeto("Incomplete primary key %s for table %s" %(
                repr(id),self._table.getTableName()))
        #tailAtomicName = pka[-1][0]
        #tailType = pka[-1][1]

        # get or set self._lastId
        if len(front):
            # self._lastId is a dict
            x = self._lastId
            for i in front[:-1]:
                try:
                    x = x[i]
                except KeyError:
                    x[i] = {}
                    x = x[i]
            # x is now the bottom-level dict
            i = front[-1]
            if not x.has_key(i):
                x[i] = self._connection.executeGetLastId(
                    self._table,front)
                if x[i] is None:
                    x[i] = 0
            if tail is None:
                x[i] += 1
                id[-1] = x[i]
            elif tail > x[i]:
                x[i] = tail
                
        else:
            if self._lastId is None:
                self._lastId = self._connection.executeGetLastId(
                    self._table,front)
                if self._lastId is None:
                    self._lastId = 0
            if tail is None:
                if type(self._lastId) == type(''):
                    self._lastId = str(int(self._lastId)+1)
                else:
                    self._lastId += 1
                id[-1] = self._lastId
            elif tail > self._lastId:
                self._lastId = tail

        if tail is None:
            #row.setAtomicValue(pka[-1][0],id[-1])
            #atomicRow[len(pka)-1] = id[-1]
            autoIncCol.setCellValue(row,id[-1])
        #return tuple(id)


class VolatileStore(BaseStore):
    def __init__(self,lst,db,table):
        BaseStore.__init__(self,db,table)
        self._list=lst # a list of tuples of atomic values
        raise "not yet usable (maybe never)"

    def csr2atoms(self,qry,sqlatoms):
        return sqlatoms
    
    def zap(self):
        raise NotImplementedError

    def executeCount(self,qry):
        raise NotImplementedError
    
    def executePeek(self,qry,id):
        raise NotImplementedError

    def executeSelect(self,qry,**kw):
        raise NotImplementedError

    

#from lino.console.task import Task
from lino.console.task import Progresser

#class Populator(Task):
class Populator(Progresser):
    def run(self,dbc):
        status=dbc.getSessionStatus()
        for store in dbc.db.getStoresById():
            if not store.isVirgin():
                self.debug("%s is not virgin",
                           store.getTable().name) 
            else:
                name = "populate"+store.getTable().name
                try:
                    m = getattr(self,name)
                except AttributeError:
                    self.debug("No method %s.%s()",
                               self.__class__,name) 
                else:
                    self.debug("Running %s.%s()",
                               self.__class__,name) 
                    self.status("Populating %s." % store)
                    qry=store.query(dbc,"*")
                    m(qry)
                    store.commit()
        dbc.setSessionStatus(status)
    


