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

from datasource import Datasource, DataCell
from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError
from lino.ui.console import getSystemConsole, Console


class BabelLang:
    def __init__(self,index,id):
        self.index = index
        self.id = id

    def __repr__(self):
        return "<BabelLang %s(%d)>" % (self.id,self.index)



class Context:
    "interface class"
    def getBabelLangs(self):
        raise NotImplementedError


            
class Session(Context):
    """
    A Session is if a machine starts Adamo
    """
    _dataCellFactory = DataCell
    #_windowFactory = lambda x: x
    
    def __init__(self,console=None,**kw):
        #self.app = app
        self._user = None
        self.db = None
        self.schema = None
        #self.tables = None
        self.forms = None
        
        if console is None:
            console = getSystemConsole()
        self._dumping = None
        self._setcon(console)
        
        self.use(**kw)

    def _setcon(self,console):
        self.console = console
        for m in console.forwardables:
            setattr(self,m,getattr(console,m))

##     def startDump(self,**kw):
##         assert self._dumping is None
##         self._dumping = self.console
##         self._setcon(Console(out=StringIO(),**kw))

##     def stopDump(self):
##         assert self._dumping is not None, "dumping was not started"
##         s = self.console.out.getvalue()
##         self._setcon(self._dumping)
##         self._dumping = None
##         return s
        

    def hasAuth(self,*args,**kw):
        return True
            
        
    def use(self,db=None,langs=None):
        # if necessary, stop using current db
        if db != self.db and self.db is not None:
            #self.db.removeSession(self)
            if self._user is not None:
                self.logout()
        if db is None:
            self.schema = None
            #self.tables = None
            self.forms = None
            self.db = None
        else:
            # start using new db
            self.schema = db.schema # shortcut
            self.db = db
            # self.tables = AttrDict(factory=self.openTable)
            self.forms = AttrDict(factory=self.openForm)
            if langs is None:
                langs = db.getDefaultLanguage()
            #self.db.addSession(self)
                
        if langs is not None:
            self.setBabelLangs(langs)
        
        #self._formStack = []
        
    def showForm(self,formName,modal=False,**kw):
        raise NotImplementedError

    def showReport(self,ds,showTitle=True,**kw):
        raise NotImplementedError

    def errorMessage(self,msg):
        raise NotImplementedError

    def notifyMessage(self,msg):
        raise NotImplementedError
        

##  def spawn(self,**kw):
##      kw.setdefault('db',self.db)
##      kw.setdefault('langs',self.getLangs())
##      return center.center().createSession(**kw)

    def commit(self):
        return self.db.commit()

    def shutdown(self):
        return self.db.shutdown()

    def setBabelLangs(self,langs):
        
        """langs is a string containing a space-separated list of babel
        language codes"""
        
        self.db.commit()
        self._babelLangs = []
        for lang_id in langs.split():
            self._babelLangs.append(self.db.findBabelLang(lang_id))
        if self._babelLangs[0].index == -1:
            raise "First item of %s must be one of %s" % (
                repr(langs), repr(self.db.getBabelLangs()))

    def getBabelLangs(self):
        return self._babelLangs

    def getLangs(self):
        return " ".join([lng.id for lng in self._babelLangs])
    
    def query(self,leadTable,columnNames=None,**kw):
        try:
            store = self.db._stores[leadTable]
        except KeyError,e:
            raise InvalidRequestError("no such table: "+str(leadTable))
        return Datasource(self,store,columnNames=columnNames,**kw)

    def report(self,**kw):
        raise NotImplementedError
    
##     def openTable(self,name):
##         try:
##             store = self.db._stores[name]
##         except KeyError,e:
##             #except AttributeError,e:
##             raise InvalidRequestError("no such table: "+name)
##         return Datasource(self,store)
    
##     def getDatasource(self,name):
##         return getattr(self.tables,name)

    def end(self):
        self.use()

    def populate(self):
        self.schema.populate(self)
        

