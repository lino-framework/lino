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

import types
import datetime

from lino.adamo import datatypes 
from lino.adamo.rowattrs import Field, Pointer #, Detail
#from query import Query, QueryColumn

from lino.adamo.connection import Connection
from lino.ui import console

#from mx.DateTime import DateTime


class SqlConnection(Connection):
    
    "base class for SQL connections"
    
    DEBUG = False
    
    CST_NEW = 1       # just created, must create tables and populate
    CST_OPENED = 2    # just opened, must check integrity
    CST_ACTIVE = 3    # tables created, integrity checked
    CST_CLOSING = 4
    CST_CLOSED = 5
    
    def __init__(self,schema):
        Connection.__init__(self,schema)
        self._dump = None
        self._status = self.CST_NEW
        
    def getModificationTime(self,table):
        raise NotImplementedError
    
    def sql_exec_really(self,sql):
        raise NotImplementedError
    
    def sql_exec(self,sql):
        if self._dump is not None:
            self._dump += sql + ";\n"
        return self.sql_exec_really(sql)
        
    def startDump(self):
        self._dump = ""

    def stopDump(self):
        s = self._dump 
        self._dump = None
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
        elif val is True:
            return '1'
        elif val is False:
            return '0'
        elif isinstance(type, datatypes.DateType):
            # 20050128 return "%s" % str(val)
            return str(val.toordinal())
        elif isinstance(type, datatypes.TimeType):
            return "'%s'" % str(val).replace("'", "''") 
        elif isinstance(type, datatypes.DurationType):
            s = type.format(val)
            return "'%s'" % s.replace("'", "''") 
        elif isinstance(type, datatypes.IntType):
            return "%s" % str(val)
        #elif isinstance(val, DateTime):
        #   return "'%s'" % str(val)
        elif isinstance(val, types.StringType):
            return "'%s'" % val.replace("'", "''") 
        #elif isinstance(type, StringType):
        #    return "'%s'" % val.replace("'", "''") 
        elif isinstance(val, types.UnicodeType):
            return "'%s'" % val.replace("'", "''") 
        #elif type == self.schema.areaType:
        #   return "'%s'" % val._table.getName()
        raise TypeError, repr(val)
    

    def sql2value(self,s,type):
        #print "sql.sql2value() :", s, type
        if s is None:
            return None
        elif isinstance(type, datatypes.DateType):
            return datetime.date.fromordinal(s)
        elif isinstance(type, datatypes.IntType):
            return int(s)
        elif isinstance(type, datatypes.TimeType):
            return type.parse(s)
        elif isinstance(type, datatypes.DurationType):
            return type.parse(s)
        elif isinstance(type, datatypes.PriceType):
            return int(s)
        #elif type == self.schema.areaType:
        #   return type.parse(val)
        return s
        
    def type2sql(self,type):
        if isinstance(type, datatypes.IntType):
            return 'BIGINT'
        elif isinstance(type, datatypes.PriceType):
            return 'BIGINT'
        elif isinstance(type, datatypes.DateType):
            return 'INT'
        elif isinstance(type, datatypes.MemoType):
            return 'TEXT'
        elif isinstance(type, datatypes.BoolType):
            return 'INT'
        #elif type == self.schema.areaType:
        #   return 'VARCHAR(%d)' % 30 # area names are limited to 30 chars
        elif isinstance(type, datatypes.TimeType):
            return 'CHAR(%d)' % type.width
        elif isinstance(type, datatypes.DurationType):
            return 'CHAR(%d)' % type.width
        elif isinstance(type, datatypes.StringType):
            if type.width < 20:
                return 'CHAR(%d)' % type.width
            else:
                return 'VARCHAR(%d)' % type.width
        else:
            raise TypeError, repr(type)

    def mustCreateTables(self):
        console.debug('mustCreateTables '+str(self._status))
        if self._status == self.CST_NEW:
            return True
        return False
    
    def mustCheckTables(self):
        return self._status == self.CST_OPENED

        
    def executeCreateTable(self,query):
        table = query.leadTable
        #query = table.query()
        sql = 'CREATE TABLE ' + table.getTableName() + " (\n     "
        sep = ' '
        l = []
        for atom in query.getAtoms():
            s = atom.name + " " + self.type2sql(atom.type)
            if atom in table.getPrimaryKey():
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
        self.sql_exec(sql)



    def getSqlSelect(self, ds, 
                     sqlColumnNames=None,
                     limit=None,
                     offset=None) :
        clist = ds._clist
        leadTable = ds._clist.leadTable
        
        if sqlColumnNames is None:
            sqlColumnNames = ''
        else:
            sqlColumnNames += ', '
            
        sqlColumnNames += ", ".join([a.getNameInQuery(clist)
                                     for a in clist.getAtoms()])
        sql = "SELECT " + sqlColumnNames
        
        sql += "\nFROM " + leadTable.getTableName()
        
        if clist.hasJoins():
            
            sql += " AS lead"
            
            for join in clist._joins:
                if len(join.pointer._toTables) == 1:
                    toTable = join.pointer._toTables[0]
                    sql += '\n  LEFT JOIN ' + toTable.getTableName()
                    sql += ' AS ' + join.name 
                    sql += '\n    ON ('
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
                        parentJoinName = join.parent.name+"."
                    i = 0
                    for toTable in join.pointer._toTables:
                        sql += '\n  LEFT JOIN ' + toTable.getTableName()
                        sql += ' AS ' + join.name + toTable.getTableName()
                        sql += '\n    ON ('
                        l = []
                        #l.append("%s_tableId = %d" % (
                        #   parentJoinName+join.name,toTable.getTableId()))
                        for (name,type) in toTable.getPrimaryAtoms():
                            (a,b) = joinAtoms[i]
                            l.append("%s = %s" % (
                                a.getNameInQuery(clist),
                                b.getNameInQuery(clist)) )
                            i += 1
                        sql += " AND ".join(l) + ")"
                
        where = []

