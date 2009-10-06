# is it possible to model the dictionary using only classes who
# represent a row?

from lino.adamo.table import Table,LinkTable
from lino.adamo.type import *
from lino.plugins import babel

class DataVeto(Exception):
   pass

class Field:
   def __init__(self,type):
      self.type = type
      
class Pointer:
   def __init__(self,toTable):
      self.toTable = type
      

class Table:
   def __init__(self,name,rowClass):
      self.name = name
      self.rowClass = rowClass

class Row:
   def __init__(self,**kw):
      self._values = {}
      for (k,v) in kw:
         self._values[k] = v
      

class Contact(Row):
   name = Field(STRING)
   email = Field(STRING)
   phone = Field(STRING)
   
   def getRowName(self):
      return self.name

class Organisation(Contact):
   id = Field(ROWID)

   
   
class Person(Contact):
   id = Field(ROWID)
   fname = Field(STRING)
   title = Field(STRING)

   def getRowName(self):
      return self.fname+" "+self.name
      
   def validate(self):
      if (self.fname is None) and (self.name is None):
         raise DataVeto("Either name or fname must be specified")
   

p1 = Person(fname="Luc",name="Saffre")

