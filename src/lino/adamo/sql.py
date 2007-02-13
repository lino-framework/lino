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

import types
import datetime
#from time import mktime
from cStringIO import StringIO
import codecs

from lino.adamo import datatypes 
#from lino.adamo.rowattrs import Field, Pointer, Detail
from lino.adamo.query import FieldColumn, PointerColumn, DetailColumn
#from lino.adamo.rowattrs import Detail
from lino.adamo.row import DataRow
#from query import Query, QueryColumn
from lino.misc.etc import ispure

from lino.adamo.connection import Connection
#from lino.ui import console

#from mx.DateTime import DateTime

from lino.adamo.filters import NotEmpty, IsEqual, DateEquals, Contains


class SqlError(Exception):
    pass

class Master:
    # pseudo row for a Detail
    def __init__(self,ds):
        self.ds=ds

    def getRowId(self):
        l = []
        for col in self.ds._pkColumns:
            for a in col.getAtoms():
                l.append(self.ds.getTableName()+"."+a.name)
        return l
    
    def getContext(self):
        return self.ds.getContext()


class SqlConnection(Connection):
    
    "base class for SQL connections"
    
    #DEBUG = False
    
    CST_NEW = 1       # just created, must create tables and populate
    CST_OPENED = 2    # just opened, must check integrity
    CST_ACTIVE = 3    # tables created, integrity checked
    CST_CLOSING = 4
    CST_CLOSED = 5
    
    def __init__(self,sess): # ,*args,**kw):
        #Connection.__init__(self,ui,*args,**kw)
        self._dumpWriter = None
        self._status = self.CST_NEW
        self._dirty=False
        self.session=sess
        
    def getModificationTime(self,table):
        raise NotImplementedError
    def sql_exec_really(self,sql):
        raise NotImplementedError
    def commit_really(self):
        raise NotImplementedError
    
    def sql_exec(self,sql):
        #print "lino.adamo.sql:", sql
        if self._dumpWriter is not None:
            #self._dumpWriter += sql + ";\n"
            self._dumpWriter.write(sql+";\n")
        return self.sql_exec_really(sql)
        
    def startDump(self,writer=None):
        assert self._dumpWriter is None
        #self._dumpWriter = ""
        if writer is None:
            #writer=sys.stdout
            writer=StringIO()
        #else:
        #    assert hasattr(writer,"__call__")
        self._dumpWriter = writer
        

    def stopDump(self):
        dumpWriter = self._dumpWriter
        self._dumpWriter = None
        return dumpWriter.getvalue()
    def peekDump(self):
        s=self.stopDump()
        self.startDump()
        return s

    def testEqual(self,colName,type,value):
        if value is None:
            return "%s ISNULL" % (colName)
        else:
            return "%s = %s" % (colName,
                                self.value2sql(value, type))

    def value2sql(self,val,type):
        #print val, type
        if val is None:
            return 'NULL'
        elif isinstance(type, datatypes.BoolType):
            if val:
                return '1'
            else:
                return '0'
        elif isinstance(type, datatypes.DateType):
            # 20050128 return "%s" % str(val)
            return str(val.toordinal())
        elif isinstance(type, datatypes.TimeType):
            return "'" + type.format(val).replace("'", "''") + "'"
        elif isinstance(type, datatypes.DurationType):
            return "'" + type.format(val).replace("'", "''") + "'"
        elif isinstance(type, datatypes.IntType):
            return "%s" % str(val)
        elif isinstance(type, datatypes.TimeStampType):
            #return "%f" % mktime(val)
            return "%f" % val
        #elif isinstance(val, DateTime):
        #   return "'%s'" % str(val)
        elif val.__class__ in (types.StringType, types.UnicodeType):
            return "'%s'" % val.replace("'", "''") 
