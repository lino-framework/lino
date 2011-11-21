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

import os
import threading
#import time
from types import StringType
import datetime

try:
    import sqlite3 as sqlite # Python 2.5
except ImportError,e:
    try:
        import pysqlite2.dbapi2 as sqlite # pysqlite 2.0
    except ImportError,e:
        import sqlite # pysqlite 0.4.3
    
##     import warnings
##     warnings.filterwarnings("ignore",
##                             "DB-API extension",
##                             UserWarning,
##                             "sqlite")

##     import sqlite # pysqlite 0.4.3

from types import TupleType

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

        

class Connection(SqlConnection):
    
    def __init__(self,filename=None):
        self.threadLock = threading.Lock()
        SqlConnection.__init__(self)
        self.dbapi = sqlite
        
        #self._isTemporary = isTemporary
        self._mtime = 0.0
        self._filename = filename
        if filename is None:
            # assert isTemporary
            filename=":memory:"
        elif os.path.exists(filename):
            self._mtime = os.stat(filename).st_mtime
            self._status = self.CST_OPENED
            
        try:
            self._dbconn = sqlite.connect(filename,
                                          check_same_thread=False)
            
            self._dbconn.create_function("month",1,month)
            self._dbconn.create_function("year",1,year)
            self._dbconn.create_function("day",1,day)
                                          
        except sqlite.DatabaseError,e:
            raise DatabaseError(filename + ":" +str(e))
        


    def __str__(self):
        filename = self._filename
        if filename is None:
            filename = ':memory:'
        return "SQLiteConnection(%r)" % filename
        
        
        #print "SQLite database : " + os.path.abspath(filename)
        # self._dbcursor = self._dbconn.cursor()

##     def isVirtual(self):
##         return self._filename is None

    def sql_exec_really(self,sql):
        
        """sql must be a unicode strings if it contains non-ascii
            characters:"""
        
        if type(sql) == StringType:
            try:
                #sql=sql.decode("latin1")
                sql=sql.decode("ascii")
            except UnicodeDecodeError,e:
                raise "r%s : %s" % (sql,e)
            
        self.threadLock.acquire()
        csr=self._dbconn.cursor()
        #print "sqlite_dbd.py:" + sql
            
        try:
##              if "PARTNERS" in sql:
##                  print "sqlite_dbd.py:" + sql
            csr.execute(sql)
            self.threadLock.release()
            return csr
        except sqlite.DatabaseError,e:
            self.threadLock.release()
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