##      if len(ctrl.atomicSamplesColumns) > 0:
##          for (atom,value) in ctrl.atomicSamplesColumns:
##              where.append("%s = %s" % (atom.name,
##                                                conn.value2sql(value,
##                                                                    atom.type)))

        for (atom,value) in ds.getAtomicSamples():
        #for (atom,value) in ds.atomicSamples:
            where.append(self.testEqual(atom.name,atom.type,value))         
            
##      for (col,value) in self.getSampleColumns(samples):
##          w = col.
##          if isinstance(col.rowAttr,Pointer):
##              avalues = value.getRowId()
##          else:
##              avalues = (value,)

##          i = 0
##          for atom in col.getAtoms():
##              where.append("%s = %s" % (atom.name,
##                                                conn.value2sql(avalues[i],
##                                                                    atom.type)))
##              i += 1
                    

        where += ds.filterExpressions
        
        if len(where):
            sql += "\n  WHERE " + "\n     AND ".join(where)

                
        if len(ds.orderByColumns) >  0 :
            l = []
            for col in ds.orderByColumns:
                #col = self.findColumn(colName)
                #if col:
                    for atom in col.getFltAtoms(ds.getSession()):
                        l.append(atom.getNameInQuery(clist))
                #else:
                #   raise "%s : no such column in %s" % \
                #           (colName,
                #            [col.name for col in self.getColumns()])
            sql += "\n  ORDER BY " + ", ".join(l)

        if limit is not None:
            if offset is None:
                sql += " LIMIT %d" % limit
                #offset = 0
            else:
                sql += " LIMIT %d OFFSET %d" % (limit,offset)
                
        return sql
    


        

        
    def executeSelect(self,ds,**kw):
        sql = self.getSqlSelect(ds,sqlColumnNames=None, **kw)
        #print sql
        csr = self.sql_exec(sql)
        if self.DEBUG:
            print "%s -> %d rows" % (sql,csr.rowcount)