##         elif isinstance(val, types.StringType):
##             return "'%s'" % val.replace("'", "''") 
##         elif isinstance(val, types.UnicodeType):
##             return "'%s'" % val.replace("'", "''") 
        #elif type == self.schema.areaType:
        #   return "'%s'" % val._table.getName()
        raise TypeError, repr(val)
    

    def sql2value(self,s,type):
        #print "sql.sql2value() :", s, type
        if s is None:
            return None
        
        if isinstance(type, datatypes.DateType):
            return datetime.date.fromordinal(s)
        elif isinstance(type, datatypes.BoolType):
            return bool(s)
        elif isinstance(type, datatypes.LongType):
            return long(s)
        elif isinstance(type, datatypes.IntType):
            return s
        elif isinstance(type, datatypes.TimeStampType):
            return float(s)
        elif isinstance(type, datatypes.TimeType):
            return type.parse(s)
        elif isinstance(type, datatypes.DurationType):
            return type.parse(s)
        elif isinstance(type, datatypes.PriceType):
            return int(s)
        
        if not s.__class__ in (types.StringType,
                               types.UnicodeType):
            raise SqlError("%r is not a string" % s)
        
        if len(s) == 0:
            return None
            
        return type.parse(s)
        
    def type2sql(self,type):
        if isinstance(type, datatypes.IntType):
            return 'BIGINT'
        elif isinstance(type, datatypes.PriceType):
            return 'BIGINT'
        elif isinstance(type, datatypes.TimeStampType):
            return 'FLOAT'
        elif isinstance(type, datatypes.DateType):
            return 'INT'
        elif isinstance(type, datatypes.MemoType):
            return 'BLOB'
        elif isinstance(type, datatypes.BoolType):
            return 'INT'
        #elif type == self.schema.areaType:
        #   return 'VARCHAR(%d)' % 30 # area names are limited to 30 chars
        elif isinstance(type, datatypes.TimeType):
            return 'CHAR(%d)' % type.maxWidth
        elif isinstance(type, datatypes.DurationType):
            return 'CHAR(%d)' % type.maxWidth
        elif isinstance(type, datatypes.StringType):
            return 'VARCHAR(%d)' % type.maxWidth
        elif isinstance(type, datatypes.AsciiType):
            return 'CHAR(%d)' % type.maxWidth
        else:
            raise TypeError, repr(type)

    def mustCreateTables(self):
        #self.ui.debug('mustCreateTables '+str(self._status))
        if self._status == self.CST_NEW:
            return True
        return False
    
    def mustCheckTables(self):
        return self._status == self.CST_OPENED

        
    def executeCreateTable(self,query):
        table = query.getLeadTable()
        #query = table.query()
        sql = 'CREATE TABLE ' + table.getTableName() + " (\n     "
        sep = ' '
        l = []
        pka_names = [ n for (n,t) in table.getPrimaryAtoms()]
        for atom in query.getAtoms():
            s = atom.name + " " + self.type2sql(atom.type)
            if atom.name in pka_names:
                s += " NOT NULL"
            l.append(s)
            
        sql += ",\n  ".join(l)
                
        sql += ',\n  PRIMARY KEY ('
        l = []
        for (name,type) in table.getPrimaryAtoms():
            l.append(name)
            
        sql += ", " . join(l)

        sql += ")"
        
        #for ndx in table.indexes:
        #   sql += ', ' + ndx
     
        sql += "\n)"
        self._dirty=True
        self.sql_exec(sql) # .close()
        self.commit()



    def getSqlSelect(self, ds, 
                     sqlColumnNames=None,
                     limit=None,
                     offset=None) :
        clist = ds
        leadTable = ds.getLeadTable()
        
        if sqlColumnNames is None:
            sqlColumnNames = ", ".join([a.getNameInQuery(ds)
                                        for a in ds.getAtoms()])
