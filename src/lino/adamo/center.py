## Copyright Luc Saffre 2003-2004.

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

from cStringIO import StringIO

from session import ConsoleSession

_center = None # User code should call getCenter() to get this instance.

class Center:
    """
    The Center is the global singleton object used by adamo.
    It holds a list of connections, sessions and databases. 
    Each session can have its own console
    """

    def __init__(self):
        self._connections = []
        self._databases = []
        self._sessions = []
        self._sessionFactory = ConsoleSession

    def addConnection(self,conn):
        assert not conn in self._connections
        self._connections.append(conn)
        

    def setSessionFactory(self,sf):
        self._sessionFactory = sf
        
    def createSession(self,**kw):
        sess = self._sessionFactory(**kw)
        self._sessions.append(sess)
        return sess

    def removeSession(self,session):
        self._sessions.remove(session)

##      def addSession(self,session):
##          self._sessions.append(session)
    
    def addDatabase(self,db):
        #assert db is not None
        #assert not self._databases.has_key(db.getName())
        #self._databases[db.getName()] = db
        assert not db in self._databases
        self._databases.append(db)
        
##  def getDatabase(self,name):
##          return self._databases[name]
    
    def removeDatabase(self,db):
        self._databases.remove(db)
        #del self._databases[db.getName()]
        
    def startup(self,checkIntegrity=True,populate=True):
        sess = self.createSession()
        assert len(self._databases) > 0,"no databases"
        for db in self._databases:
            sess.use(db)
            for store in db.getStoresById():
                store.createTables(sess)
            if populate:
                for store in db.getStoresById():
                    store.populate(sess)
            if checkIntegrity:
                for store in db.getStoresById():
                    store.checkIntegrity(sess)
        sess.setDefaultLanguage()
        return sess

    
    def shutdown(self):

        for db in self._databases:
            db.close()
        self._databases = []
        
        for conn in self._connections:
            conn.close()
        self._connections = []

##    use createSession().use() instead!
##  def use(self,db=None,**kw):
##      self.addDatabase(db)
##      sess = self.createSession()
##      sess.use(db=db,**kw)
##      return sess

            

            
_center = Center()

for m in ('createSession',
          'startup', 'shutdown',
          'addDatabase', 'removeDatabase',
          'addConnection'
          ):
    globals()[m] = getattr(_center,m)


## def start(**kw):
    
##     """This can be invoked once to specify explicit options for the Center singleton.  
##     It is not allowed to call it when the Center is already instanciated.
##     """
##     global _center
##     assert _center is None
##     return _center

## def getCenter():

##     """ Returns the global Center singleton.  Instanciates it if this
##     is the first call.  """
    
##     global _center
##     if _center is None:
##         start()
##     return _center

## def createSession(**kw):
##     return _center.createSession(**kw)
    
## def shutdown(**kw):
##     return _center.shutdown(**kw)
    

    
