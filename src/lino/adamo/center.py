## Copyright 2003-2005 Luc Saffre

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

import atexit
#from cStringIO import StringIO

from lino.adamo.session import Session
from lino.adamo import DatabaseError
#from lino.ui import console

class Center:
    """
    The Center is the global singleton object used by adamo.
    It holds a list of connections, sessions and databases. 
    """

    def __init__(self):
        self.ui = None
        self._schemas = []
        self._connections = []
        #self._databases = []
        self._sessions = []
        #self._sessionFactory = Session
        self._checkIntegrity = False

    def connection(self,ui,schema,*args,**kw):
        try:
            from lino.adamo.dbds.sqlite_dbd import Connection
        except ImportError:
            try:
                from lino.adamo.dbds.mysql_dbd import Connection
            except ImportError:
                try:
                    from lino.adamo.dbds.gadfly_dbd import Connection
                except ImportError:
                    raise DatabaseError("no database driver available")
                
        conn = Connection(ui,*args,**kw)
        self._connections.append(conn)
        return conn
        
    def set(self,checkIntegrity=None):
        if checkIntegrity is not None:
            self._checkIntegrity = checkIntegrity

##     def setSessionFactory(self,sf):
##         self._sessionFactory = sf
        
    def createSession(self,ui,**kw):
        #sess = self._sessionFactory(self,**kw)
        sess = Session(self,ui,**kw)
        self._sessions.append(sess)
        return sess

    def removeSession(self,session):
        self._sessions.remove(session)

##      def addSession(self,session):
##          self._sessions.append(session)
    
    def addSchema(self,schema):
        #assert db is not None
        #assert not self._databases.has_key(db.getName())
        #self._databases[db.getName()] = db
        assert not schema in self._schemas
        self._schemas.append(schema)
        
        
    def startup(self,ui,**kw):
##         if ui is None:
##             ui = console.getSystemConsole()
        self.ui = ui
        assert len(self._schemas) > 0, "no schemas"
        #job = ui.job("center.startup()",len(self._schemas))
        sess = self.createSession(ui)
        for sch in self._schemas:
            #job.increment()
            sch.startup(sess,**kw)
        sess.setDefaultLanguage()
        #job.done()
        return sess

    
    def shutdown(self):
        # self.shutdown() # tests/adamo/7.py failed when several tests
        # were run (because previous startups remained open.
        if self.ui is None:
            return
        self.ui.debug("Center.shutdown()")
        for sch in self._schemas:
            sch.shutdown(self.ui)
        self._schemas = []
        for conn in self._connections:
            conn.close()
        self._connections = []

    def getOptionParser(self,**kw):
        p = self.ui.getOptionParser(**kw)

        def call_set(option, opt_str, value, parser,**kw):
            self.set(**kw)

        p.add_option("-c",
                     "--check",
                     help="perform integrity checks",
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(checkIntegrity=True)
                     )
        return p

    def parse_args(args=None):
        p = self.getOptionParser()
        return p.parse_args(args)

    def doCheckIntegrity(self):
        return self._checkIntegrity
    
            
_center = Center() 
atexit.register(_center.shutdown)



for m in ('createSession','getOptionParser',
          'startup', 'shutdown',
          'doCheckIntegrity', 
          'addSchema',
          'connection'
          ):
    globals()[m] = getattr(_center,m)



    
