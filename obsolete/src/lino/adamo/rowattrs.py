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

#import types
#from copy import copy

import types
from lino.adamo import datatypes
from lino.misc.compat import *
from lino.misc.etc import issequence
from lino.adamo.exceptions import DataVeto, StartupDelay, NoSuchField
from lino.misc.descr import Describable, setdefaults

## reservedWords = """\
## pages
## order
## date
## time
## year
## type
## password
## null
## isnull notnull
## """.split()



# source: kinterbase language reference, keywords list
reservedWords = tuple("""\
ACTION ACTIVE ADD
ADMIN AFTER ALL
ALTER AND ANY
AS ASC ASCENDING
AT AUTO AUTODDL
AVG BASED BASENAME
BASE_NAME BEFORE BEGIN
BETWEEN BLOB BLOBEDIT
BUFFER BY CACHE
CASCADE CAST CHAR
CHARACTER CHARACTER_LENGTH CHAR_LENGTH
CHECK CHECK_POINT_LEN CHECK_POINT_LENGTH
COLLATE COLLATION COLUMN
COMMIT COMMITTED COMPILETIME
COMPUTED CLOSE CONDITIONAL
CONNECT CONSTRAINT CONTAINING
CONTINUE COUNT CREATE
CSTRING CURRENT CURRENT_DATE
CURRENT_TIME CURRENT_TIMESTAMP CURSOR
DATABASE DATE DAY
DB_KEY DEBUG DEC
DECIMAL DECLARE DEFAULT
DELETE DESC DESCENDING
DESCRIBE DESCRIPTOR DISCONNECT
DISPLAY DISTINCT DO
DOMAIN DOUBLE DROP
ECHO EDIT ELSE
END ENTRY_POINT ESCAPE
EVENT EXCEPTION EXECUTE
EXISTS EXIT EXTERN
EXTERNAL EXTRACT FETCH
FILE FILTER FLOAT
FOR FOREIGN FOUND
FREE_IT FROM FULL
FUNCTION GDSCODE GENERATOR
GEN_ID GLOBAL GOTO
GRANT GROUP GROUP_COMMIT_WAIT
GROUP_COMMIT_ WAIT_TIME HAVING
HELP HOUR IF
IMMEDIATE IN INACTIVE
INDEX INDICATOR INIT
INNER INPUT INPUT_TYPE
INSERT INT INTEGER
INTO IS ISOLATION
ISQL JOIN KEY
LC_MESSAGES LC_TYPE LEFT
LENGTH LEV LEVEL
LIKE LOGFILE LOG_BUFFER_SIZE
LOG_BUF_SIZE LONG MANUAL
MAX MAXIMUM MAXIMUM_SEGMENT
MAX_SEGMENT MERGE MESSAGE
MIN MINIMUM MINUTE
MODULE_NAME MONTH NAMES
NATIONAL NATURAL NCHAR
NO NOAUTO NOT
NULL NUMERIC NUM_LOG_BUFS
NUM_LOG_BUFFERS OCTET_LENGTH OF
ON ONLY OPEN
OPTION OR ORDER
OUTER OUTPUT OUTPUT_TYPE
OVERFLOW PAGE PAGELENGTH
PAGES PAGE_SIZE PARAMETER
PASSWORD PLAN POSITION
POST_EVENT PRECISION PREPARE
PROCEDURE PROTECTED PRIMARY
PRIVILEGES PUBLIC QUIT
RAW_PARTITIONS RDB$DB_KEY READ
REAL RECORD_VERSION REFERENCES
RELEASE RESERV RESERVING
RESTRICT RETAIN RETURN
RETURNING_VALUES RETURNS REVOKE
RIGHT ROLE ROLLBACK
RUNTIME SCHEMA SECOND
SEGMENT SELECT SET
SHADOW SHARED SHELL
SHOW SINGULAR SIZE
SMALLINT SNAPSHOT SOME
SORT SQLCODE SQLERROR
SQLWARNING STABILITY STARTING
STARTS STATEMENT STATIC
STATISTICS SUB_TYPE SUM
SUSPEND TABLE TERMINATOR
THEN TIME TIMESTAMP
TO TRANSACTION TRANSLATE
TRANSLATION TRIGGER TRIM
TYPE UNCOMMITTED UNION
UNIQUE UPDATE UPPER
USER USING VALUE
VALUES VARCHAR VARIABLE
VARYING VERSION VIEW
WAIT WEEKDAY WHEN
WHENEVER WHERE WHILE
WITH WORK WRITE
YEAR YEARDAY
ISNULL NOTNULL
""".split())


