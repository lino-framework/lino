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

import os
from types import StringType, UnicodeType
import datetime

from PyQt4 import QtSql
from PyQt4 import QtCore

##     import warnings
##     warnings.filterwarnings("ignore",
##                             "DB-API extension",
##                             UserWarning,
##                             "sqlite")

##     import sqlite # pysqlite 0.4.3

from types import TupleType

from lino.adamo.sql import SqlConnection #, SqlError
from lino.adamo import DatabaseError
from lino.adamo import datatypes



_qtapp=QtCore.QCoreApplication([])


def month(s):
    d=datetime.date.fromordinal(s)
    return d.month
def year(s):
    d=datetime.date.fromordinal(s)
    return d.year
def day(s):
    d=datetime.date.fromordinal(s)
    return d.day


        

class Connection(SqlConnection):
    
    def __init__(self,sess,name=None,filename=None):
        SqlConnection.__init__(self,sess)
        #self._isTemporary = isTemporary
        self._mtime = 0.0
        self._filename = filename
        
        if name is None:
            name=sess.name
            if name is None:
                name=sess.__class__.__name__
            if len(sess._connections):
                name+=str(len(sess._connections)+1)
        self.name=name

        if filename is None:
            # assert isTemporary
            filename=":memory:"
        elif os.path.exists(filename):
            self._mtime = os.stat(filename).st_mtime
            self._status = self.CST_OPENED

        self._dbconn=QtSql.QSqlDatabase.addDatabase("QSQLITE",self.name)
        self._dbconn.setDatabaseName(filename)
        _qtapp.processEvents()
        if not self._dbconn.open():
            raise DatabaseError(filename+":"+str(self._dbconn.lastError().text()))

##         handle=self._dbconn.driver().handle().data()
##         handle.create_function("month",1,month)
##         handle.create_function("year",1,year)
##         handle.create_function("day",1,day)
    

    def __str__(self):
        filename = self._filename
        if filename is None:
            filename = ':memory:'
        return "SQLiteConnection(%r)" % filename


    def sql2value(self,s,type):
        
        """Convert a QVariant to a Python value.

        """
        #print "sql.sql2value() :", s, type
        if s is None: return None
        if s.isNull(): return None
        
        if isinstance(type, datatypes.DateType):
            #return s.toDate()
            return s.toDate().toPyDate()
            #return datetime.date.fromordinal(s)
        
        elif isinstance(type, datatypes.BoolType):
            return s.toBool()
        elif isinstance(type, datatypes.LongType):
            n,ok=s.toLongLong()
            #assert ok, "oops"
            return n
        elif isinstance(type, datatypes.IntType):
            n,ok=s.toInt()
            #assert ok, "oops:"+repr(n)
            return n
        elif isinstance(type, datatypes.TimeStampType):
            return float(s.toFloat())
        elif isinstance(type, datatypes.TimeType):
            return type.parse(s.toString())
        elif isinstance(type, datatypes.DurationType):
            return type.parse(s.toString())
        elif isinstance(type, datatypes.PriceType):
            n,ok=s.toInt()
            return n
        elif isinstance(type, datatypes.StringType):
            #s=str(s.toString().toUtf8()).decode('utf8')
            s=unicode(s.toString())
        elif isinstance(type, datatypes.AsciiType):
            #s=str(s.toString().toAscii())
            s=str(s.toString())

        #s=s.toString()
        #print s
        #s=str(s.toString().toLatin1()) # .__str__()
        #s=unicode(s.toString().toUtf8())
        #s=s.__unicode__()
        
        assert s.__class__ in (StringType, UnicodeType), "%r is not a string" % s
            #print repr(s)
        #    raise ValueError("%r is not a string" % s)
        
        if len(s) == 0:
            return None
            
        return type.parse(s)
        
    
        
        
    def sql_exec_really(self,sql):
        
        """sql must be a unicode strings if it contains non-ascii
            characters:"""
        
        if type(sql) == StringType:
            try:
                #sql=sql.decode("latin1")
                sql=sql.decode("ascii")
            except UnicodeDecodeError,e:
                raise "r%s : %s" % (sql,e)

        #self.session.notice(sql)
        #self.session.breathe()
        
        return self._dbconn.exec_(sql)
            
        
    def commit_really(self):
        self._dbconn.commit()
        _qtapp.processEvents()

    def close(self):
        if self._status == self.CST_CLOSED:
            return
        if self._status == self.CST_CLOSING:
            return
        self._status = self.CST_CLOSING
        #self.commit()
        if self._dirty:
            self.commit()
        self._dbconn.close()
        #self.session.breathe()
        self._dbconn=None
        _qtapp.processEvents()
        QtSql.QSqlDatabase.removeDatabase(self.name)
        _qtapp.processEvents()
        self._status = self.CST_CLOSED
        #self._dbconn = None
##         if self._isTemporary and self._filename is not None:
##             os.remove(self._filename)

    def getModificationTime(self,table):
        return self._mtime

    def checkTableExist(self,tableName):
        sql = """SELECT rootpage
        FROM sqlite_master
        where tbl_name='%s' AND type='table';""" % tableName
        csr = self.sql_exec(sql)
        if csr.size() == 0:
            return False
        if csr.size() == 1:
            return True
        raise DatabaseError('"%s" returned %d' % (sql,csr.size()))
    

  

##  def executeCreateTable(self,table):
        
##      try:
##          self.sql_exec("DROP TABLE %s" % table.getName())
##      except sqlite.DatabaseError:
##          pass
##      SqlConnection.executeCreateTable(self,table)


    def checkDatabaseSchema(self,db):
        # not yet usable
        csr = self.sql_exec("""\
        SELECT * FROM sqlite_master
            WHERE type='table'
        UNION ALL
        SELECT * FROM sqlite_temp_master
        WHERE type='table' '
        ORDER BY name;
        """)
        print csr

    def executeCount(self,qry):
        sql = self.getSqlSelect(qry,sqlColumnNames='COUNT (*)' )
        csr = self.sql_exec(sql)
        csr.first()
        i,ok=csr.value(0).toInt()
        return i
    
    def executeGetLastId(self,table,knownId=()):
        pka = table.getPrimaryAtoms()
        # pka is a list of (name,type) tuples
        assert len(knownId) == len(pka) - 1
        if self.isVirtual():
            # means that sqlite_dbd.Connection._filename is None
            return None
        #print "qtconn.py:", table.getTableName(),pka,knownId
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
        csr.first()
        val=csr.value(0)
        assert not csr.next(), \
               "%s.executeGetLastId(%r) found more than one row" % (table.getName(), id)
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
        if not csr.first():
            return None
        #if csr.size() == 0:
        #    return None
        rec=csr.record()
        atomicRow=[rec.value(i) for i in range(len(qry.getAtoms()))]
        assert not csr.next(), \
               "%s.peek(%r) found more than one row" % (table.getName(), id)
        return self.csr2atoms(qry,atomicRow)
    
