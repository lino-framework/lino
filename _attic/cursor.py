import lino
from lino.tools import *
from gandalf.table import Field, Join, Detail

raise "no longer used"

# see http://www.python.org/peps/pep-0249.html


class Cursor(EventManager):
   """
   
   A Cursor is an iterator over the result of a Query.  It can move
   through the rows of the result one by one, maintaining a current
   row.
   
   """
   
   def __init__(self, conn, query):
      """
      conn : the connection to use
      query : the view to use.
      
      """
      EventManager.__init__(self,("AfterSkip","BeforeSkip"))
      
      self.conn = conn
      self.master = None
      
      self.columns = None
      self.rowcount = None 
      self.row = None
      self.rownumber = None
      # rownumber None : no data
      # rownumber -1 : before first fetchone()
      
      self.query = query
      self._mustExecute = True

      # self.description = None # not supported
      # self.setupColumns()
      
   def setupColumns(self, columnList=None, budget=None):
      "Instantiate Column objects in self.columns (if not yet done)"
      
      """ if budget is specified, it must be an integer. It will
      override the default columnList of the query.  """

      self.columns = []
      if budget != None:
         # decide column list automagically using the budget
         for comp in self.query.leadTable.comps:
            price = comp.GetPrice() 
            if price <= budget:
               #if comp.GetVolume() <= space:
               self.columns.append(self.CreateColumn(comp))
               budget -= comp.price
               #space -= comp.GetVolume()
               # comp.SetupCursor(self)
      elif self.query.columnList != None:
         # if the query has an explicit column list
         for name in self.query.columnList.split():
            comp = self.query.leadTable.FindComponent(name)
            self.columns.append(self.CreateColumn(comp))
      else:
         for comp in self.query.leadTable.comps:
            if comp.isDefaultColumn:
               self.columns.append(self.CreateColumn(comp))
         

      #self.trigger("Setup")

   def setMaster(self,master):
      """
      master : another Cursor who acts as my master. It means that I
      am instanciated in a DetailColumn of my master.
      """
      self.master = master

   #def mustSetupColumns(self):
   #   self.columns = None

   def mustExecute(self):
      self._mustExecute = True


   def CreateColumn(self,comp):
      """
      a Query has "bought" the Column from this Component
      """
      if isinstance(comp,Field):
         return FieldColumn(self,comp)
      elif isinstance(comp,Join):
         return JoinColumn(self,comp)
      elif isinstance(comp,Detail):
         return DetailColumn(self,comp)
      
      raise MustOverride()
   
   def FindColumn(self,name):
      if self.columns is None:
         self.setupColumns()
      for col in self.columns:
         if col.comp.name == name:
            return col
      raise "%s : no such column in %s\nmust be one of %s" % (\
         name,
         str(self.query.GetName()),
         map(str,self.columns)
         )
   
   def close(self):
      pass

   def lock(self):
      "lock the current row for update"
      pass
   
   def unlock(self):
      "unlock the current row. make changes visible to others"
      pass

   def executeSelect(self):
      raise MustOverride

   def executeCount(self):
      raise MustOverride

##    def execute(self,query):
      
##       """modified from DBAPI. Does not accept a string, but a Query
##       instance"""
      
##       raise MustOverride()

   def fetchone(self):
      
      """modified from DBAPI. Does not return a tuple of values but a
      Row."""
      
      raise MustOverride()
      
   def __str__(self):
      sep = ""
      s = self.query.GetName() + " cursor"
##       s += "row=("
##       for comp in self.query.leadTable.comps:
##          value = getattr(self.row,comp.name)
##          if value != None:
##             s += sep + comp.name + "=" + str(value)
##          sep = ","
##       s += ")"   
      return s

         
   def getCurrentRow(self):
      return self.row

      

