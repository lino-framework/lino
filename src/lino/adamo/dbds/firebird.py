## Copyright 2005 Luc Saffre

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
from types import StringType
import datetime

import kinterbasdb

from lino.adamo.sql import SqlConnection
from lino.adamo import DatabaseError


# from lino.ui import console
# import console to make sure that sys.setdefaultencoding() is done
# because sqlite.Connection() will use this as default encoding.

def month(s):
    d=datetime.date.fromordinal(s)
    return d.month
def year(s):
    d=datetime.date.fromordinal(s)
    return d.year
def day(s):
    d=datetime.date.fromordinal(s)
    return d.day

# TEMP_DBNAME 

class Connection(SqlConnection):
    
    def __init__(self,ui,
                 filename=None, dsn=None, host=None,
                 user="sysdba",pwd="masterkey"):
        SqlConnection.__init__(self,ui)
        self.dbapi = kinterbasdb
        self._user=user
        self._pwd=pwd
        if dsn is not None:
            assert host is None
            assert filename is None
            host,filename=dsn.split(':',1)
        self._host=host
        
        if filename is None:
            self._filename=r"c:\temp\tmp.fdb"
            self._host="localhost"
            if os.path.exists(self._filename):
                os.remove(self._filename)
        else:
            self._filename = filename
            if os.path.exists(filename):
                self._mtime = os.stat(filename).st_mtime
                
            self._status = self.CST_OPENED
            self._dbconn = kinterbasdb.connect(
                host=self._host,
                database=filename,
                user=self._user,
                password=self._pwd)
            return
        
        
        self._mtime = 0.0
        self._dbconn = kinterbasdb.create_database(
        "create database '%s:%s' user '%s' password '%s'" % (
            self._host,self._filename,
            self._user,self._pwd))
            
            
##         try:

##             self._dbconn.create_function("month",1,month)
##             self._dbconn.create_function("year",1,year)
##             self._dbconn.create_function("day",1,day)
                                          
##         except kinterbasdb.DatabaseError,e:
##             raise DatabaseError(filename + ":" +str(e))
        


    def __str__(self):
        filename = self._filename
        return "%s (firebird)" % filename
        
        
    def sql_exec_really(self,sql):
        csr=self._dbconn.cursor()
        #print "sqlite_dbd.py:" + sql
        #if type(sql) == StringType:
        #    sql=sql.decode("latin1")
        try:
            csr.execute(sql)
            return csr
        except kinterbasdb.DatabaseError,e:
            #print sql
            raise DatabaseError('"%s" in sql_exec(%s)' % (e,sql))

        
    def commit_really(self):
        self._dbconn.commit()

    def close(self):
        if self._status == self.CST_CLOSED:
            return
        if self._status == self.CST_CLOSING:
            return
        self._status = self.CST_CLOSING
        self.commit()
        if self._dirty:
            self._dbconn.commit()
        self._dbconn.close()
        self._dbconn=None
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
        if csr is None:
            return False
        if csr.rowcount == 0:
            return False
        if csr.rowcount == 1:
            return True
        raise DatabaseError('"%s" returned %d' % (sql,csr.rowcount))
    

