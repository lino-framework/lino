import time
import sys, os


class Reporter:
   def __init__(self,parent=None):
      """
      
      parent can be another Report from whom this instance inherits
      some parameters.
      """
      
      self.groups = []
      self.totals = []
      self.recno = None
      self.colSep = "\t"
      self.indent = 0
      self.parent = parent
      if parent is not None:
         assert isinstance(parent,Reporter)
         # self.conn = parent.conn
         # self.writer = parent.writer
   
   def connect(self,conn):
      """
      connect using an existing connection.
      """
      self._conn = conn

   def initialize(self,sql):
      conn = self.getConnection()
      assert conn is not None, "use connect() before initialize()"
      self.csr = conn.cursor()
      self.csr.execute(sql)
      
      self.columns = []
      
      self.currentRow = None
      i = 0
      for coldesc in self.csr.description:
         self.columns.append(IndexedColumn(self,i))
         i += 1

   def addColumn(self,name,type,func):
      """use this to add your own computed columns"""
      self.columns.append(ComputedColumn(self,name,type,func))

   def execute(self,writer=None):
      assert hasattr(self,"columns"), "use initialize() before execute()"
      if writer is None:
         if self.parent is None:
            self._writer = SimpleWriter()
      else:
         self._writer = writer
         
      self.recno = 0
      
      while 1:
         row = self.csr.fetchone()
         if not row: break
         if self.recno == 0:
            self.onHeader()
         self.recno += 1
         self.currentRow = Row()
         for col in self.columns:
            setattr(self.currentRow,col.name,col.fetch(row))
         self.onEachRow()
         
      self.onFooter()

   def close(self):
      if self.parent is None:
         self._writer.close()


   def write(self,txt):
      if self.parent is None:
         self._writer.write(txt)
      else:
         self.parent.write(txt)


   def getConnection(self):
      if self.parent is None:
         return self._conn
      return self.parent.getConnection()
      


   def onHeader(self):
      
      """prints a header line. May be overridden."""
      
      colnames = []
      for col in self.columns:
         colnames.append(col.name)
      self.write(self.colSep * self.indent)
      self.write("\t".join(colnames))
      self.write(os.linesep)
      
   def onFooter(self):
      pass
   
   def onEachRow(self):
      
      """Prints the current row. May be overridden. Executed on each
      row."""
      
      a = []
      for col in self.columns:
         v = getattr(self.currentRow,col.name)
         a.append(col.format(v))
      self.write(self.colSep * self.indent)
      self.write(self.colSep.join(a))
      self.write(os.linesep)
      


def date2sql(secs):
   
   """converts a timestamp to the representation for dates required by
   ODBC driver, that is here month/day/year
   
   (year,month,day,hour,...) """
   
   tup = time.localtime(secs)
   return str(tup[1]) + "/" + str(tup[2])+ "/" + str(tup[0])

def date2out(secs):
   return time.strftime("%Y-%m-%d",time.localtime(secs))


class Row:

   def __init__(self):
      # self.__dict__["_rpt"] = rpt
      self.__dict__["_values"] = {}

   def __getitem__(self,name):
      "for accessing the row as a dict"
      #return repr(i)+"?"
      #name = self.__dict__["_rpt"].columns[i].name
      return self.__dict__["_values"][name]
      
   def __getattr__(self,name):
      try:
         return self.__dict__["_values"][name]
         #return self._values[name]
      except KeyError,e:
         s = "this row has no attribute '%s'" % name
         raise AttributeError,s
   
   def __setattr__(self,name,value):
      self.__dict__["_values"][name] = value

   def __repr__(self):
      if True: # hide None values
         s = ""
         sep = ""
         for (k,v) in self.__dict__["_values"].items():
            if not v is None:
               s += sep + "%s=%s" % (k,repr(v))
               sep = ", "
               
         return "row %s" % s 
      # show all values, including None
      return "row %s" % repr(self.__dict__["_values"])
   


class Column:
   def __init__(self,rpt,name,type):
      self.rpt = rpt
      self.name = name
      self.type = type
      if type == "DATE":
         self.formatter = date2out
      else:
         self.formatter = lambda x : str(x)
         
   def fetch(self,tupleRow):
      raise MustOverride

   def format(self,value):
      if value is None:
         return ""
      return self.formatter(value)

      
class IndexedColumn(Column):
   def __init__(self,rpt,index):
      Column.__init__(self,rpt,
                      rpt.csr.description[index][0],
                      rpt.csr.description[index][1]
                      )
      self.index = index

   def fetch(self,row):
      v = row[self.index]
      if v is None:
         if self.type == "DATE":
            return None
         elif self.type == "NUMBER":
            return 0
         elif self.type == "STRING":
            return ''
         else:
            raise "%s : unsupported type" % self.type
      return v
   

class ComputedColumn(Column):      
   def __init__(self,rpt,name,type,func):
      Column.__init__(self,rpt,name,type)
      self.func = func


   def fetch(self,row):
      try:
         return self.func(self.rpt.currentRow)
      except AttributeError,e:
         print self.rpt.currentRow
         raise # return e
   

   
