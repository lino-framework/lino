"""

Application

A normal application will have a single instance of Application::

  app = lino.Application()
  app.loadPlugin("lino.plugins.system")
  app.loadPlugin("...")
  app.startup()
  app.connect(...)

  app.startMainLoop()

A plugin can be any Python module which provides a install() method
which takes the application object as parameter.

I cannot currently imagine any situation where subclassing would be
useful.

The initialization process is always the same and will probably one
day become more encapsulated: using an application config file with
the list of plugins and connections. (This now becomes very similar to
the GNUe common part...)

"""

raise "No longer used"

import sys

from lino.tools import *
from lino.table import Table


## class Plugin(SubSingleton):
   
   
##    def init(self):
##       "override this method to add Tables to your Plugin"
##       pass

##    def link(self):
##       "override this method to add links from your Plugin to others"
##       pass

##    def _declare(self,app,name):
##       self.app = app
##       self.name = name
      
##    def AddTable(self,name,table):
##       # sys.stderr.write("Declare table %s...\n" % name)
##       #table.DoDeclare(self,name)
##       setattr(self.app.tables,name,table)


class Application:
   def __init__(self):
      #if __builtins__.has_key('app'):
      #   raise LinoError('builtin name app already used!')
      #__builtins__['app'] = self
      # self.plugins = [] # AttribDict(self,"plugins")
      self.tables = [] # AttribDict(self,"tables")
      self.conn = None
      self._startupDone = False
      #self.plugins = AttribDict(self,"plugin list")
      #self.Startup()

##    def DeclareLink(self,
##                    fromTableName,joinName,fromLabel,
##                    toTableName,detailName=None,toLabel=None):
##       fromTable = app.tables[fromTableName]
##       toTable = app.tables[toTableName]
##       fromTable.AddJoin(joinName,toTable)
##       if detailName != None:
##          toTable.AddDetail(detailName,fromTable,joinName)

##    def init(self):
##       "override this method to add plugins to your Application"
##       pass

##    def AddPlugin(self,name,plugin):
##       "to be used during init()"
##       #plugin._declare(self,name)
##       #self.plugins.dict[name] = plugin
##       setattr(self.plugins,name,plugin)

##    def loadPlugin(self,name):
##       if name in self.plugins:
##          return
##       print "loadPlugin %s" % name
##       p = my_import(name)
##       self.plugins.append(p)
##       p.install(self)

   def connect(self,conn):
      self.conn = conn

   def Startup(self):
      if self._startupDone:
         raise "double startup"

      for (modname,module) in sys.modules:
         for (name,value) in dir(module):
            if isinstance(value,Table):
               value._declare(name)
               value.init()
               self.tables.append(value)
      
      # initialize Tables
      for (name,table) in self.tables.items():
         table._declare(self,name) #.__dict__['_dict']['_owner'])
         table.init()
   
      for (name,table) in self.tables.items():
         print "link ", table.name
         table.link(self)
   
      for (name,table) in self.tables.items():
         table.SetupPrimaryKey()
         
      for (name,table) in self.tables.items():
         table.SetupComponents()
         
      self._startupDone = True


   def getCursor(self,
                 target,
                 columnList=None):
      if isinstance(target,Table):
         return self.conn.getCursor(target.getDefaultQuery(columnList))
      elif isinstance(target,Query):
         return self.conn.getCursor(target)
      raise "target must be Table or Query"
      


      

   def ShutDown(self):
      if self.conn != None:
         self.conn.close()
         
##    def SetConnection(self,conn):
##       self.conn = conn
      
   def GetConnection(self):
      return self.conn

   def initdb(self):
      for (name,table) in self.tables.items():
         self.conn.create_table(table)