def is_reserved(name):
    # raise "'%s' is a reserved keyword" % name
    return name.upper() in reservedWords
       







class RowAttribute(Describable):
    def __init__(self,owner, name,
                 label=None,doc=None):
        Describable.__init__(self,None,name,label,doc)
        #assert owner.__class__ is Table
        self._owner = owner
        self._isMandatory = False
        self._validator = None
        self._trigger = None
        self._deleted=False
        
    def child(self,*args,**kw):
        return self.__class__(self,owner,*args,**kw)

    def delete(self):
        self._deleted=True
    
##     def canSetValue(self,row,value):
##         if value is None:
##             if self._isMandatory: return "may not be empty"
##             return
##         for v in self._onValidate:
##             msg=v(row,value)
##             if msg is not None: return msg
    
##     def afterSetAttr(self,row):
##         pass
##         """called after setting this value for this attribute in this
##         row. Automatically replaced by after_xxx table method.
##         Override this to modify other attributes who depend on this
##         one.    """

        
    def trigger(self,row):
        if self._trigger is not None:
            self._trigger(row)
        #for t in self._triggers:
        #    t(row)


        

    def format(self,v):
        #print repr(v)
        assert v is not None, datatypes.ERR_FORMAT_NONE
        return unicode(v)
        
    def parse(self,s):
        return s
        
    def onOwnerInit1(self,owner,name):
        pass
        
    def onTableInit1(self,owner,name):
        pass
    
    def onTableInit2(self,owner,schema):
        pass
        #self.owner = table
        
    def onTableInit3(self,owner,schema):
        pass
        #self._validators = tuple(self._validators)
        #self._triggers = tuple(self._triggers)

    def setValidator(self,meth):
        self._validator = meth

    def setTrigger(self,meth):
        self._trigger=meth

##     def onAreaInit(self,area):
##         pass
    
    def setMandatory(self):
        self._isMandatory = True

    def onAppend(self,row):
        pass

    def validate(self,value):
        if value is not None:
            self.validateType(value)
        #for v in self._validators:
        #    v(value)
        if self._validator is not None:
            self._validator(value)


    def checkIntegrity(self,row):
        pass

    def getAttrName(self):
        return self.name
    
##  def __str__(self):
##      return self.name

    def __repr__(self):
        return "<%s %s.%s>" % (self.__class__.__name__,
                                      self._owner.getTableName(),
                                      self.name)

    def getDefaultValue(self,row):
        return None
    

    def setCellValue(self,row,value):
        assert isinstance(row,self._owner._instanceClass)
        # does not setDirty() !
        self.validate(value)
        #self.canSetValue(row,value)
        row._values[self.name] = value
        #print self.name, "=", value
        
##     def getCellValue(self,row,col):
##         # overridden by BabelField and Detail
##         return row.getFieldValue(self.name)

    def getFltAtoms(self,colAtoms,context):
        return colAtoms

##     def getTestEqual(self,ds, colAtoms,value):
##         raise NotImplementedError

    def canWrite(self,row):
        # note : row may be None. 
        return True
    
##     def row2atoms(self,row):
##         """fill into atomicRow the atomic data necessary to represent
##         this column"""
##         value = row._values.get(self.name)
##         return self.value2atoms(value, row.getDatabase())

        
##     def value2atoms(self,value,ctx):
##         print self,value
##         raise NotImplementedError
    
    
    def atoms2row(self,atomicRow,colAtoms,row):
        atomicValues = [atomicRow[atom.index] for atom in colAtoms]
        row._values[self.name] = self.atoms2value(atomicValues,
                                                  row.getContext())
        #row.setDirtyRowAttr(self)

    #
    # change atoms2value(self,atomicRow,colAtoms,context)
    # to atoms2value(self,atomicValues,context)
    #
    def atoms2value(self,atomicValues,dbc):
        raise NotImplementedError

        
##  def atoms2dict(self,atomicRow,valueDict,colAtoms,area):
##      # overridden by Detail to do nothing
##      valueDict[self.name] = self.atoms2value(atomicRow,colAtoms,area)
        
    
    def getNeededAtoms(self,ctx):
        return ()

