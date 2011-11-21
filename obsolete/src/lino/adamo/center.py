## Copyright 2003-2007 Luc Saffre

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

raise "no longer used. now implemented by lino.console.Session"

import atexit
#from cStringIO import StringIO

#from lino.adamo.session import Session
from lino.adamo.database import Database
from lino.adamo import DatabaseError
#from lino.ui import console
#from lino.console import syscon
#from lino.console import Application


class Center:
    """
    singleton object used by adamo.
    """

    def __init__(self):
        #assert isinstance(app,Application)
        #self.ui = None
        #self._schemas = []
        self._connections = []
        self._databases = []
        #self._sessionFactory = Session
        #self._checkIntegrity = False
        #if toolkit is None:
        #    toolkit=syscon.getSystemConsole()
        #self.toolkit=toolkit

    def connection(self,*args,**kw):
        
        from lino.adamo.qtconn import Connection
        #from lino.adamo.dbds.firebird import Connection
        #from lino.adamo.dbds.sqlite_dbd import Connection
        #from lino.adamo.dbds.mysql_dbd import Connection
        #from lino.adamo.dbds.gadfly_dbd import Connection
        
##         try:
##             from lino.adamo.dbds.sqlite_dbd import Connection
##         except ImportError:
##             try:
##                 from lino.adamo.dbds.mysql_dbd import Connection
##             except ImportError:
##                 try:
##                     from lino.adamo.dbds.gadfly_dbd import Connection
##                 except ImportError:
##                     raise DatabaseError("no database driver available")
                
        conn = Connection(*args,**kw)
        self._connections.append(conn)
        #print conn
        return conn

    def debug(self):
        print "Connections:"
        for c in self._connections: print c
        print "Databases:"
        for c in self._databases: print c
        
            

    def database(self,schema,name=None,**kw):
        #if name is None:
        #    name = str(schema)+str(len(self._databases)+1)
        db = Database(schema,name=name,**kw)
        self._databases.append(db)
        return db

    def startDump(self):
        assert len(self._connections) == 1
        self._connections[0].startDump()
    def stopDump(self):
        assert len(self._connections) == 1
        return self._connections[0].stopDump()
    
    def peekDump(self):
        assert len(self._connections) == 1
        return self._connections[0].peekDump()
        
##     def set(self,checkIntegrity=None):
##         if checkIntegrity is not None:
##             self._checkIntegrity = checkIntegrity

##     def setSessionFactory(self,sf):
##         self._sessionFactory = sf
        
##      def addSession(self,session):
##          self._sessions.append(session)
    
##     def addSchema(self,schema):
##         #assert db is not None
##         #assert not self._databases.has_key(db.getName())
##         #self._databases[db.getName()] = db
##         assert not schema in self._schemas
##         self._schemas.append(schema)
        
        
##     def startup(self,ui,**kw):
##         self.ui = ui
##         assert len(self._schemas) > 0, "no schemas"
##         sess = self.createSession(ui)
##         for sch in self._schemas:
##             sch.startup(sess,**kw)
##         sess.setDefaultLanguage()
##         return sess

    
    def shutdown(self):
        # tests/adamo/7.py failed when several tests
        # were run (because previous startups remained open.
        #if self.ui is None:
        #    return
        #self.app.debug("Center.shutdown()")
##         for sch in self._schemas:
##             sch.shutdown(syscon)
##         self._schemas = []
        for db in self._databases:
            db.close()
        self._databases = []
        for conn in self._connections:
            conn.close()
        self._connections = []

##     def getOptionParser(self,**kw):
##         p = self.ui.getOptionParser(**kw)

##         def call_set(option, opt_str, value, parser,**kw):
##             self.set(**kw)

##         p.add_option("-c",
##                      "--check",
##                      help="perform integrity checks",
##                      action="callback",
##                      callback=call_set,
##                      callback_kwargs=dict(checkIntegrity=True)
##                      )
##         return p

##     def parse_args(args=None):
##         p = self.getOptionParser()
##         return p.parse_args(args)

##     def doCheckIntegrity(self):
##         return self._checkIntegrity
    
            
_center = Center() 
atexit.register(_center.shutdown)



for m in ( #'openSession',#'getOptionParser',
          'shutdown','database',
          'startDump', 'stopDump', 'peekDump',
          'debug',
          #'doCheckIntegrity', 
          #'addSchema',
          'connection'
          ):
    globals()[m] = getattr(_center,m)



    