##      dont delete. 
##         elif sqlColumnNames != "*":
##             sqlColumnNames += ", " +", ".join(
##                 [a.getNameInQuery(ds) for a in ds.getAtoms()])
            
        sql = u"SELECT " + sqlColumnNames
        
        sql += " FROM " + leadTable.getTableName()
        
        if ds.hasJoins():
            
            sql += " AS lead"
            
            for join in clist._joins:
                if len(join.pointer._toTables) == 1:
                    toTable = join.pointer._toTables[0]
                    sql += ' LEFT JOIN ' + toTable.getTableName()
                    sql += ' AS ' + join._sqlName 
                    sql += ' ON ('
                    l = []
                    for (a,b) in join.getJoinAtoms():
                        l.append("%s = %s" % (a.getNameInQuery(clist),
                                              b.getNameInQuery(clist)))
                    sql += " AND ".join(l) + ")"
                else:
                    joinAtoms = join.getJoinAtoms()
                    if join.parent is None:
                        if clist.hasJoins():
                            parentJoinName = "lead."
                        else:
                            parentJoinName = ""
                    else:
                        parentJoinName = join.parent._sqlName+"."
                    i = 0
                    for toTable in join.pointer._toTables:
                        sql += ' LEFT JOIN ' + toTable.getTableName()
                        sql += ' AS ' + join._sqlName \
                               + toTable._sqlName
                        sql += ' ON ('
                        l = []
                        for (name,type) in toTable.getPrimaryAtoms():
                            (a,b) = joinAtoms[i]
                            l.append("%s = %s" % (
                                a.getNameInQuery(clist),
                                b.getNameInQuery(clist)) )
                            i += 1
                        sql += " AND ".join(l) + ")"

        sql += self.whereClause(ds)
                
        l = []
        for col in ds.sortColumns:
            for atom in col.getFltAtoms(ds.getContext()):
                l.append(atom.getNameInQuery(clist))
        if len(l) >  0 :
            sql += " ORDER BY " + ", ".join(l)

        if limit is not None:
            if offset is None:
                sql += " LIMIT %d" % limit
            else:
                sql += " LIMIT %d OFFSET %d" % (limit,offset)
                
        return sql

    def filterWhere(self,flt,ds):
        l=[]
        if isinstance(flt,IsEqual):
            if isinstance(flt.col,PointerColumn):
                if flt.value is None:
                    for a in flt.col.getAtoms():
                        l.append(a.name+" ISNULL")
                elif isinstance(flt.value,DataRow):
                    # a constant pointer 
                    avalues=flt.col.atomize(
                        flt.value, ds.getDatabase())
                    i=0
                    for a in flt.col.getAtoms():
                        l.append(self.testEqual(
                            a.name,a.type,avalues[i]))
                        i+=1
                elif isinstance(flt.value,Master):
                    masterAtoms=[]
                    for c in flt.value.ds._pkColumns:
                        masterAtoms += c.getAtoms()
                    assert len(masterAtoms) == len(flt.col.getAtoms())
                    i=0
                    for a in flt.col.getAtoms():
                        l.append(\
                            a.name + \
                            "="+\
                            flt.value.ds.getTableName()+\
                            "."+masterAtoms[i].name)
                        i+=1
            elif isinstance(flt.col,FieldColumn):
                assert len(flt.col.getAtoms()) == 1
                a=flt.col.getAtoms()[0]
                l.append(self.testEqual(a.name,a.type,flt.value))
            else:
                raise NotImplementedError
                
        elif isinstance(flt,DateEquals):
            if isinstance(flt.col,FieldColumn):
                a=flt.col.getAtoms()
                assert len(a) == 1
                a=a[0]
                if flt.year is not None:
                    l.append("year("+a.name+")="+str(flt.year))
                if flt.month is not None:
                    #l.append(a.name+".month="+str(flt.month))
                    l.append("month("+a.name+")="+str(flt.month))
                if flt.day is not None:
                    l.append("DAY("+a.name+")="+str(flt.day))
            else:
                raise NotImplementedError
            
        elif isinstance(flt,Contains):
            if isinstance(flt.col,FieldColumn):
                raise NotImplementedError
            elif isinstance(flt.col,DetailColumn):
                raise NotImplementedError
                #if flt.value is not None:
                #    l.append()
            else:
                raise NotImplementedError
            
        elif isinstance(flt,NotEmpty):
            if isinstance(flt.col,FieldColumn):
                for a in flt.col.getAtoms():
                    l.append(a.name+" NOT NULL")
            elif isinstance(flt.col,DetailColumn):
                master=Master(ds)
                slave=flt.col.getCellValue(master)
                s = "EXISTS ("
                s += self.getSqlSelect(slave(),"*")
                s += ")"
                l.append(s)
            else:
                raise NotImplementedError, str(flt.col.__class__)
                    
        return l
    
##     def filterWhere(self,flt,ds):
##         l=[]
##         if isinstance(flt,NotEmpty):
##             if isinstance(flt.col.rowAttr,Field):
##                 for a in flt.col.getAtoms():
##                     l.append(a.name+" NOT NULL")
##             elif isinstance(flt.col.rowAttr,Detail):
##                 master=flt.col.rowAttr._owner
##                 slave=flt.col.rowAttr.pointer._owner
##                 #print "Master:", master.getTableName()
##                 #print "Slave:", slave.getTableName()
##                 s = "EXISTS (SELECT * FROM "
##                 s += slave.getTableName()
##                 s += " WHERE "
##                 l2=[]
##                 i=0
##                 pka=flt.col.rowAttr.pointer.getNeededAtoms(None)
##                 for name,t in master.getPrimaryAtoms():
##                     s2=master.getTableName()+"."+name
##                     s2+="="
##                     s2+=slave.getTableName()+"."+pka[i][0]
##                     l2.append(s2)
##                     i+=1
##                 s+=" AND ".join(l2)
##                 s += ")"
##                 l.append(s)
##             else:
##                 raise NotImplementedError
                    
