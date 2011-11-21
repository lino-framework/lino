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

from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError
from lino.adamo.dbreports import QueryReport

class BabelLang:
    def __init__(self,index,id):
        self.index = index
        self.id = id

    def __repr__(self):
        return "<BabelLang %s(%d)>" % (self.id,self.index)



class Context:
    "interface implemented by DbContext and Database"
    
    def getBabelLangs(self):
        raise NotImplementedError

    def getLangs(self):
        return " ".join([lng.id for lng in self.getBabelLangs()])

    def supportsLang(self,lngId):
        for lng in self.getBabelLangs():
            if lng.id == lngId:
                return True
        return False
    
class DbContext(Context):
    def __init__(self,db,*args,**kw):
        self.db = db
        self.setDefaultLanguage()
        db.addContext(self)
        
    
    def setDefaultLanguage(self):
        self.setBabelLangs(self.db.getDefaultLanguage())

    def __str__(self):
        #return "%s on %s" % (self.user,self.db)
        #return self.__class__.__name__+
        return str(self.db)
        
    def setBabelLangs(self,langs):
        
        """langs is a string containing a space-separated list of babel
        language codes"""
        
        self.db.commit()
        self._babelLangs = []
        for lang_id in langs.split():
            self._babelLangs.append(self.db.findBabelLang(lang_id))
        assert self._babelLangs[0].index != -1,\
               "First language of %r must be one of %r" \
               % (langs,self.db.getSupportedLangs())
            
##         if self._babelLangs[0].index == -1:
##             raise InvalidRequestError(
##                 "First item of %s must be one of %s" % (
##                 repr(langs), repr(self.db.getBabelLangs())))

    def getBabelLangs(self):
        return self._babelLangs

    def getSchema(self):
        return self.db.schema

    def startup(self):
        self.db.startup(self)
    


    def checkIntegrity(self):
        self.status("Checking %s", self.db.getLabel())
        for store in self.db.getStoresById():
            store.checkIntegrity(self)
        self.status("Checking %s", self.db.getLabel())
        
##     def populate(self,p):
##         status=self.getSessionStatus()
##         #schema=self.db.schema
##         for store in self.db.getStoresById():
##             if store.isVirgin():
##                 #p.runfrom(self.db.schema.session.toolkit,self,store)
##                 name = "populate"+store.getTable().name
##                 print name
##                 try:
##                     m = getattr(p,name)
##                     self.status("Populating %s" % store)
##                     qry=store.query(self,"*")
##                     m(qry)
##                     store.commit()
##                 except AttributeError:
##                     self.debug("no method %s.%s",p,name)
##                     #pass
                
##         self.setSessionStatus(status)

    #def getSession(self):
    #    return self.session
    
    def getSessionStatus(self):
        return (self.getBabelLangs(),)
        
    def setSessionStatus(self,status):
        self.commit()
        self._babelLangs = status[0]
        
    def commit(self):
        return self.db.commit()

    def close(self):
        #self.db.removeSession(self.session)
        self.db.removeContext(self)
        #self.session.close()
        #self.app.close()
        
    def shutdown(self):
        # called in many TestCases during tearDown()
        # supposted to close all connections
        #
        self.close()
        self.db.shutdown()
        #center.shutdown()

    def getTableList(self):
        return self.db.schema.getTableList()
    
    def getTableClass(self,tableName):
        for table in self.db.schema.getTableList():
            if table.getTableName() == tableName:
                return table._instanceClass


##     def notice(self,*args,**kw):
##         return self.app.notice(*args,**kw)
##     def message(self,*args,**kw):
##         return self.app.message(*args,**kw)
##     def confirm(self,*args,**kw):
##         return self.app.confirm(*args,**kw)
        

    def query(self,tcl,columnNames=None,**kw):
        tables=self.db.schema.findImplementingTables(tcl)
        if len(tables) == 1:
            tcl=tables[0]._instanceClass
##             for t in tables:
##                 if t._instanceClass is leadTable
##                 leadTable= 
        if columnNames is None: columnNames="*"
        return self.db.getStore(tcl).query(self,columnNames,**kw)
        #return self.db.getStore(
        #    tables[0]._instanceClass).query(
        #    self,columnNames,**kw)
        #return tables[0]._store.query(self,columnNames,**kw)

    def peek(self,tableClass,*args):
        # used in raceman/report.py, cities_be.py...
        return self.db.getStore(tableClass).query(self).peek(*args)


##     def end(self):
##         self.use()
##         self.center.closeSession(self)


    def onLogin(self):
        return self.db.schema.onLogin(self)
    
    def getViewReport(self,tc,viewName="std",**kw):
        raise "should be replaced"
        qry = self.query(tc)
        view=qry.getView(viewName)
        if view is not None:
            assert not view.has_key('label')
            kw.update(view)
        return self.createQueryReport(qry,**kw)

    def createQueryReport(self,qry,*args,**kw):
        return QueryReport(qry,*args,**kw)
    
    def createReport(self,rptclass,**kw):
        "rptclass is expected to be a DataReport"
        return rptclass(self,**kw)


    def startDump(self):
        assert len(self.db._connections) == 1
        self.db._connections[0].startDump()
    def stopDump(self):
        assert len(self.db._connections) == 1
        return self.db._connections[0].stopDump()
    def peekDump(self):
        assert len(self.db._connections) == 1
        return self.db._connections[0].peekDump()






class Change:
    pass

class Update(Change):
    def __init__(self,row,attr,old,new):
        self.row=row
        self.attr=attr
        self.old=old
        self.new=new

class Insert(Change):        
    def __init__(self,row):
        self.row=row


class Delete(Change):        
    def __init__(self,row):
        self.row=row



class ChangeManager:
    def __init__(self):
        self.changes=[]

    
