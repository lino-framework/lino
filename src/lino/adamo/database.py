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

from lino.misc.descr import Describable
#from lino.ui import console 
from lino.console import syscon

from lino.adamo import DataVeto
from lino.adamo import InvalidRequestError

#from lino.adamo.dbds.sqlite_dbd import Connection

from lino.adamo.session import Context, BabelLang

#from query import DatasourceColumnList
from lino.adamo.tim2lino import TimMemoParser
from lino.adamo.store import Store
#from lino.adamo import center 
from lino.adamo.dbsession import DbSession


class Database(Context,Describable):
    
    def __init__(self, app, langs=None, **kw):
        
        self._supportedLangs = []
        if langs is None:
            langs = 'en'
        for lang_id in langs.split():
            self._supportedLangs.append(
                BabelLang(len(self._supportedLangs), lang_id) )
        Describable.__init__(self,**kw)
        
        self._memoParser = TimMemoParser(self)

        self.app = app
        self._stores = {}
        self._sessions=[]
        self._connections=[]
        #self._populators = []
        self._startupDone= False
        #print self, "__init__():", self.getSupportedLangs()

##     def addPopulator(self,p):
##         #if self._startupDone:
##         #    raise TooLate("Cannot addPopulator() after startup()")
##         self._populators.append(p)
        
    def addSession(self,s):
        self._sessions.append(s)
        

    def removeSession(self,s):
        self._sessions.remove(s)
        #if len(self._sessions) == 0:
        #    self.close()
        
    def populate(self,sess,p):
        for store in self.getStoresById():
            if store.isVirgin():
                store.populate(sess,p)

    def getBabelLangs(self):
        "implements Context.getBabelLangs()"
        return self._supportedLangs

    def getSupportedLangs(self):
        return " ".join([lng.id for lng in self._supportedLangs])

    def getDefaultLanguage(self):
        return self._supportedLangs[0].id

    def findBabelLang(self,lang_id):
        for lang in self._supportedLangs:
            if lang.id == lang_id:
                return lang
            
        if not lang_id in self.app._possibleLangs:
            raise InvalidRequestError(
                "%r : impossible language (must be one of %r)" % (
                lang_id, self.app._possibleLangs))
            
        """
        index -1 means that values in this language should be ignored
        """
        #print self, ":", lang_id, \
        #      "not found in", self.getSupportedLangs()
        return BabelLang(-1,lang_id)
        #raise "%s : no such language code in %s" % (lang_id, repr(self))
        
    def memo2html(self,renderer,txt):
        if txt is None:
            return ''
        txt = txt.strip()
        self._memoParser.parse(renderer,txt)
        #return self.memoParser.html

        
    def getStoresById(self):
        l = []
        for table in self.app.getTableList():
            try:
                l.append(self._stores[table.__class__])
            except KeyError:
                pass
        return l

    def connect(self,conn,tableClasses=None):
        self._connections.append(conn)
        for t in self.app.getTableList(tableClasses):
            if not self._stores.has_key(t.__class__):
                self._stores[t.__class__] = Store(conn,self,t)


    def getContentRoot(self):
        return self.app.getContentRoot(self)

    def update(self,otherdb):
        
        # todo: should maybe explicitly close those stores who are
        # going to be referenceless...
        
        self._stores.update(otherdb._stores)
        
##      l = list(self._stores)
##      for store in otherdb._stores:
##          if l.
##      self._stores = tuple(l)

    
##  def beginContext(self,langs=None):
##      ctx = Context(self,langs)
##      self._contexts.append(ctx)
##      return ctx

##  def endContext(self,ctx):
##      assert self._contexts[-1] is ctx
##      self._contexts.pop()
##      #ctx.commit()

##  def beginSession(self,context=None):
##          if context is None:
##              context = self.beginContext()
##      sess = ConsoleSession()
##      sess.setContext(context)
##      return sess

    def checkTables(self,sess):
        job = sess.job("checkTables: " + self.getName(),
                       maxval=len(self._stores))

        for store in self._stores.values():
            store.checkTable(sess)
            job.inc()
            
        job.done()
        
    def createTables(self):
        for store in self.getStoresById():
            if store._connection.checkTableExist(
                store._table.getTableName()):
                pass
            else:
                store.createTable()
        #for store in self._stores:
        #   store._table.populate(store)
            #store.flush()

##      def connect(self,conn):
##          self.__dict__['conn'] = conn


    def startup(self,console=None):
        #print "%s.startup()" % self.__class__
        #if ui is None:
        #    ui = syscon.getSystemConsole()
        #sess=center.openSession(syscon.getSystemConsole())
        assert not self._startupDone,\
                 "Cannot startup() again " + repr(self)
        if console is None:
            console=syscon.getSystemConsole()
            
        sess=DbSession(self,console)
        for store in self.getStoresById():
            store.onStartup(sess)
                
        self._startupDone=True
        return sess
        

    def commit(self,sess):
        for store in self.getStoresById():
            store.commit(sess)
            
    #def flush(self):
    #   for store in self._stores:
    #       store.flush()
        #self.conn.commit()

    #def disconnect(self):

    def close(self):
        for store in self.getStoresById():
            store.close()
        self._stores = {}
        self._startupDone=False
            
        
    def shutdown(self):
        syscon.debug("Closing database "+ str(self))
        self.close()
        for conn in self._connections:
            conn.close()
        self._connections = []
        
##      for sess in self._sessions:
##          #sess.beforeShutdown()
##          self.removeSession(sess)
        
        #center.removeDatabase(self)
    
##     def restart(self):
##         self.close()
##         self.open()

                    
##         msgs = sess.checkIntegrity()
##         if len(msgs):
##             msg = "%s : %d database integrity problems" % (
##                 db.getName(), len(msgs))
##             print msg + ":"
##             print "\n".join(msgs)

            
        #~ ctx = self.beginContext()
        #~ retval = ctx.checkIntegrity()
        #~ self.endContext(ctx)
        #~ return retval
        

##  def beginSession(self,d=None):
##      #assert not d.has_key('__context__')
##      ctx = self.beginContext()
##      return ctx.beginSession(d)
        
##  def getAreaDict(self):
##      return self._areas

##  def __str__(self):
##      return "%s database connected to %s" % (str(self.schema),
##                                                           str(self.conn))

##  def datasource(self,query,**kw):
##      area = self._areas[query.leadTable.name]
##      if len(kw) > 0:
##          query = query.child(**kw)
##      return Datasource(area,query,**kw)



## class QuickDatabase(Database):
##     "Database instance with only one connection"
##     def __init__(self,
##                  schema,
##                  langs=None,
##                  label=None,
##                  filename=None
##                  ):


##         Database.__init__(self,
##                           schema,
##                           langs=langs,
##                           label=label)

        
##         self._connection = Connection(filename=filename,
##                                       schema=schema)

##         self.connect(self._connection)

## ##     def close(self):
## ##         Database.close(self)
## ##         self._connection.close()
## ##         self._connection = None

## ##     def commit(self):   
## ##         Database.commit(self)
## ##         self._connection.commit()
        
        