##         return l
    

    def whereClause(self,ds):
        where = []
        for mc in ds._masterColumns:
            #flt=Master(mc,ds)
            flt=IsEqual(mc,ds._masters[mc.name])
            where+=self.filterWhere(flt,ds)
##         for (atom,value) in ds.getAtomicSamples():
##             where.append(self.testEqual(atom.name,atom.type,value))
        where += ds.filterExpressions
        if ds._filters is not None:
            for flt in ds._filters:
                where+=self.filterWhere(flt,ds)
        if len(where):
            return " WHERE " + " AND ".join(where)
        return ""

    def executeSelect(self,qry,**kw):
        sql = self.getSqlSelect(qry,sqlColumnNames=None, **kw)
        #print sql
        csr = self.sql_exec(sql)
##         if self.DEBUG:
##             print "%s -> %d rows" % (sql,csr.rowcount)
##          print "Selected %d rows for %s" % (csr.rowcount,
##                                                        query.getName())
        
        """TODO : check here for consistency between csr.description
        and expected meta-information according to query."""

        return csr
        # return SQLiteCursor(self,query)

    def executeCount(self,qry):
        sql = self.getSqlSelect(qry,sqlColumnNames='COUNT (*)' )
        #sql = "SELECT COUNT(*) FROM (%s)" % self.getSqlSelect(qry)
        csr = self.sql_exec(sql)
        #assert csr.rowcount is None or csr.rowcount == 1
        result=csr.fetchall()
        #csr.close()
        assert len(result) == 1, "more than one row?!"
        atomicRow=result[0]
        #atomicRow = csr.fetchone()
        #assert csr.fetchone() is None, "more than one row?!"
        count = int(atomicRow[0])
        #print "%s -> %d" % (sql, count)
        return count

    def isVirtual(self):
        return False

    def executeGetLastId(self,table,knownId=()):
        pka = table.getPrimaryAtoms()
        # pka is a list of (name,type) tuples
        assert len(knownId) == len(pka) - 1
        if self.isVirtual():
            # means that sqlite_dbd.Connection._filename is None
            return None
        # print pka
        sql = "SELECT MAX(%s) "  % pka[-1][0]
        sql += "FROM " + table.getTableName()
        l = []
        i = 0
        for (n,t) in pka[:-1]:
            l.append("%s = %s" % (n,self.value2sql(knownId[i],t)))
            i += 1
            
        if len(l):
            sql += " WHERE " + " AND ".join(l)
        #print sql
        csr = self.sql_exec(sql)
        #assert csr.rowcount is None or csr.rowcount == 1
        #assert csr.rowcount == 1
        result=csr.fetchall()
        #csr.close()
        assert len(result) == 1, "more than one row?!"
        val=result[0][0]
        #val = csr.fetchone()[0]
        return self.sql2value(val,pka[-1][1])

        
        
    def executePeek(self,qry,id):
        table = qry.getLeadTable()
        assert len(id) == len(table.getPrimaryAtoms()),\
                 "len(%s) != len(%s)" % (repr(id),
                                         repr(table.getPrimaryAtoms()))
        #for i in id: assert ispure(i)
        sql = "SELECT "
        l = [a.name for a in qry.getAtoms()]
        sql += ", ".join(l)
        sql += " FROM %s WHERE " % table.getTableName()
        
        l = []
        i = 0
        for (name,type) in table.getPrimaryAtoms():
            l.append("%s = %s" % (name,
                                  self.value2sql(id[i],type)))
            i += 1
        sql += " AND ".join(l)
        csr = self.sql_exec(sql)
        
        result=csr.fetchall()
        #csr.close()
        if len(result) == 0:
            return None
        assert len(result) == 1, \
               "%s.peek(%r) found more than one row" % (
            table.getName(), id)
        atomicRow=result[0]
        
        #atomicRow=csr.fetchone()
        #if atomicRow is None:
        #    return None
        #assert csr.fetchone() is None, \
        #       "%s.peek(%r) found more than one row" % (
        #    table.getName(), id)
        return self.csr2atoms(qry,atomicRow)
    
##         if False: 
##             print "%s -> %d rows" % (sql,csr.rowcount)
##         if csr.rowcount == 0:
##             return None
        
