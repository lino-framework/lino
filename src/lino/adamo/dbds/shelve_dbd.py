import os.path
import shelve

import dbd
import datadict

shelves = {}


class Result:
   def __init__(self,cursor,ds):
      self.ds = ds
      self.cursor = cursor
      try:
         self.shelf = shelves[cursor.query.leader.name]
      except KeyError:
         filename = self.ds.tablefilename(cursor.query.leader)
         self.shelf = shelve.open(filename,"w")
         shelves[cursor.query.leader.name] = self.shelf
      self.list = self.shelf.keys()
      
##    def fetch_row(self):
##       return self.shelf[str(row.values["id"])]

   def commit(self):
      self.shelf.sync()

   def fetchone(self):
      self.trigger("BeforeSkip")
      if self.recno == -1:
         self.recno = 0
      if self.recno+1 > len(self.list):
         self.recno = -1
         self.row = None
      else:
         self.row = self.shelf[self.list[self.recno]]
      self.trigger("AfterSkip")
      return self.row
   
   
                                            
      

class Datasource(dbd.Datasource):
   def __init__(self,basePath="."):
      self.basePath = basePath
      
   def tablefilename(self,table):
      return os.path.join(self.basePath,table.name)+".db"

      
   def create_table(self,table):
      d = shelve.open(self.tablefilename(table),"n")
      #d = self.open_table(query.leader)
      assert len(d) == 0
      d.close()

   def commit_row(self,cursor,row):
      cursor.shelf[str(row.id)] = row._values
      
   def GetCursor(self,query):
      return Cursor(query,self)
      