##  def getValueFromRow(self,row):
##      try:
##          return row._values[self.name]
##      except KeyError,e:
##          row._readFromStore()
##          return row._values[self.name]
##      #return row._values[name]

        

class Field(RowAttribute):
    """A storable atomic value of a known and constant type.
    
    """
    def __init__(self,owner,name,type,**kw):
        RowAttribute.__init__(self,owner,name,**kw)
        self.type = type
        if is_reserved(name):
            self._sqlName = "x"+name
        else:
            self._sqlName = name
        
        #self.visibility = 0
        #self.format = format

    def setType(self,type):
        self.type = type

##     def configure(self,type=None,label=None):
##         if type is not None:
##             self.

##     def getType(self):
##         return self.type

    def format(self,v):
        #assert v is not None, datatypes.ERR_FORMAT_NONE
        return self.type.format(v)
        
    def validateType(self,value):
        return self.type.validate(value)
    
##     def setCellValue(self,row,value):
##         if value is not None:
##             self.validate(value)
##             #print self, repr(value)
##         RowAttribute.setCellValue(self,row,value)
        
##     def canSetValue(self,row,value):
##         if value is not None:
##             self.type.validate(value)
##         RowAttribute.canSetValue(self,row,value)
        
    def parse(self,s):
        #print self.type
        return self.type.parse(s)
        
##  def asFormCell(self,renderer,value,size=None):
##      renderer.renderValue(value,self.type,size)
        
    def getNeededAtoms(self,ctx):
        return ((self._sqlName, self.type),)
        #return (query.provideAtom(self.name, self.type),)

##     def value2atoms(self,value,ctx):
##         return (value,)


##     def getTestEqual(self,ds,colAtoms,value):
##         assert len(colAtoms) == 1
##         a = colAtoms[0]
##         return ds._connection.testEqual(a.name,a.type,value)

        
    def atoms2value(self,atomicValues,dbc):
        assert len(atomicValues) == 1
        return atomicValues[0]
        
    
    def getMinWidth(self):
        return self.type.minWidth
    def getMaxWidth(self):
        return self.type.maxWidth
    def getMinHeight(self):
        return self.type.minHeight
    def getMaxHeight(self):
        return self.type.maxHeight



class BabelField(Field):

    def getNeededAtoms(self,ctx):
        assert ctx is not None,\
                 "tried to use BabelField for primary key?"
        l = []
        for lang in ctx.getBabelLangs(): 
            l.append( (self._sqlName+"_"+lang.id, self.type) )
        return l


    def validateType(self,value):
        return type(value) == types.TupleType
    
##     def getSupportedLangs(self):
##         return self._owner._schema.getSupportedLangs()

    
    def setCellValue(self,row,value):
        assert isinstance(row,self._owner._instanceClass)
        langs = row.getContext().getBabelLangs()
        #values = row.getFieldValue(self.name)
        values = row._values.get(self.name)
        if values is None:
            #if self._isMandatory:
            #    raise DataVeto("may not be empty")
            values = [None] * len(row.getDatabase().getBabelLangs())
            row._values[self.name] = values
        if len(langs) > 1:
            assert issequence(value), \
                   "%s is not a sequence" % repr(value)
            assert len(value) == len(langs), \
                   "%s expects %d values but got %s" % \
                   (self.name, len(langs), repr(value))
            i = 0
            for lang in langs:
                if lang.index != -1:
                    values[lang.index] = value[i]
                i += 1
        else:
            assert not issequence(value)
            index = langs[0].index
            if index != -1:
                values[index] = value
            
        
##     def getCellValue(self,row,col):
##         langs = row.getSession().getBabelLangs()
##         dblangs = row.getDatabase().getBabelLangs()
##         #if row.getTableName() == "Nations":
##         #    print __name__, langs, dblangs
##         # 35.py dblangs = row._ds._session.getBabelLangs()
##         values = row.getFieldValue(self.name)
##         #values = Field.getCellValue(self,row)
##         if values is None:
##             values = [None] * len(dblangs)
##         else:
##             assert issequence(values), \
##                    "%s is not a sequence" % repr(values)
##             assert len(values) == len(dblangs), \
##                    "Expected %d values but got %s" % \
##                    (len(dblangs), repr(values))
        