##     def installto(self,d):
##         """
##         deprecated.
##         installto() will open all tables.
##         """
##         d['__session__'] = self
##         d['setBabelLangs'] = self.setBabelLangs
##         #self.context.tables.installto(d)
##         #d.update(
##         for name in self.db._stores.keys():
##             d[name] = getattr(self.tables,name)
##         #for name,store in self.db._stores.items():
##         #   ds = Datasource(self,store)
##         #   self.tables.define(name,ds)
        
    
    def onBeginSession(self):
        self.schema.onBeginSession(self)
        
    
    def openForm(self,formName,*args,**values):
        #print "openForm()" + formName
        cl = getattr(self.schema.forms,formName)
        frm = cl(self,*args,**values)
        #frm.init()
        return frm
    
    def onLogin(self):
        return self.db.schema.onLogin(self)
    
    def getUser(self):
        return self._user

    def login(self,user):
        if self._user is not None:
            self.logout()
        self._user = user
        
    def logout(self):
        assert self._user is not None
        self._user = None

    def checkIntegrity(self):
        msgs = []
        #for q in self.tables:
        for cl in self.db._stores.keys():
            q = self.query(cl)
            #q = getattr(self.tables,name)
            self.info("%s : %d rows" % (q._table.getTableName(),
                                        len(q)))
            l = len(q)
            for row in q:
                #row = q.atoms2instance(atomicRow)
                msg = row.checkIntegrity()
                if msg is not None:
                    msgs.append("%s[%s] : %s" % (
                        q._table.getTableName(),
                        str(row.getRowId()),
                        msg))
            #store.flush()
        return msgs
        


##  def startSession(self):
##      if self.context is not None:
##          self.context.schema.onStartSession(self)
        
        


class ConsoleSession(Session):

    def showForm(self,formName,modal=False,**kw):
        frm = self.openForm(formName,**kw)
        wr = self.console.out.write
        wr(frm.getLabel()+"\n")
        wr("="*len(frm.getLabel())+"\n")
        for cell in frm:
            wr(cell.getLabel() + ":" + cell.format())
            wr("\n")


##     def report(self,**kw):
##         return self.console.report(**kw)
        
    def showReport(self,ds,*args,**kw):
        rpt = self.report(ds,*args,**kw)
        rpt.beginReport()
        for row in ds:
            rpt.renderRow(row)
        rpt.endReport()
        
##     def showReport(self,ds,columnNames=None,showTitle=True,**kw):
##         raise "replaced by report()"
##         wr = self.console.out.write
##         #if len(kw):
##         rpt = ds.report(columnNames,**kw)
##         #print [col.name for col in rpt._clist.visibleColumns]
##         if showTitle:
##             wr(rpt.getLabel()+"\n")
##             wr("="*len(rpt.getLabel())+"\n")
##         columns = rpt.getVisibleColumns()
##         wr(" ".join(
##             [col.getLabel().ljust(col.getPreferredWidth()) \
##              for col in columns]).rstrip())
##         wr("\n")
##         wr(" ".join( ["-" * col.getPreferredWidth() \
##                               for col in columns]))
##         wr("\n")
##         for row in rpt:
##             l = []
##             for cell in row:
##                 #col = columns[i]
##                 l.append(cell.format())
##             wr(" ".join(l).rstrip())
##             wr("\n")





class AbstractWebSession(Session):
    
    def __init__(self,**kw):
        Session.__init__(self,**kw)
        self._messages = []

    def errorMessage(self,msg):
        self._messages.append(msg)

    def notifyMessage(self,msg):
        self._messages.append(msg)

    def popMessages(self):
        l = self._messages
        self._messages = []
        return l
        
    def showForm(self,formName,modal=False,**kw):
        raise NotImplementedError
        
    def showReport(self,ds,columnNames=None,showTitle=True,**kw):
        raise NotImplementedError
        
        
        
