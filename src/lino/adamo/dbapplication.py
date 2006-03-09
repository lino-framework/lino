## Copyright 2003-2006 Luc Saffre

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


from lino.adamo.schema import Schema
from lino.console import Application
from lino.adamo import center
from lino.adamo.dbsession import DbContext

class DbApplication(Application):
    
    #_dataCellFactory = DataCell
    #_windowFactory = lambda x: x
    tableClasses=NotImplementedError
    
        
##     def use(self,db=None): # ,langs=None):
##         # if necessary, stop using current db
##         if db != self.db and self.db is not None:
##             self.db.commit()
##             #self.db.removeSession(self)
##             if self._user is not None:
##                 self.logout()
##         if db is None:
##             #self.schema = None
##             #self.tables = None
##             #self.forms = None
##             self.db = None
##         else:
##             # start using new db
##             #self.schema = db.schema # shortcut
##             self.db = db
##             # self.tables = AttrDict(factory=self.openTable)
##             #self.forms = AttrDict(factory=self.openForm)
##             #if langs is None:
##             #    langs = db.getDefaultLanguage()
##             #self.setBabelLangs(langs)
##             self.setDefaultLanguage()
        
##         #self._formStack = []


##     def startup(self,**kw):
##         self.db.startup(self,**kw)
##         return DbContext(self,self.db)
        
        
    def quickStartup(self,
                     langs=None,
                     dump=False,
                     filename=None,
                     schema=None,
                     **kw):
        #print "%s.quickStartup()" % self.__class__
        if schema is None:
            schema=Schema()
            for cl in self.tableClasses:
                schema.addTable(cl)
            schema.initialize()
        #schema.setupSchema()
        #self.console.debug("Initialize Schema")
        db = schema.database(langs=langs)
        #self.console.debug("Connect")
        conn = center.connection(filename=filename)
        db.connect(conn)
        if dump:
            #conn.startDump(syscon.notice)
            #conn.startDump(self.console.stdout)
            assert hasattr(dump,'write')
            conn.startDump(dump)
        #return db.startup(self,**kw)
        return DbContext(self,db)
    



class MirrorLoaderApplication(DbApplication):

    def __init__(self,loadfrom=".",**kw):
        DbApplication.__init__(self,**kw)
        self.loadfrom = loadfrom
    
    def registerLoaders(self,loaders):
        for l in loaders:
            it = self.findImplementingTables(l.tableClass)
            assert len(it) == 1
            it[0].setMirrorLoader(l)

            
    def setupOptionParser(self,parser):
        Schema.setupOptionParser(self,parser)
        
        parser.add_option("--loadfrom",
                          help="""\
directory containing mirror source files""",
                          action="store",
                          type="string",
                          dest="loadfrom",
                          default=".")
    
##     def applyOptions(self,options,args):
##         Application.applyOptions(self,options,args)
##         self.loadfrom = options.loadfrom


