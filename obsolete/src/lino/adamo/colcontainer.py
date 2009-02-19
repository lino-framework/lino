raise "not used"
from new import classobj

class Atom:
   def __init__(self,name,type,prefix,index):
      self.name = name
      self.type = type
      if prefix != name:
         self.prefix = prefix
      else:
         self.prefix = None
      self.index = index

   def getValue(self,row):
      for subname in self.name.split("_"):
         row = getattr(row,subname)
      return row

   def getName(self):
      if self.prefix is None:
         return self.name
      return self.prefix+'.'+self.name

##    def __str__(self):
##       s = self.name
##       if self.alias is not None:
##          s += " AS " + self.alias
##       return s
      
      
class ColumnContainer:
   """Base class for Tables and Queries
   """
   def __init__(self,rowBase):
      # self._rowMethods = {}

      
   
##    def findColumn(self,name):
##       for col in self._columns:
##          if col.name == name:
##             return col
##       raise "%s : no such column in %s\nmust be one of %s" % (\
##          name,
##          str(self.getName()),
##          map(str,self._columns))
   

##    def findColIndex(self,name):
##       i = 0
##       for col in self._columns:
##          if col.getName() == name:
##             return i
##          i += 1
##       raise "%s : no such column in %s\nmust be one of %s" % (\
##          name,
##          str(self.getName()),
##          map(str,self._columns))


##    def atoms2row(self,atomicRow):
##       "doesn't work (?)"
##       l = []
##       for col in self.getColumns():
##          e = []
##          for atom in col.getAtoms():
##             e.append(atomicRow[atom.index])
##          if len(e) == 1:
##             l.append(e[0])
##          else:
##             l.append(tuple(e))
##       return tuple(l)
      


