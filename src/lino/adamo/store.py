## Copyright Luc Saffre 2003-2005.

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

from lino.adamo import DataVeto
#from datasource import Datasource
from query import DataColumnList

class Store:
    """
    One instance per Database and Table.
    Distributes auto-incrementing keys for new rows.
    """

    SST_MUSTCHECK = 1
    SST_VIRGIN = 2 # must populate with default data?
    SST_READY = 3
    
    def __init__(self,conn,db,table):
        self._connection = conn # shortcut
        self._mtime = conn.getModificationTime(table)
        self._db = db
        self._table = table
        self._schema = db.schema # shortcut
        self._lockedRows = []
        self._status = self.SST_MUSTCHECK
        
        self._datasources = []
        
        if len(self._table.getPrimaryAtoms()) == 1:
            self._lastId = None
        else:
            self._lastId = {}

        #self._queries = {}
        #self._peekQuery = self.defineQuery(None)
        self._peekQuery = DataColumnList(self,db)
        self._table.onConnect(self)


    def mtime(self):
        return self._mtime

    def touch(self):
        self._mtime = time()
    
    def getTable(self):
        return self._table
        #return self.schema.getTable(self._table.getTableId())
    
    def zap(self):
        self._connection.executeZap(self._table)
        self.touch()


    def registerDatasource(self,ds):
        self._datasources.append(ds)

    def fireUpdate(self):
        for ds in self._datasources:
            ds.onStoreUpdate()

    def createTables(self,sess):
        if self._status == self.SST_MUSTCHECK:
            if self._connection.mustCreateTables():
                self.createTable(sess)
                self._status = self.SST_VIRGIN
                
    def checkIntegrity(self,sess):
        if self._status == self.SST_MUSTCHECK:
            if self._connection.mustCheckTables():
                self.checkTable(sess)
            self._status = self.SST_READY
                
    def populate(self,sess):
         if self._status == self.SST_VIRGIN:
             self._table.populate(sess)
         self._status = self.SST_READY
        
            

    def checkTable(self,sess):
        q = sess.query(self._table)
        l = len(q)
        sess.progress("%s : %d rows" % ( q._table.getTableName(),l))
        for row in q:
            msg = row.checkIntegrity()
            if msg is not None:
                msg = "%s[%s] : %s" % (
                    q._table.getTableName(),
                    str(row.getRowId()),
                    msg)
                sess.error(msg)
                #msgs.append(msg)

        
        
    def removeFromCache(self,row):
        pass
    
    def addToCache(self,row):
        pass

    def beforeCommit(self):
        #assert len(self._lockedRows) == 0
        for row in self._lockedRows:
            row.writeToStore()
        
    def beforeShutdown(self):
        assert len(self._lockedRows) == 0
##      for row in self._dirtyRows.values():
##          row.commit()
##      self._dirtyRows = {}
    
    def createTable(self,sess):
        sess.progress( "create table " + self._table.getTableName())
        self._connection.executeCreateTable(self._peekQuery)
        #self._table.populate(self)

        

    def lockRow(self,row):
        # todo: use getLock() / releaseLock()
        self.removeFromCache(row)
        self._lockedRows.append(row)
        
    def unlockRow(self,row):
        self.addToCache(row)
        self._lockedRows.remove(row)
        self.touch()
        #row.writeToStore()
        #if row.isDirty():
        #   key = tuple(row.getRowId())
        #   self._dirtyRows[key] = row

    def unlockall(self):
        for row in self._lockedRows:
            row.unlock()
        assert len(self._lockedRows) == 0
    

    def setAutoRowId(self,row):
        "get auto-incremented row id"
        autoIncCol = self._peekQuery._pkColumns[-1]
        #assert isinstance(autoIncCol.rowAttr.type,AutoIncType)
        assert len(autoIncCol._atoms) == 1
        autoIncAtom = autoIncCol._atoms[0]
        
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