##    def CreateRow(self,template=None):
##       self.row = self.query.CreateRow(template)
##       return self.row

   def trigger_BeforeSkip(self):
      if self.row is None:
         return 
      if self.row.IsDirty():
         self.trigger("BeforeSkip")
         self.commit()
   
   def appendRow(self,*args,**keywords):
      if self.columns is None:
         self.setupColumns()
      else:
         self.trigger_BeforeSkip()
      self.row = Row(self.query.leadTable,new=True)
      self.query.onAppend(self.row)
      i = 0
      for arg in args:
         if arg != None:
            col = self.columns[i]
            setattr(self.row,col.comp.name,arg)
            # col.SetValue(self.row,arg)
            #value = col.expr2value(arg)
            #self.row.values[col.comp.name] = value
         i += 1
      for (name,expr) in keywords.items():
         try:
            col = self.FindColumn(name)
            setattr(self.row,col.comp.name,expr)
            #col.SetValue(self.row,expr)
            #self.row.values[name] = col.expr2value(expr)
         except KeyError:
            raise LinoError("%s : no such component in %s" %
                            (name,
                             self.GetName()))

      self.trigger("AfterSkip")
      #self.commit_row()
      
   def appendAsCopy(self,row):
      if self.columns is None:
         self.setupColumns()
      else:
         self.trigger_BeforeSkip()
      self.row = Row(self.query.leadTable,new=True)
      self.query.onAppend(row)
      for col in self.columns:
         if col.comp.sticky:
            setattr(self.row,col.comp.name,
                    getattr(row,col.comp.name))
      self.trigger("AfterSkip")
      #self.commit_row()

   def commit(self):
      self.conn.commit_row(self,self.row)
      
      for col in self.columns:
         if isinstance(col,DetailColumn):
            col.slaveCursor.commit()
##             # the value of a detail is a list of rows
##             detailRowList = getattr(self.row,col.comp.name)
##             if detailRowList != None:
##                #try:
##                   #slaveQuery = query.columns[comp.name].slaveQuery
##                   slaveCursor = self.conn.getCursor(col.slaveQuery)
##                   for detailRow in detailRowList:
##                      slaveCursor.row = detailRow
##                      slaveCursor.commit()
##                      #self.commit_row(slaveCursor,detailRow)
##                #except Exception,e:
##                #   raise LinoError(str(col)+": "+str(e))
            
            

##    def commit_row(self,row):
##       return self.ds.commit_row(self,row)


   def SetCellByExpr(self,colName,expr):
      """
      assign a value to a column in the current row
      """
      #if self.row == None:
      #   raise LinoError("no current row")
      try:
         col = self.FindColumn(colName)
      except KeyError,e:
         raise LinoError(\
               "(%s.%s) %s" % (self.query.GetName(),colName,e))
      # col.SetByExpr(self.row,expr)
      setattr(self.row,colName,col.expr2value(expr))
      #self.trigger() # FireRowEvent("AfterSkip")

   def __iter__(self):
      if self.columns is None:
         self.setupColumns()
      if self._mustExecute:
         self.executeSelect()
      else:
         self.rownumber = -1
      return self

   def next(self):
      if self._mustExecute:
         raise "data changed during iteration"
      row = self.fetchone()
      if row is None:
         raise StopIteration
      return row

   def __len__(self):
      if self.rowcount is None:
         self.executeCount()
      return self.rowcount
   

      

class Column(EventManager):
   """
   
   a Column is the instance of a Component in a Cursor. Components are
   rather static while Columns are rather dynamic. It is necessary to
   instanciate something for each Component in each Cursor because
   DetailColumn contains a Query.
   
   """
   def __init__(self,cursor,comp):
      """
      cursor : the one who contains me
      comp : the one which i represent
      """
      EventManager.__init__(self,())
      #self.cursor = cursor
      self.cursor = cursor
      self.comp = comp
      
   def expr2value(self,expr):
      raise MustOverride()

##    def SetValue(self,row,value):
##       raise MustOverride()

   def __str__(self):
      #return self.cursor.query.GetName()+"."+self.comp.name
      return self.comp.name

class FieldColumn(Column):
   pass
      
   def expr2value(self,expr):
##       # row.values[self.comp.name] =
      return self.comp.type.expr2value(expr)
   
##    def SetValue(self,row,value):
##       setattr(row,self.comp.name,value)
      