##         if len(langs) > 1:
##             l = []
##             for lang in langs:
##                 if lang.index != -1:
##                     l.append(values[lang.index])
##                 else:
##                     l.append(None)
##             return l
##         else:
##             index = langs[0].index
##             assert not index == -1
##             #print __name__, values[index], langs
##             return values[index]
        
##     def getTestEqual(self,ds, colAtoms,value):
##         langs = ds.getSession().getBabelLangs()
##         lang = langs[0] # ignore secondary languages
##         a = colAtoms[lang.index]
##         return ds._connection.testEqual(a.name,a.type,value)

##     def value2atoms(self,value,ctx):
##         # value is a sequence with all langs of db
##         dblangs = ctx.getBabelLangs()
##         rv = [None] * len(dblangs)
##         if value is None:
##             return rv
##         assert issequence(value), "%s is not a sequence" % repr(value)
##         assert len(value) == len(dblangs), \
##                "Expected %d values but got %s" % \
##                (len(dblangs), repr(value))
##         i = 0
##         for lang in dblangs:
##             rv[lang.index] = value[i]
##             i += 1

##         return rv
            
    def atoms2row(self,atomicRow,colAtoms,row):
        #print "BabelField.atoms2row()", self.name
        #langs = row.getSession().getBabelLangs()
        dblangs = row.getDatabase().getBabelLangs()
        assert len(dblangs) == len(colAtoms)
        # 35.py dblangs = row._ds._session.getBabelLangs()
        #values = row.getFieldValue(self.name)
        values = row._values.get(self.name)
        #print "poop"
        if values is None:
            values = [None] * len(dblangs)
            row._values[self.name] = values
        for lang in dblangs:
            #assert lang.index != -1
            #if lang.index != -1:
            value = atomicRow[colAtoms[lang.index].index]
            values[lang.index] = value
        #row._values[self.name] = l
        #row.setDirtyRowAttr(self)
    
    
    def getFltAtoms(self,colAtoms,context):
        l = []
        langs = context.getBabelLangs()
        for lang in langs:
            if lang.index != -1:
                l.append(colAtoms[lang.index])
        return l

    

    
## class Match(Field):
##     def __init__(self,origin,**kw):
##         assert isinstance(origin,Field)
##         self._origin = origin
##         Field.__init__(self,origin.type,**kw)
##         self.getLabel = origin.getLabel

##     def __getattr__(self,name):
##         return getattr(self._origin,name)
    

## class Button(RowAttribute,Action):
##  def __init__(self,meth,label=None,*args,**kw):
##      RowAttribute.__init__(self,label=label,doc=meth.__doc__)
##      Action.__init__(self,meth,*args,**kw)
        
##  def getCellValue(self,row):
##      return self._func(row)
    
class Pointer(Field):
    """A pointer to a row in another table.
    
    """
    def __init__(self, owner, name, toClass,
                 detailName=None,
                 **kw):
        Field.__init__(self,owner,name,toClass,**kw)
        self._neededAtoms = None
        
    def setType(self,tp):
        raise "not on Pointers"

##     def setDetail(self,detailName,columnNames=None,**kw):
##         return
##         "no longer used"
##         self.detailName = detailName
##         self.dtlColumnNames = columnNames
##         if columnNames is not None:
##             kw['columnNames'] = columnNames
##         self.dtlKeywords = kw
        
##     def onTableInit1(self,owner,name):
##         assert owner == self._owner
##         return
##         if self.detailName is None:
##             self.setDetail(
##                 owner.getTableName().lower()+'_by_'+self.name)
            
    def onTableInit2(self,owner,schema):
        self._toTables = schema.findImplementingTables(self.type)
        if len(self._toTables) == 0:
            # no Partner.type if PartnerTypes not implemented
            self.delete()
            return
        for toTable in self._toTables:
            toTable.registerPointer(self)
            
##         assert len(self._toTables) > 0, \
##                  "%s.%s : found no tables implementing %s" % \
##                  (owner.getName(),
##                   str(self),
##                   str(self.type))
        #if len(self._toTables) > 1:
        #   print "rowattrs.py:", repr(self)

