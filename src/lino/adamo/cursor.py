import new
from lino.adamo.row import WritableRow
from lino.adamo.table import Field, Pointer, Detail
from lino.misc.etc import EventManager

# see http://www.python.org/peps/pep-0249.html


class CursorMixin(EventManager):
   """
   
   A Cursor is an iterator over the result of a Query.  It can move
   through the rows of the result one by one, maintaining a current
   row.

   Unlike the DBAPI cursor, Lino Cursors correspond to
   data-retrieving queries (SELECT).
   
   """
   
   def __init__(self, conn, query):
      """
      conn : the connection to use
      query : the view to use.
      
      """
      EventManager.__init__(self,("AfterSkip","BeforeSkip"))
      
      self.conn = conn
      self.query = query
      
      self.master = None

      
      #self.columns = None

##    def setupColumns(self, columnList=None): #, budget=None):
##       "Instantiate Column objects in self.columns (if not yet done)"
      
##       """ if budget is specified, it must be an integer. It will
##       override the default columnList of the query.  """

##       self.columns = []
## ##       if budget != None:
## ##          # decide column list automagically using the budget
## ##          for comp in self.query.leadTable.comps:
## ##             price = comp.GetPrice() 
## ##             if price <= budget:
## ##                #if comp.GetVolume() <= space:
## ##                self.columns.append(self.CreateColumn(comp))
## ##                budget -= comp.price
## ##                #space -= comp.GetVolume()
## ##                # comp.SetupCursor(self)
## ##       elif self.query.columnList != None:
##          # if the query has an explicit column list
##       if columnList is None:
##          columnList = self.query.columnList
##       for name in columnList:
##          comp = self.query.leadTable.findComponent(name)
##          self.columns.append(self.CreateColumn(comp))

##       #self.trigger("Setup")

   def appendRow(self,*args):
      assert len(args) == len(self.query.getColumns()), \
             "%d values given, but %d values expected" % \
             (len(args),len(self.query.getColumns()))
      i = 0
      d = {}
      for col in self.query.getColumns():
         d[col.getName()] = args[i]
         i += 1
      return self.query.leadTable.appendRow(d)
         

   def setMaster(self,master):
      
      """master : another Cursor who acts as my master. It means that
      this Cursor is instanciated in a DetailColumn of my master."""

      self.master = master


##    def CreateColumn(self,comp):
##       """
##       a Query has "bought" the Column from this Component
##       """
##       if isinstance(comp,Field):
##          return FieldColumn(self,comp)
##       elif isinstance(comp,Pointer):
##          return PointerColumn(self,comp)
##       elif isinstance(comp,Detail):
##          return DetailColumn(self,comp)
      
##       raise "cannot create Column from " + comp.__class__ 
   

   def executeSelect(self):
      raise NotImplementedError

   def executeCount(self):
      raise NotImplementedError

   def __len__(self):
      self.executeCount()
      return len(self.getCursor())
   
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

         
##    def trigger_BeforeSkip(self):
##       if self.row is None:
##          return 
##       if self.row.IsDirty():
##          self.trigger("BeforeSkip")
##          self.commit()
   
