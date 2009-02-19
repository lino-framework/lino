"""
cPickle should be replaced some day by a less limited "pickler"...
http://www.egenix.com/files/python/mxBeeBase.html

"""


from warnings import warn

import os.path
from cPickle import load, dump

from lino.dbd import abstract
# from lino.dbd import cursor
import lino.table
from lino.tools import *
#from lino.query import FieldColumn, JoinColumn, DetailColumn
#from lino.dbd.abstract import Row
from lino.table import Field, Join, Detail

class Cursor(abstract.Cursor):
   def __init__(self,conn,query):
      abstract.Cursor.__init__(self,conn,query)
      self.ut = conn.GetUsedTable(query.leadTable)
      self.ut.add_listener(self)
      self.rows = None
      #self.list = self.data.keys()
      #raise NotImplemented


   def executeSelect(self):
      if self.columns is None:
         self.setupColumns()
      self.rows = []
      for values in self.ut.data:
         row = self.ut.data2row(values)
         if self.query.RowIsVisible(row):
            self.rows.append(row)

      self.rowcount = len(self.rows)
      self.rownumber = -1
      self._mustExecute = False
      
   def executeCount(self):
      if self.columns is None:
         self.setupColumns()
      # self.rownumber = -1
      self.rowcount = 0
      self.rows = None
      for values in self.ut.data:
         row = self.ut.data2row(values)
         if self.query.RowIsVisible(row):
            self.rowcount += 1



   def close(self):
      self.trigger_BeforeSkip()
      self.ut.commit()
      self.ut.remove_listener(self)
      del self.ut

##    def _getrow(self):
##       try:
##          (keys,values) = self.iter.next()
##       except StopIteration:
##          return None
##       row = self.query.CreateRow()
##       i = 0
##       pk = self.query.leadTable.GetPrimaryKey()
##       for comp in pk:
##          if isinstance(comp,FieldColumn):
##             setattr(row,comp.name,keys[i])
##             i += 1
##          elif isinstance(comp,JoinColumn):
##             jrow = QueryRow()
##             for jpk in comp.join.toTable.GetPrimaryKey():
##                setattr(jrow,jpk.name,keys[i])
##                i += 1
##             setattr(row,comp.name,jrow)
            
##       i = 0
##       for comp in self.query.leadTable.comps:
##          if not comp.name in pk:
##             if isinstance(comp,FieldColumn):
##                setattr(row,comp.name,values[i])
##                i += 1
##             elif isinstance(comp,JoinColumn):
##                jrow = QueryRow()
##                for jpk in comp.join.toTable.GetPrimaryKey():
##                   setattr(jrow,jpk.name,keys[i])
##                   i += 1
##                setattr(row,comp.name,jrow)
##       return row
            

   def fetchone(self):
      assert self.rownumber is not None
      self.trigger_BeforeSkip()
      self.rownumber += 1
      if self.rownumber < len(self.rows):
         self.row = self.rows[self.rownumber]
      else:
         self.row = None
      self.trigger("AfterSkip")
      return self.row
   
   
                                            
      

class Connection(abstract.Connection):
   def __init__(self,basePath="."):
      self.basePath = basePath
      
      self._usedTables = {}
      
   def GetUsedTable(self,table):
      try:
         return self._usedTables[table.name]
      except KeyError:
         ut = UsedTable(self.basePath,table)
         self._usedTables[table.name] = ut
         return ut
      
      
   def create_table(self,table):
      ut = self.GetUsedTable(table)
      ut.data = []
      ut.SetDirty()

   def executeInsert(self,cursor,row):
      cursor.ut.executeInsert(row)
      
   def executeUpdate(self,cursor,row):
      cursor.ut.executeUpdate(row)
      #cursor.commit()

##    def row2data(self,cursor,row):
##       keys = []
##       values = []

##       pk = cursor.query.leadTable.GetPrimaryKey()
##       for comp in pk:
##          keys.append(getattr(row,comp.name))
##       for comp in cursor.query.leadTable.comps:
##          if not comp.name in pk:
##             if isinstance(comp,FieldColumn):
##                values.append(getattr(row,comp.name))
##             elif isinstance(comp,JoinColumn):
##                for pk in comp.join.toTable.GetPrimaryKey():
##                   irow = getattr(row,comp.name)
##                   values.append(getattr(irow,pk.name))
                  
      
##       return (tuple(keys),tuple(values))
      