##         assert csr.rowcount == 1,\
##                  "%s.peek(%s) found %d rows" % (table.getName(),\
##                                                 repr(id),\
##                                                 csr.rowcount)
##         return self.csr2atoms(clist,csr.fetchone(),sess)
    
    def csr2atoms(self,qry,sqlatoms):
        "convert the result of a cursor to atoms"
        l = []
        i = 0
        for a in qry.getAtoms():
            try:
                v = self.sql2value(sqlatoms[i],a.type)
            except ValueError,e:
                qry.getDatabase().schema.session.exception(
                    e, details="""\
Could not convert raw atomic value %s in %s.%s (expected %s).""" \
                    % (repr(sqlatoms[i]),
                       qry.getLeadTable().name,
                       a.name,
                       str(a.type)))
                v = None
            l.append(v)
            i += 1
        return l

        
    def executeZap(self,table):
        sql = "DELETE FROM " + table.getTableName()
        self.sql_exec(sql)#.close()
        
    def executeInsert(self,row):
        query = row._store._peekQuery
        table = query.getLeadTable()
        #context = row.getContext()

        atomicRow = query.row2atoms(row)
        
        sql = "INSERT INTO %s ( " % table.getTableName()
        l = []
        #for atom in query.getFltAtoms(context): 
        for atom in query.getAtoms(): 
            l.append(atom.name) 
            
        sql += ", ".join(l)
        sql += " ) VALUES ( "
        l = []
        #for atom in query.getFltAtoms(context):
        for atom in query.getAtoms():
            l.append(
                self.value2sql(atomicRow[atom.index],
                               atom.type))
        #try:
        sql += ", ".join(l)
        #except UnicodeDecodeError,e:
        #    raise Exception(repr(l) + "\n" + str(e))
        
        sql += " )"
        self.sql_exec(sql)#.close()
        self._dirty=True
        #self.commit()
        
    def executeUpdate(self,row):
        query = row._store._peekQuery
        table = query.getLeadTable()
        #context = row.getContext()

        atomicRow = query.row2atoms(row)

        sql = "UPDATE %s SET " % table.getTableName()
        
        l = []
        #for atom in query.getFltAtoms(context): 
        for atom in query.getAtoms(): 
            l.append("%s = %s" % (
                atom.name,
                self.value2sql(atomicRow[atom.index],atom.type)))
        sql += ", ".join(l)

        # note: primary atoms are also set although their value never
        # changes. As long as this doesn't disturb I'll leave it
        # because filtering them out would be another test here.
        
        sql += " WHERE "

        l = []
        i = 0
        id = row.getRowId()
        for (name,type) in table.getPrimaryAtoms():
            l.append("%s = %s" % (name,
                                  self.value2sql(id[i],type)))
            i += 1
        sql += " AND ".join(l)

        self.sql_exec(sql)#.close()
        self._dirty=True
        #self.commit()

    def executeDelete(self,row):
        table = row._store.getTable()

        sql = "DELETE FROM " + table.getTableName()
        sql += " WHERE "

        l = []
        i = 0
        id = row.getRowId()
        for (name,type) in table.getPrimaryAtoms():
            l.append("%s = %s" % (name,
                                  self.value2sql(id[i],type)))
            i += 1
        sql += " AND ".join(l)
        self.sql_exec(sql)#.close()
        self._dirty=True

    def executeDeleteAll(self,ds):
        
        raise """
        no longer used because each row's delete() method must
        indiviually be called
        """
        
        assert ds._filters is None
        sql = "DELETE FROM " + ds.getLeadTable().getTableName()
        sql += self.whereClause(ds)
        #print sql
        self.sql_exec(sql)#.close()
        self._dirty=True

##     def executeDeleteRows(self,ds):
##         sql = "DELETE FROM " + ds._table.getTableName()
##         sql += self.whereClause(ds)
##         self.sql_exec(sql)

    def commit(self):
        #print "commit"
        if not self._dirty:
            return
        if self._dumpWriter is not None:
            self._dumpWriter.write("/* commit */\n")
        #print "COMMIT", __file__
        self.commit_really()
        self._dirty=False
        

#class SqlQuery(Query):     
#   def __init__(self, leadTable, name=None):
#       Query.__init__(self,leadTable,name)
        

## class ConsoleWrapper:
    
##     """
##     SQL requests are simply written to stdout.
##     """

##     def __init__(self,conn):
##         if writer is None:
##             self.writer = sys.stdout
##         else:
##             self.writer = writer

##     def write(self,msg):
##         self.writer.write(msg+";\n")



