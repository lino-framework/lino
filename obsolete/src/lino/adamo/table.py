#coding: iso-8859-1

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

"""

Baseclass Table and some derived classes (LinkTable, MemoTable, TreeTable, MemoTreeTable, BabelTable)

"""

import types

from lino.misc.compat import *
from lino.misc.descr import Describable
from lino.misc.etc import issequence

from lino.adamo import datatypes 
from lino.adamo.exceptions import StartupDelay, NoSuchField
from lino.adamo.rowattrs import RowAttribute,\
     Field, BabelField, Pointer, Detail, is_reserved
#from lino.adamo.row import StoredDataRow


DEFAULT_PRIMARY_KEY = 'id'
#DEFAULT_PRIMARY_KEY = 'key'
#DEFAULT_PRIMARY_KEY = 'rowId'

class SchemaComponent:
    
    def __init__(self):
        self._schema = None
        self._id = None
        
    def registerInSchema(self,schema,id):
        assert self._schema is None
        self._schema = schema
        self._id = id

    def getSchema(self):
        return self._schema

class FieldContainer:
    # inherited by Table 
    def __init__(self):
        self.__dict__['_fields'] = []
        self.__dict__['_rowAttrs'] = {}

    def addField(self,name,type,*args,**kw):
        return self.addRowAttr(Field(self,name,type,*args,**kw))
    def addPointer(self,name,*args,**kw):
        return self.addRowAttr(Pointer(self,name,*args,**kw))
    def addDetail(self,*args,**kw):
        return self.addRowAttr(Detail(self,*args,**kw))
    def addBabelField(self,name,type,*args,**kw):
        return self.addRowAttr(
            BabelField(self,name,type,*args,**kw))

    def addRowAttr(self,attr):
        assert attr._owner == self
        assert not self._rowAttrs.has_key(attr.name),\
               "Duplicate field definition %s.%s" % \
               (self.getTableName(),attr.name)
        #print self.getTableName()+':'+str(attr)
        self._fields.append(attr)
        self._rowAttrs[attr.name] = attr
        #i = self.Instance
        ic=self._instanceClass
        try:
            meth = getattr(ic,"validate_"+attr.name)
            attr.setValidator(meth)
            #attr._onValidate.append(meth)
        except AttributeError:
            pass
        
        try:
            meth = getattr(ic,"after_"+attr.name)
            #attr.afterSetAttr = meth
            attr.setTrigger(meth)
        except AttributeError:
            pass
        return attr

    def getFields(self):
        return self._fields
    
    def getRowAttr(self,name):
        try:
            return self._rowAttrs[name]
        except KeyError,e:
            raise NoSuchField, "%s.%s" % (self.name,name)

            #raise AttributeError,\
    


class Table(FieldContainer,SchemaComponent,Describable):
    """
    
    Holds meta-information about a data table. There is one instance
    of each database table in a Schema.  The Table does not worry
    about how the data is stored.
    
    
    """
    
    #_instanceClass=StoredDataRow

    def __init__(self,instanceClass,
                 name=None,label=None,doc=None):
        if name is None:
            name = instanceClass.tableName
            #name = self.__class__.__name__


        if is_reserved(name):
            self._sqlName="X"+name
        else:
            self._sqlName=name
            
        #if label is None:
        #    label = instanceClass.tableLabel
        if label is None:
            label = name

        self._instanceClass=instanceClass
        
        Describable.__init__(self,None,name,label,doc)
        SchemaComponent.__init__(self)
        FieldContainer.__init__(self)
        self._pk = None
        self._mandatoryColumns = None
        self._views = {}
        self._rowRenderer = None
        #self._mirrorLoader = None
        self._initStatus = 0
        self._defaultView = None
        self._pointers=[]


##     def init(self):
##         pass


    def __str__(self):
        #return self.__class__.__name__
        return self.name
    
    def __repr__(self):
        #return self.__class__.__name__
        return "Table(%s)" % self.name
    
##     def peek(self,sess,*args):
##         return sess.peek(self.__class__,*args)

##  def cmd_show(self):
##      return Command(self.show,label=self.getLabel())

##  def show(self,sess):
##      sess.openForm(self.getTableName())

    #def getLabel(self):
    #   return self.getTableName()

    def registerPointer(self,ptr):
        self._pointers.append(ptr)


    def setupMenu(self,frm):
        return self.dummy.setupMenu(frm)
        #"override this to insert specific actions to a form's menu"
        #pass
    
    def fillReportForm(self,rpt,frm):
        for col in rpt.getVisibleColumns():
            frm.addDataEntry(col,label=col.getLabel())
        
    def init1(self):
        #print "%s : init1()" % self._tableName
        self.dummy = self._instanceClass(None,None,{},False)
        self.dummy.initTable(self)
        
        #for (name,attr) in self.__dict__.items():
        #    if isinstance(attr,RowAttribute):
        #        self.addField(name,attr)
                
        if self._pk == None:
            if not self._rowAttrs.has_key(DEFAULT_PRIMARY_KEY):
                #f = Field(ROWID)
                #setattr(self,DEFAULT_PRIMARY_KEY,f)
                self.addField(DEFAULT_PRIMARY_KEY,datatypes.ROWID)
                #self._rowAttrs[DEFAULT_PRIMARY_KEY] = f
            self.setPrimaryKey(DEFAULT_PRIMARY_KEY)

        mandatoryColumns=[]
        for name,attr in self._rowAttrs.items():
            attr.onOwnerInit1(self,name)
            attr.onTableInit1(self,name)
            
