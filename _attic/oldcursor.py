class OldCursor:
   def __init__(self, conn, query):
      self.rowcount = None

      """
      Python Database API Specification v2.0
      http://www.python.org/peps/pep-0249.html
      
      rowcount
      
      This read-only attribute specifies the number of rows that
      the last executeXXX() produced (for DQL statements like
      'select') or affected (for DML statements like 'update' or
      'insert').
            
      The attribute is -1 in case no executeXXX() has been
      performed on the cursor or the rowcount of the last
      operation is not determinable by the interface. [7]
      
      Note: Future versions of the DB API specification could
      redefine the latter case to have the object return None
      instead of -1.

      """

      
      
      # ? self.row = None

      
      self.rownumber = None
      # rownumber None : no data 
      # rownumber -1 : before first fetchone()
      
      self._mustExecute = True

      # self.description = None # not supported
      # self.setupColumns()
      
   #def mustSetupColumns(self):
   #   self.columns = None

   def mustExecute(self):
      self._mustExecute = True

   def close(self):
      pass

   def lock(self):
      "lock the current row for update"
      pass
   
   def unlock(self):
      "unlock the current row. make changes visible to others"
      pass
   
##    def execute(self,query):
      
##       """modified from DBAPI. Does not accept a string, but a Query
##       instance"""
      
##       raise MustOverride()

   def fetchone(self):
      
      """modified from DBAPI. Does not return a tuple of values but a
      Row."""
      
      raise NotImplementedError
      
   def getCurrentRow(self):
      return self.row

      

##    def CreateRow(self,template=None):
##       self.row = self.query.CreateRow(template)
##       return self.row

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
   


##    def commit(self):
##       self.conn.commit_row(self,self.row)
      
##       for col in self.columns:
##          if isinstance(col,DetailColumn):
##             col.slaveCursor.commit()
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


##    def SetCellByExpr(self,colName,expr):
##       """
##       assign a value to a column in the current row
##       """
##       #if self.row == None:
##       #   raise LinoError("no current row")
##       try:
##          col = self.FindColumn(colName)
##       except KeyError,e:
##          raise LinoError(\
##                "(%s.%s) %s" % (self.query.GetName(),colName,e))
##       # col.SetByExpr(self.row,expr)
##       setattr(self.row,colName,col.expr2value(expr))
##       #self.trigger() # FireRowEvent("AfterSkip")


      

## class Column(EventManager):
##    """
   
##    a Column is the instance of a Component in a Cursor. Components are
##    rather static while Columns are rather dynamic. It is necessary to
##    instanciate something for each Component in each Cursor because
##    DetailColumn contains a Query.
   
##    """
##    def __init__(self,cursor,comp):
##       """
##       cursor : the one who contains me
##       comp : the one which i represent
##       """
##       EventManager.__init__(self,())
##       #self.cursor = cursor
##       self.cursor = cursor
##       self.comp = comp
      
##    def expr2value(self,expr):
##       raise MustOverride()

## ##    def SetValue(self,row,value):
## ##       raise MustOverride()

##    def __str__(self):
##       #return self.cursor.query.GetName()+"."+self.comp.name
##       return self.comp.name

## class FieldColumn(Column):
##    pass
      
##    def expr2value(self,expr):
## ##       # row.values[self.comp.name] =
##       return self.comp.type.expr2value(expr)
   
## ##    def SetValue(self,row,value):
## ##       setattr(row,self.comp.name,value)
      

## class PointerColumn(Column):

##    def __init__(self,cursor,comp):
##       assert isinstance(comp,Pointer)
##       Column.__init__(self,cursor,comp)

##       # self.joinComponents contains the non-primary foreign
##       # components to be included 
      
##    def addColumns(self,columnList):
##       l = []
##       for comp in self.comp.toTable.comps:
##          if not comp in self.comp.toTable.GetPrimaryKey():
##             #if ... joinBudget:
##             l.append(comp)
##       self.joinComponents = tuple(l)
##       self.joinQuery

      
      
      
##    #def SetByExpr(self,row,expr):
##    def expr2value(self,expr):
## ##       #row.values[self.comp.name] =
##       return self.comp.toTable.expr2row(expr)
   
## ##    def SetValue(self,row,value):
## ##       setattr(row,
## ##               self.comp.name,
## ##               apply(self.comp.toTable.Peek,value))

      
   
## class DetailColumn(Column):
   
##    def __init__(self,cursor,comp):
##       Column.__init__(self,cursor,comp)
##       #self.detail = comp # just an alias

##    def getCursor(self,columnList=None):
##       csr = gandalf.conn.getCursor(\
##                                 comp.slaveTable.getDefaultQuery())
##       self.slaveCursor.setMaster(cursor)
      

##    def BeforeSkip(self,masterRow):
##       pass
   
##    def AfterSkip(self,masterCursor):
##       #if not isinstance(masterRow,Cursor):
##       #   raise "masterRow is %s, must be QueryRow" % repr(masterRow)
##       self.slaveQuery.SetSlice(self.comp.pointerName,
##                                masterCursor.GetCurrentRow())
         
      
##    def expr2value(self,expr):
##       raise NotImplementedError
##       # cursor = self.slaveCursor.expr2cursor(expr)
## ##       # print "DetailColumn.expr2value(): " , rowlist
##       #return cursor

## ##    def SetValue(self,row,value):
## ##       setattr(row,
## ##               self.comp.name,
## ##               self.expr2value(value))


## ## class DetailAdapter:
## ##    def __init__(self,detail):
## ##       self.detail = detail
## ##       self.slaveCursor = Query(detail.slaveTable,
## ##                                cursor.query.depth-1).GetCursor()
## ##       cursor.add_listener(self.SetupSlaveQuery)

## ##    def SetupSlaveQuery(self,event=None):
## ##       self.slaveCursor.query.SetSlice(self.detail.joinName,
## ##                                       self.cursor.row)
         