##          print "Selected %d rows for %s" % (csr.rowcount,
##                                                        query.getName())
        
        """TODO : check here for consistency between csr.description
        and expected meta-information according to query."""

        return csr
        # return SQLiteCursor(self,query)

    def executeCount(self,ds):
        sql = self.getSqlSelect(ds,sqlColumnNames='COUNT()' )
        #print sql
        csr = self.sql_exec(sql)
        if self.DEBUG:
            print "%s -> %d" % (sql, csr.rowcount)
        assert csr.rowcount == 1
        atomicRow = csr.fetchone()
        #print atomicRow
        count = int(atomicRow[0])
        # print repr(count)
        return count
        #print "%s -> %d rows" % (sql,csr.rowcount)
        #print csr.
        #return csr.rowcount

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
        assert csr.rowcount == 1
        val = csr.fetchone()[0]
        return self.sql2value(val,pka[-1][1])

        
        
    def executePeek(self,clist,id):
        table = clist.leadTable
        #clist = table.clist()
        assert len(id) == len(table.getPrimaryAtoms()),\
                 "len(%s) != len(%s)" % (repr(id),
                                         repr(table.getPrimaryAtoms()))
        sql = "SELECT "
        l = [a.name for a in clist.getAtoms()]
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
        if False: 
            print "%s -> %d rows" % (sql,csr.rowcount)
        if csr.rowcount == 0:
            return None
        
        assert csr.rowcount == 1,\
                 "%s.peek(%s) found %d rows" % (table.getName(),\
                                                repr(id),\
                                                csr.rowcount)
        return self.csr2atoms(clist,csr.fetchone())
    
    def csr2atoms(self,clist,sqlatoms):
        l = []
        i = 0
        for a in clist.getAtoms():
            l.append(self.sql2value(sqlatoms[i],a.type))
            i += 1
        return l

        
    def executeZap(self,table):
        sql = "DELETE FROM " + table.getTableName()
        self.sql_exec(sql)
        
    def executeInsert(self,row):
        query = row._ds._store._peekQuery
        table = row._ds._table
        context = row.getSession()

        atomicRow = query.row2atoms(row)
        
        sql = "INSERT INTO %s (\n" % table.getTableName()
        l = []
        for atom in query.getFltAtoms(context): 
            l.append(atom.name) 
            
        sql += ", ".join(l)
        sql += " ) VALUES ( "
        l = []
        for atom in query.getFltAtoms(context):
            l.append(
                self.value2sql( atomicRow[atom.index],
                                     atom.type))
            
        sql += ", ".join(l)
        
        sql += " )"
        self.sql_exec(sql)
        
    def executeUpdate(self,row):
        query = row._ds._store._peekQuery
        table = row._ds._table
        context = row.getSession()

        atomicRow = query.row2atoms(row)

        sql = "UPDATE %s SET \n" % table.getTableName()
        
        l = []
        for atom in query.getFltAtoms(context): 
            l.append("%s = %s" % (
                atom.name,
                self.value2sql(atomicRow[atom.index],atom.type)))
            
        sql += ", ".join(l)
        sql += " WHERE "

        l = []
        i = 0
        id = row.getRowId()
        for (name,type) in table.getPrimaryAtoms():
            l.append("%s = %s" % (name,
                                  self.value2sql(id[i],type)))
            i += 1
        sql += " AND ".join(l)

        self.sql_exec(sql)

    def executeDelete(self,row):
        table = row._ds._table

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
        self.sql_exec(sql)


#class SqlQuery(Query):     
#   def __init__(self, leadTable, name=None):
#       Query.__init__(self,leadTable,name)
        

class ConsoleWrapper:
    
    """
    SQL requests are simply written to stdout.
    """

    def __init__(self,conn):
        if writer is None:
            self.writer = sys.stdout
        else:
            self.writer = writer

    def write(self,msg):
        self.writer.write(msg+";\n")