##             try:
##                 #um = getattr(self.Instance,"after_"+name)
##                 um = getattr(self._instanceClass,"after_"+name)
##                 #attr.afterSetAttr = um
##                 attr.addTrigger(um)
##             except AttributeError:
##                 pass
            
            if attr._isMandatory or name in self._pk:
                if not isinstance(attr.type,datatypes.AutoIncType):
                    mandatoryColumns.append(attr)
            
        self._mandatoryColumns = tuple(mandatoryColumns)
        self._initStatus = 1

    def init2(self):
        #print "%s : try init2()" % self._tableName

        #for attr in self._rowAttrs.values():
        for attr in self._fields:
            attr.onTableInit2(self,self._schema)
##      if self._columnList is None:
##          self._columnList = " ".join(self.getAttrList())

        
        atoms = []
        for attrname in self._pk:
            attr = self._rowAttrs[attrname]
            for (name,type) in attr.getNeededAtoms(None):
                assert isinstance(type,datatypes.IntType) \
                       or isinstance(type,datatypes.DateType)\
                       or isinstance(type,datatypes.AsciiType),\
                       "%s cannot be primary key because type is %s" \
                       % (name,type)
                
                atoms.append((name,type))
        self._primaryAtoms = tuple(atoms)
        
        self._initStatus = 2
        #print "%s : init2() done" % self._tableName
            
    def init3(self):
        "called during database startup. Don't override."
        for attr in self._rowAttrs.values():
            attr.onTableInit3(self,self._schema)
        self._initStatus = 3
            
    def init4(self):
        #if self._columnList is None:
        #   self._columnList = " ".join(self.getAttrList())
        if self._defaultView is None:
            if self._views.has_key('std'):
                self._defaultView = 'std'
        self._pointers=tuple(self._pointers)
        self._initStatus = 4

    def vetoDeleteRow(self,row):
        dbc=row.getContext()
        for ptr in self._pointers:
            kw = { ptr.name : row }
            q=dbc.query(ptr._owner._instanceClass,**kw)
            if len(q):
                return "%s is used by %d rows in %s" % (
                    unicode(row),len(q),q.getLeadTable())
            
##     def addDetail(self,name,ptr,**kw):
##         # used by Pointer. onTableInit3()
##         #print '%s.addDetail(%s)' % (self.getTableName(),name)
##         dtl = Detail(self,name,ptr, **kw)
##         self._rowAttrs[name] = dtl
##         #dtl.setOwner(self,name)
##         #dtl.onTableInit2(self,schema)
##         #setattr(self,ame,dtl)

    def addView(self,viewName,columnNames=None,**kw):
        raise "no longer used"
        if columnNames is not None:
            kw['columnSpec'] = columnNames
        self._views[viewName] = kw
        
    def getView(self,viewName):
        raise "no longer used"
        #return self._views[viewName]
        return self._views.get(viewName,None)


##  def initDatasource(self,ds):
##      if ds._viewName is None:
##          return
##      view = self.getView(ds._viewName)
##      if view is None:
##          raise KeyError,ds._viewName+": no such view"
##      #print "Table.initDatasource(): " + repr(kw)
##      ds.config(**view)
##      #print ds._samples
##      #print "load() not yet implemented"

        
        
    def getAttrList(self):
        assert self._initStatus >= 3
        return [ name for name in self._rowAttrs.keys()]
    

##  def values2id(self,knownValues):
##      q = self.query()
##      return q.values2id(knownValues)
    
    def setPrimaryKey(self,columnList):
        if type(columnList) == types.StringType:
            columnList = columnList.split()
        self._pk = tuple(columnList)


    def getPrimaryKey(self):
        "returns a tuple of the names of the columns who are primary key"
        if self._pk == None:
            raise "Table %s : primary key is None!" % self.getName()
        return self._pk # ('id',)

    def onConnect(self,store):
        # will maybe never be used
        pass
    
##     def setMirrorLoader(self,loader):
##         self._mirrorLoader = loader
        