##     def onTableInit3(self,owner,schema):
##         RowAttribute.onTableInit3(self,owner,schema)
##         #print '%s.%s' % (owner,self.name), ':', self._toTables
##         for toTable in self._toTables:
##             #if self.detailName == 'children':
##             #    print toTable, owner
##             toTable.registerPointer(self)
##             return
##             toTable.addDetail(self.detailName,
##                               self,
##                               self.dtlColumnNames,
##                               **self.dtlKeywords)
            
##     def getTestEqual(self,ds,colAtoms,value):
##         av = self.value2atoms(value,ds.getSession())
##         i = 0
##         l = []
##         for (n,t) in self.getNeededAtoms(ds.getSession()):
##             l.append(ds._connection.testEqual(n,t,av[i]))
##             i += 1
##         return " AND ".join(l)


            
    def getNeededAtoms(self,ctx):
        
        """ The toTable is possibly not yet enough initialized to tell
        me her primary atoms. In this case getPrimaryAtoms() will raise
        StartupDelay which will be caught in Schema.startup() """
        
        if self._neededAtoms is None:
            neededAtoms = []
            if self._deleted:
                pass
            elif len(self._toTables) > 1:
                #neededAtoms.append((self.name+"_tableId",AREATYPE))
                #i = 0
                for toTable in self._toTables:
                    for (name,type) in toTable.getPrimaryAtoms():
                        neededAtoms.append(
                            (self.name + toTable._sqlName
                             + "_" + name,
                             type) )
                    #i += 1
            else:
                for (name,type) in self._toTables[0].getPrimaryAtoms():
                    neededAtoms.append( (self.name + "_" + name,
                                         type) )

            self._neededAtoms = tuple(neededAtoms)
        return self._neededAtoms

    def checkIntegrity(self,row):
        raise "won't work: getCellValue() now needs col"
        pointedRow = self.getCellValue(row)
        if pointedRow is None:
            return # ok

        if pointedRow._query.peek(*pointedRow.getRowId()) is None:
            return "%s points to non-existing row %s" % (
                self.name,str(pointedRow.getRowId()))



    def getMinWidth(self):
        # TODO: 
        return 10
    def getMaxWidth(self):
        # TODO: 
        return 50
        #w = 0
        #for pk in self._toTable.getPrimaryKey():
        #   w += pk.getPreferredWidth()
        #return w
    def getMinHeight(self):
        return 1
    def getMaxHeight(self):
        return 1

        
##     def _findToTable(self,tableId):
##         for toTable in self._toTables:
##             if toTable.getTableId() == tableId:
##                 return toTable
##         raise "not found %d" % tableId

    
##     def value2atoms(self,value,ctx):
##         pointedRow = value
##         #print repr(pointedRow)
##         if pointedRow is None:
##             return [None] * len(self._neededAtoms)
        
##         if len(self._toTables) == 1:
##             return pointedRow.getRowId()
##         else:
##             rv = [None] * len(self._neededAtoms)
##             i = 0
##             tableId = pointedRow._query.getLeadTable().getTableId()
##             rid = pointedRow.getRowId()
##             for toTable in self._toTables:
##                 if toTable.getTableId() == tableId:
##                     ai = 0
##                     for a in toTable.getPrimaryAtoms():
##                         rv[i] = rid[ai]
##                         i+=1
##                         ai+=1
##                     return rv
##                 else:
##                     i += len(toTable.getPrimaryAtoms())


    def atoms2value(self,atomicValues,dbc):
        #ctx = row._ds._context
        if self._deleted: return None
        elif len(self._toTables) > 1:
            toTable = self._findUsedToTable(atomicValues)
            if toTable is None:
                return None
            atomicValues = self._reduceAtoms(toTable.getTableId(),
                                             atomicValues)
            #toArea = getattr(sess.tables,toTable.getTableName())
            toArea = dbc.query(toTable._instanceClass)
        else:
            #toTable = self._toTables[0]
            #areaName = toTable.getTableName()
            #toArea = getattr(sess.tables,areaName)
            toArea = dbc.query(self._toTables[0]._instanceClass)
        
        if None in atomicValues:
            return None
        try:
            return toArea.getInstance(atomicValues,False)
        except DataVeto,e:
            return str(e)
    
    
    def _findUsedToTable(self,atomicValues):
        i = 0
        for toTable in self._toTables:
            for justLoop in toTable.getPrimaryAtoms():
                #if atomicRow[colAtoms[i].index] is not None:
                if atomicValues[i] is not None:
                    return toTable
                i += 1
        return None
    
    def _reduceAtoms(self,tableId,atomicValues):
        """
            
        We want only the atoms for this tableId.  Example: if there
        are 3 possible tables (tableId may be 0,1 or 2) and pklen
        is 2, then there are 2*3 = 6 atoms.
            
              tableId 0 -> I want atoms 0 and 1  -> [0:2]
              tableId 1 -> I want atoms 2 and 3  -> [2:4]
              tableId 2 -> I want atoms 4 and 5  -> [4:7]
              
        """
            
        # the first atom is the tableId
        for toTable in self._toTables:
            pklen = len(toTable.getPrimaryAtoms())
            if toTable.getTableId() == tableId:
                return atomicValues[:pklen]
            else:
                atomicValues = atomicValues[pklen:]
        raise "invalid tableId %d" % tableId
    
    def validateType(self,value):
        #print value
        for toTable in self._toTables:
            if isinstance(value,toTable._instanceClass):
                return
            
        raise DataVeto("%r is not a %s instance" % \
                       (value,toTable.getTableName()))
        