##       for col in cursor.query.columns:
##          if isinstance(comp,DetailColumn):
##             # the value of a detail is a list of rows
##             detailRowList = getattr(row,col.comp.name)
##             if detailRowList != None:
##                slaveQuery = col.slaveQuery
##                slaveCursor = slaveQuery.cursor()
##                for detailRow in detailRowList:
##                   slaveCursor.commit_row(detailRow)
      
   def getCursor(self,query):
      return Cursor(self,query)

   def close(self):
      for ut in self._usedTables.values():
         ut.commit()

   

class Index:
   def __init__(self,table,compList):
      a = []
      i = 0      
      for comp in table.comps:
         if comp in compList:
            a.append(i)
         i += 1
      self._rowindexes = tuple(a)
      #print self._rowindexes
      self.dict = {}
      self._table = table # debug only
         
   def setRecnoForRow(self,recno,values):
      a = []
      for i in self._rowindexes:
         a.append(values[i])
      self.dict[tuple(a)] = recno

   def GetName(self):
      return self._table.GetName()+"1.ntx"

   def findRowIndex(self,values):
      a = []
      for i in self._rowindexes:
         try:
            a.append(values[i])
         except IndexError,e:
            raise "%s : invalid row for %s" % (repr(values),
                                               self.GetName())
      key = tuple(a)
      try:
         return self.dict[key]
      except KeyError,e:
         return -1
         #raise "%s : no such key in %s" % (repr(key),self.GetName())
         
      

      

class UsedTable(EventManager):
   def __init__(self,basePath,table):
      EventManager.__init__(self,())
      self.table = table
      self.filename = os.path.join(basePath,table.name)+".db"
      self._dirty = False
      self._index = Index(table,table.GetPrimaryKey())
      try:
         f = open(self.filename,"rb")
         self.data = load(f)
         recno = 0
         for values in self.data:
            #warn(repr(values))
            self._index.setRecnoForRow(recno,values)
            recno += 1
         #print "%s : %d rows" % (self.filename,recno)
      except IOError,e:
         self.data = {}
      #self.add_listener(cursor)

   def SetDirty(self,dirty=True):
      self._dirty = dirty

   def commit(self):
      if self._dirty:
         f = open(self.filename,"wb")
         dump(self.data,f,True)

   def data2row(self,values):
      row = abstract.Row(self.table)
      i = 0
      for comp in self.table.comps:
         if isinstance(comp,Field):
            try:
               setattr(row,comp.name,values[i])
            except IndexError,e:
               raise "%s : bad data for %s" % (repr(values),
                                             self.table.GetName())
            i += 1
         elif isinstance(comp,Join):
            jrow = cursor.Row(comp.toTable)
            for jpk in comp.toTable.GetPrimaryKey():
               setattr(jrow,jpk.name,values[i])
               i += 1
            setattr(row,comp.name,jrow)
         elif isinstance(comp,Detail):
            detailCursor = comp.slaveTable.getCursor()
            setattr(row,comp.name,detailCursor)
      row.SetDirty(False)
      return row

   def row2data(self,row):
      values = []
         
      for comp in self.table.comps:
         if isinstance(comp,Field):
            values.append(getattr(row,comp.name))
         elif isinstance(comp,Join):
            jrow = getattr(row,comp.name)
            if jrow is None:
               for pk in comp.toTable.GetPrimaryKey():
                  values.append(None)
            else:
               for pk in comp.toTable.GetPrimaryKey():
                  values.append(getattr(jrow,pk.name))
##       if self.table.name == "PERSONS":
##          print "row2data() : %s => %s" % (repr(row),
##                                           repr(tuple(values)))
      return tuple(values)
   

   def executeUpdate(self,row):
      values = self.row2data(row)
      i = self._index.findRowIndex(values)
      self.data[i] = values
      self.SetDirty()
      
   def executeInsert(self,row):
      values = self.row2data(row)
      i = self._index.findRowIndex(values)
      if i != -1:
         raise LinoError("cannot insert %s into %s: key exists" % (
            str(row),
            str(self.table)            
            ))
      self.data.append(values)
      self._index.setRecnoForRow(len(self.data)-1,values)
      self.SetDirty()
      #cursor.commit()
         