##     def loadMirror(self,store,sess):
##         if self._mirrorLoader is None:
##             return
##         if self._mirrorLoader.mtime() <= store.mtime():
##             sess.debug("No need to load "+\
##                        self._mirrorLoader.sourceFilename())
##             return
##         self._mirrorLoader.load(sess,store.query(sess))

    def onAppend(self,row):
        pass

    def getPrimaryAtoms(self):
        try:
            return self._primaryAtoms
        except AttributeError:
            raise StartupDelay, str(self)+"._primaryAtoms"

    def setColumnList(self,columnList):
        pass
        
    def setOrderBy(self,orderBy):
        pass

    def getTableId(self):
        return self._id

    def getTableName(self):
        return self.name





## class LinkTable(Table):
##     def __init__(self, parent, fromClass, toClass,*args,**kw):
##         Table.__init__(self,parent,*args,**kw)
##         self._fromClass = fromClass
##         self._toClass = toClass 
        

##     def init(self):
##         # Table.init(self)
##         self.addPointer('p',self._fromClass)
##         self.addPointer('c',self._toClass)
##         self.setPrimaryKey("p c")
##         del self._fromClass
##         del self._toClass


## class MemoTable(Table):
        
##     def init(self):
##         self.addField('title',datatypes.STRING).setMandatory()
##         self.addField('abstract',datatypes.MEMO)
##         self.addField('body',datatypes.MEMO)

##     class Instance(Table.Instance):
        
##         def __str__(self):
##             return self.title

    

## class TreeTable(Table):
        
##     def init(self):
##         self.addField('seq',datatypes.INT)
##         self.addPointer('super',self.__class__) #.setDetail('children')

##     class Instance(Table.Instance):
##         def getUpTree(self):
##             l = []
##             super = self.super
##             while super:
##                 l.insert(0,super)
##                 super = super.super
##             return l

## class MemoTreeTable(MemoTable,TreeTable):
##     def init(self):
##         MemoTable.init(self)
##         TreeTable.init(self)

##     class Instance(MemoTable.Instance,TreeTable.Instance):
##         def __str__(self):
##             return self.title

        
        

## class BabelTable(Table):
    
##     def init(self):
##         self.addBabelField('name',datatypes.STRING).setMandatory()
        
##     class Instance(Table.Instance):
##         def __str__(self):
##             return self.name














import os
import datetime
from lino.adamo.datatypes import TIME, DURATION
from lino.adamo.exceptions import DataVeto, DatabaseError
#from lino.ui import console
from lino.tools import dbfreader
from lino.console.task import Task
#from lino.console.task import Job


class DbfMirrorLoader(Task):

    tableClass = NotImplementedError  # subclass of adamo.tables.Table
    tableName = NotImplementedError   # name of external .DBF file

    def __init__(self,dbfpath=".",severe=True):
        assert type(dbfpath) == type(''), repr(dbfpath)
        self.dbfpath = dbfpath
        self.severe=severe
        # self.label="Loading "+ self.sourceFilename()
        # Task.__init__(self,"Loading "+ self.sourceFilename())
        
    def getLabel(self):
        return "Loading "+ self.sourceFilename()
    
    #def load(self,sess,store):
    def run(self,dbc):
        store=dbc.db.getStore(self.tableClass)
        # task.setLabel("Loading "+ self.sourceFilename())
        if self.mtime() <= store.mtime():
            self.verbose("No need to load %s.",self.sourceFilename())
            return

        f = dbfreader.DBFFile(self.sourceFilename(),codepage="cp850")
        f.open()
        #task.setMaxVal(len(f))
        def looper(task):
            q=store.query(dbc,"*")
            q.zap()
            for dbfrow in f:
                task.increment()
                if self.severe:
                    self.appendFromDBF(q,dbfrow)
                else:
                    try:
                        self.appendFromDBF(q,dbfrow)
                    except DataVeto,e:
                        sess.error(str(e))
                    except DatabaseError,e:
                        sess.error(str(e))
                    except UnicodeError,e:
                        raise
                    except ValueError,e:
                        sess.error(str(e))
                    except Exception,e:
                        if str(e).startswith(
                            "'ascii' codec can't encode character"):
                            raise
                        sess.error(repr(e))
            q.commit()
            
        self.loop(looper,"Loading "+ self.sourceFilename(),
                  maxval=len(f))
        f.close()

    def sourceFilename(self):
        return os.path.join(self.dbfpath, self.tableName+".DBF")
        
    def mtime(self):
        return os.stat(self.sourceFilename()).st_mtime


    def dbfstring(self,s):
        s=s.strip()
        if len(s) == 0:
            return None
        #s=s.replace(chr(255),' ')
        return s
    
    def dbfdate(self,s):
        if s is None: # len(s.strip()) == 0:
        #if len(s.strip()) == 0:
            return None
        return datatypes.DATE.parse(s)

    def dbftime(self,s):
        if s is None: # len(s.strip()) == 0:
            return None
        return datatypes.TIME.parse(s.replace('.',':'))
    
    def dbfduration(self,s):
        s = s.strip()
        if len(s) == 0:
            return None
        if s == "X":
            return None
        return datatypes.DURATION.parse(s.replace(':','.'))