##     def getType(self):
##         return self.type
##         #return datatypes.STRING

##     def getTargetSource(self,row): 
##         return row.getContext().query(self.type)
    
##     def getTargetSource(self,dbc): 
##         return dbc.query(self.type)
    
        
class Detail(RowAttribute):
    def __init__(self,owner,
                 name,tcl,pointerName,
                 label=None,doc=None,
                 **kw):
        self.pointerName = pointerName
        self.tcl=tcl
        #self.pointer = pointer
        RowAttribute.__init__(self,owner,
                              name,label=label,doc=doc)
        #kw[pointerName] = None
        self._queryParams = kw
        
    def onTableInit3(self,owner,schema):
        RowAttribute.onTableInit3(self,owner,schema)
        itables=schema.findImplementingTables(self.tcl)
        if self.pointerName is None:
            pn=None
            for t in itables:
                for f in t._fields:
                    pass
                for ptr in t._pointers:
                    if ptr.type == self.tcl:
                        pass
        for t in itables:
            self.pointer=t.getRowAttr(self.pointerName)
        self._queryParams[self.pointerName] = None
        
    def format(self,ds):
        return str(len(ds))+" "+ds.getLeadTable().getName()

        
##     def canSetValue(self,row,value):
##         raise "cannot set value of a detail"
    
    def getMinWidth(self):
        return 20
    def getMaxWidth(self):
        return 40
    def getMinHeight(self):
        return 1
    def getMaxHeight(self):
        return 4
    

        
##     def onAreaInit(self,area):
##         area.defineQuery(self.name,self._queryParams)
        

##     def row2atoms(self,row):
##         return ()
    
    def atoms2row(self,atomicRow,colAtoms,row):
        row._values[self.name] = None
        #row.setDirtyRowAttr(self)
    
    def atoms2value(self,atomicRow,colAtoms,dbc):
        assert len(colAtoms) == 0
        raise "cannot"
        
    def canWrite(self,row):
        # note : row may be None. 
        return False


##     def getCellValue(self,row,col):
##         q=col.detailQuery.child(masters=(row,))
##         #print "Detail.getCellValue():", q._search
##         return q
##         return col.detailQuery.child(samples={
##             self.pointer.name:row})
##         ds=row.getFieldValue(self.name)
##         if ds is None:
##             #ds=self.getDefaultValue()
##             kw = dict(self._queryParams)
##             kw[self.pointer.name] = row
##             ds=row.getSession().query(
##                 self.pointer._owner.__class__, **kw)
##             row._values[self.name] = ds
##         return ds
        
    def validateType(self,value):
        #raise "should never be called"
        pass
    
##     def getType(self):
##         return datatypes.STRING

class Vurt(Field):
    """
    
    A Vurt (virtual field) is a method 
    
    """
    def __init__(self,func,type,**kw):
        Field.__init__(self,type,**kw)
        self._func = func
        #self.type = type

    def format(self,v):
        return self.type.format(v)
        
    def parse(self,s):
        raise "not allowed"
        

##     def getPreferredWidth(self):
##         return self.type.width


    def setCellValue(self,row,value):
        raise DataVeto("not allowed")
        
    def getCellValue(self,row,col):
        return self._func(row)
    
    def atoms2row(self,atomicRow,colAtoms,row):
        pass

    
    