class JoinColumn(Column):

   def __init__(self,cursor,comp,joinBudget=None):
      Column.__init__(self,cursor,comp)

      # self.joinComponents contains the non-primary foreign
      # components to be included 
      
      l = []
      for comp in self.comp.toTable.comps:
         if not comp in self.comp.toTable.GetPrimaryKey():
            #if ... joinBudget:
            l.append(comp)
      self.joinComponents = tuple(l)
      
      
   #def SetByExpr(self,row,expr):
   def expr2value(self,expr):
##       #row.values[self.comp.name] =
      return self.comp.toTable.expr2row(expr)
   
##    def SetValue(self,row,value):
##       setattr(row,
##               self.comp.name,
##               apply(self.comp.toTable.Peek,value))

      
   
class DetailColumn(Column):
   
   def __init__(self,cursor,comp):
      Column.__init__(self,cursor,comp)
      #self.detail = comp # just an alias
      self.slaveCursor = lino.conn.getCursor(\
                                comp.slaveTable.getDefaultQuery())
      self.slaveCursor.setMaster(cursor)



   def BeforeSkip(self,masterRow):
      pass
   
   def AfterSkip(self,masterCursor):
      #if not isinstance(masterRow,Cursor):
      #   raise "masterRow is %s, must be QueryRow" % repr(masterRow)
      self.slaveQuery.SetSlice(self.comp.joinName,
                               masterCursor.GetCurrentRow())
         
      
   def expr2value(self,expr):
      raise "NotImplemented"
      # cursor = self.slaveCursor.expr2cursor(expr)
##       # print "DetailColumn.expr2value(): " , rowlist
      #return cursor

##    def SetValue(self,row,value):
##       setattr(row,
##               self.comp.name,
##               self.expr2value(value))


## class DetailAdapter:
##    def __init__(self,detail):
##       self.detail = detail
##       self.slaveCursor = Query(detail.slaveTable,
##                                cursor.query.depth-1).GetCursor()
##       cursor.add_listener(self.SetupSlaveQuery)

##    def SetupSlaveQuery(self,event=None):
##       self.slaveCursor.query.SetSlice(self.detail.joinName,
##                                       self.cursor.row)
         



class Row:

   def __init__(self,table,
                new=False,
                uncomplete=False,
                locked=False):
      self.__dict__["_values"] = {}
      self.__dict__["_dirty"] = False
      self.__dict__["_new"] = new
      self.__dict__["_locked"] = locked
      self.__dict__["_uncomplete"] = uncomplete
      self.__dict__["_table"] = table

   def SetDirty(self,dirty=True):
      self.__dict__["_dirty"] = dirty

   def SetNew(self,new):
      self.__dict__["_new"] = new

   def IsDirty(self):
      return self._dirty
   
   def IsNew(self):
      return self._new

   def __getattr__(self,name):
      try:
         return self.__dict__["_values"][name]
         #return self._values[name]
      except KeyError,e:
         s = "%s row has no attribute '%s'" % (self._table.name,
                                             name)
         raise AttributeError,s
   
   def __setattr__(self,name,value):
      comp = self._table.FindComponent(name)

      if value is not None:
         if isinstance(comp,Field):
            pass
         elif isinstance(comp,Join):
            if not isinstance(value,Row):
               raise "cannot assign %s to column %s" % \
                     ( repr(value), name )
         elif isinstance(comp,Detail):
            if not isinstance(value,Cursor):
               raise "cannot assign %s to column %s" % \
                     ( repr(value), name )
      
      
      #self.__dict__["_values"][name] = comp.assign(value)
      self.__dict__["_values"][name] = value
      self.__dict__["_dirty"] = True
      #self.SetDirty()

   def __repr__(self):
      if True: # hide None values
         s = ""
         sep = ""
         for (k,v) in self.__dict__["_values"].items():
            if not v is None:
               s += sep + "%s=%s" % (k,repr(v))
               sep = ", "
               
         return "row %s" % s #self.__dict__["_values"]
      # show all values, including None
      return "row %s" % repr(self.__dict__["_values"])
   

