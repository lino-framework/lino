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

from time import time

from lino.misc.descr import Describable
from lino.adamo.exceptions import DataVeto, InvalidRequestError
#from lino.adamo.datasource import Datasource
from lino.adamo.query import PeekQuery, Query
from lino.adamo import datatypes 

class Lock:
    def __init__(self,row):
        self._row = row
        

class Store:
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
        self._mtime = conn.getModificationTime(table)
        self._db = db
        self._table = table
        self._status = self.SST_MUSTCHECK
        
        # self._schema = db.schema # shortcut
        
        #self._datasources = []
        self._lockedRows = {}
        
        if len(self._table.getPrimaryAtoms()) == 1:
            self._lastId = None
        else:
            self._lastId = {}

        self._peekQuery = PeekQuery(self)


    def mtime(self):
        return self._mtime

    def touch(self):
        self._mtime = time()
        
    def onConnect(self):
        self._table.onConnect(self)
        
    def getTable(self):
        return self._table
        #return self.schema.getTable(self._table.getTableId())
    
    def zap(self):
        self._connection.executeZap(self._table)
        self.touch()



    def fireUpdate(self):
        pass
        #for ds in self._datasources:
        #    ds.onStoreUpdate()

    def createTable(self,sess):
        if self._status == self.SST_MUSTCHECK:
            sess.ui.debug("mustCheck " + self._table.name)
            if self._connection.mustCreateTables():
                #self.createTable(sess)
                sess.ui.debug("create table " + \
                              self._table.getTableName())
                self._connection.executeCreateTable(self._peekQuery)
                self._status = self.SST_VIRGIN
            self._table.loadMirror(self,sess)
                
    def populateOrNot(self,schema,sess,populator):
         if self._status == self.SST_VIRGIN:
             populator.populateStore(self,sess)
             #self._table.populate(sess)
         self._status = self.SST_READY
        
    def checkIntegrity(self,sess):
        if self._status != self.SST_MUSTCHECK:
            return
        if self._connection.mustCheckTables():
            q = self.query()
            l = len(q)
            job = sess.ui.job("Checking Table %s : %d rows" % \
                              q._table.getTableName(),
                              maxval=l)
            for row in q:
                job.inc()
                msg = row.checkIntegrity()
                if msg is not None:
                    msg = "%s[%s] : %s" % (
                        q._table.getTableName(),
                        str(row.getRowId()),
                        msg)
                    sess.ui.error(msg)
                    #msgs.append(msg)
            job.done()
            
        self._status = self.SST_READY
        
    def view(self,sess,viewName,columnNames=None,**kw):
        view = self._table.getView(viewName)
        if view is None:
            raise KeyError,viewName+": no such view"
            
        for k,v in view.items():
            kw.setdefault(k,v)
        kw['viewName'] = viewName
        if columnNames is not None:
            kw['columnNames'] = columnNames
        return self.query(sess,**kw)
        
            
    def createQuery(self,sess,columnNames=None,**kw):
        #return Query(self._peekQuery,self,sess,
        #             columnNames=columnNames,**kw)
        return Query(None,self,sess,columnNames,**kw)
        
    def lockRow(self,row,ds):
        k = tuple(row.getRowId())
        if self._lockedRows.has_key(k):
            raise RowLockFailed("Row is locked by another process")
        self._lockedRows[k] = ds

    def unlockRow(self,row,ds):
        k = tuple(row.getRowId())
        x = self._lockedRows.pop(k)
        assert x == ds
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
        for row in self._lockedRows:
            print "forced unlock:", row
            row.unlock()
##         #assert len(self._lockedRows) == 0
        
    def unlockDatasource(self,ds):
        for row in self._lockedRows:
            if row._ds == ds:
                print "forced unlock:", row
                row.unlock()
##         #print "Datasource.unlockAll()",self
##         for row in self._lockedRows:
##             if row._ds == ds:
##                 row.unlock()
    
        
                
        
        
    def removeFromCache(self,row):
        pass
    
    def addToCache(self,row):
        pass

    def commit(self):
        ""
        if len(self._lockedRows) > 0:
            raise InvalidRequestError("unlock first, then commit!")
##         for row in self._lockedRows:
##             row.writeToStore()
            
    def beforeShutdown(self):
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
                x[i] = self._connection.executeGetLastId(self._table,front)
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





class Populator(Describable):
    
    def populateStore(self,store,sess):
        name = "populate"+store.getTable().name
        try:
            m = getattr(self,name)
        except AttributeError:
            return
        qry=store.createQuery(sess,"*")
        m(qry)
    


